#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2024 Ryo Isogawa 　　　　　
# SPDX-License-Identifier: BSD-3-Clause

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Joy
from motor_commands.msg import IdAngle
from motor_commands.srv import GetMotorStates
from motor_commands.srv import SetTorque
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from builtin_interfaces.msg import Duration
from std_msgs.msg import Int32, String
import os
import time
import json

# Operation Mode
# -1: Test
# 0: FullManual
# 2: Assist
MODE = 0

# Recording functionality has been removed

class SystemController(Node):
    def __init__(self):
        super().__init__('system_controller')
        self.get_logger().info('Run system controller node')
        
        # Recording-related state removed
        self.controllerMap = os.path.expanduser("~/CS_Animatronics/ControllerMap.json")

        # Load motor limit
        self.motorLimits = {}
        self.loadMotorLimits()
        
        # Setting for subscriber
        self.subscription = self.create_subscription(
            Joy,
            'controller_input',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

        # Setting for publisher
        self.publisher = self.create_publisher(
            IdAngle,
            'IdAngle',
            12
        )
        self.initial_pose_attempts = 0
        self.initial_pose_max_attempts = 5
        # 起動直後～トルクON完了まで定期的に初期姿勢を送信
        self.initial_pose_timer = self.create_timer(1.0, self.publish_initial_pose_until_ready)

        # Audio publisher for dinosaur sounds
        self.audio_publisher = self.create_publisher(
            Int32,
            'play_audio_id',
            10
        )
        
        # Feedback publisher for DualSense (LED, Rumble, Triggers)
        self.feedback_pub = self.create_publisher(
            String,
            'controller_feedback',
            10
        )
        # Trajectory publisher
        self.traj_publisher = self.create_publisher(
            JointTrajectory,
            'animatronics_trajectory',
            10
        )

        # Trajectory subscriber (for tracking playback state)
        self.traj_active = False
        self.traj_end_time = 0.0
        self.controller_timeout = 2.0
        self.last_joy_time = None
        self.controller_connected = False
        self.motion_playback_lock_ids = {
            41, 42, 43, 44,  # arms
            51, 52,          # tail
            60, 61, 62, 63, 64,
            65, 66, 67, 68, 69,  # legs
        }
        
        self.traj_subscription = self.create_subscription(
            JointTrajectory,
            'animatronics_trajectory',
            self.traj_callback,
            10
        )

        # Selection mode
        self.selecting = False
        self.file_list = []
        self.cursor_index = 0
        self.record_dir = os.path.expanduser("~/CS_Animatronics/MotionFiles")
        self.last_nav_time = 0.0
        self.assigning = False
        self.assign_stage = 0  # 0=button選択, 1=file選択
        # Friendly button labels for easier assignment
        self.button_labels = {
            "0": "Cross",
            "1": "Circle",
            "2": "Square",
            "3": "Triangle",
            "4": "L1",
            "5": "R1",
            "6": "L2",
            "7": "R2",
            "8": "Share",
            "9": "Options",
            # "10": "PS (Record)",  # Reserved for recording toggle
            "11": "L3",
            "12": "R3",
        }
        # Default assignment order (exclude PS)
        self.button_list = ["0","1","2","3","4","5","6","7","8","9","11","12"]
        self.selected_button = None
        
        # Audio mapping for dinosaur sounds
        self.audio_cooldown = {}  # Prevent rapid audio triggering
        
        # Jaw roar tracking
        self.last_jaw_position = self.motorLimits["11"]["max"]  # Start closed
        self.jaw_roar_threshold = 0.3  # Threshold for triggering roar (0-1 range) - lowered for testing
        self.last_roar_time = 0.0
        self.roar_cooldown = 3.0  # 3 seconds cooldown for jaw roar
        
        # Breathing sound management
        self.last_breathing_time = 0.0
        self.breathing_interval_min = 5.0   # Minimum 5 seconds between breaths
        self.breathing_interval_max = 10.0  # Maximum 10 seconds between breaths
        self.next_breathing_time = time.time() + 3.0  # First breath in 3 seconds (faster for testing)
        self.breathing_active = True
        
        # Audio directory setup
        self.audio_dir = self.find_audio_directory()
        self.get_logger().info(f"Using audio directory: {self.audio_dir}")

        # Recording previously here has been removed
    
    def find_audio_directory(self):
        """Find the correct audio directory"""
        import os
        audio_dirs = [
            os.path.expanduser("~/CS_Animatronics/AudioFiles"),
            "/Users/isogawaryou/CS_Animatronics/AudioFiles"
        ]
        for dir_path in audio_dirs:
            if os.path.exists(dir_path):
                return dir_path
        return None

    
    def listener_callback(self, msg):
        now = time.time()
        if self.last_joy_time is None:
            # First controller message after boot
            self.controller_connected = True
            self.last_joy_time = now
        elif now - self.last_joy_time > self.controller_timeout:
            self.controller_connected = False
            self.last_joy_time = now
            self.get_logger().debug("Controller inactive for >2s; suppressing manual publish.")
            return
        else:
            self.controller_connected = True
            self.last_joy_time = now

        try:
            # Rising-edge detection for all buttons
            max_btn = max(13, len(msg.buttons))
            curr_buttons = [False] * max_btn
            for i in range(min(len(msg.buttons), max_btn)):
                curr_buttons[i] = bool(msg.buttons[i])
            if not hasattr(self, 'prev_buttons') or not isinstance(self.prev_buttons, list):
                self.prev_buttons = [False] * max_btn
            elif len(self.prev_buttons) < max_btn:
                self.prev_buttons += [False] * (max_btn - len(self.prev_buttons))
            just_pressed = [curr_buttons[i] and not self.prev_buttons[i] for i in range(max_btn)]

            # Log axes and buttons
            # Axes [0:LeftStick_X, 1:LeftStick_Y, 2:LeftTrigger, 3:RightStick_X, 4:RightStick_Y, 5:RightTrigger]
            # Buttons [0:Cross, 1:Circle, 2:Square, 3:Triangle, 4:LeftBumper, 5:RightBumper, 6:LeftTrigger, 7:RightTrigger, 8:Share, 9:Options, 10:PS, 11:LeftStick, 12:RightStick]
            # Hat/D-pad [X:down-up, Y:left-right]
            #self.get_logger().info(f'Axes: {msg.axes}')
            #self.get_logger().info(f'Buttons: {msg.buttons}')

            # Select motion file
            if self.selecting:
                now = time.time()
                # R1 上へ / L1 下へ（エッジ）
                if just_pressed[5] and self.cursor_index > 0:
                    self.cursor_index -= 1
                    self.print_selection()
                elif just_pressed[4] and self.cursor_index < len(self.file_list)-1:
                    self.cursor_index += 1
                    self.print_selection()
                # Cross で選択確定（エッジ）
                if just_pressed[0]:
                    self.selecting = False
                    self.get_logger().info("Exit file selection mode")
                return

            # Share 押下で割当モード開始
            if not self.selecting and not self.assigning and just_pressed[8]:
                self.assigning = True; self.assign_stage = 0; self.cursor_index = 0
                self.file_list = self.button_list
                self.print_selection(); return

            if self.assigning:
                now = time.time()
                # R1/L1 でカーソル移動（エッジ）
                if just_pressed[5] and self.cursor_index > 0:
                    self.cursor_index -= 1; self.print_selection()
                elif just_pressed[4] and self.cursor_index < len(self.file_list)-1:
                    self.cursor_index += 1; self.print_selection()

                if just_pressed[0]:  # Cross（エッジ）
                    if self.assign_stage == 0:
                        self.selected_button = self.file_list[self.cursor_index]
                        self.assign_stage = 1
                        self.file_list = self.list_bag_records()
                        self.cursor_index = 0
                        self.print_selection()
                    else:
                        if not self.file_list:
                            self.get_logger().warn("No recorded motions available for assignment")
                            self.assigning = False
                            return
                        target = os.path.join(self.record_dir, self.file_list[self.cursor_index])
                        self.assign_motion(target, self.selected_button)
                        self.assigning = False
                return

            # translate values
            ids, angles = self.translate(msg.axes, just_pressed)
            if not ids:
                return
 
            # Check for breathing sound (background ambient sound)
            self.check_breathing_sound()
 
            # publish IdAngle
            new_msg = IdAngle()
            new_msg.ids = ids
            new_msg.angles = angles


            # Debug: Check new_msg contents AFTER assignment
            self.get_logger().debug(f'After assignment - new_msg.ids: {new_msg.ids} (length: {len(new_msg.ids)})')
            self.get_logger().debug(f'After assignment - new_msg.angles: {new_msg.angles} (length: {len(new_msg.angles)})')
            
            # Check if ROS2 added any extra elements
            if len(new_msg.ids) != len(ids):
                self.get_logger().error(f'ROS2 modified IDs length! Original: {len(ids)}, ROS2: {len(new_msg.ids)}')
            if len(new_msg.angles) != len(angles):
                self.get_logger().error(f'ROS2 modified angles length! Original: {len(angles)}, ROS2: {len(new_msg.angles)}')

            self.publisher.publish(new_msg)
            self.get_logger().debug(f'Publishing IDs: {new_msg.ids}')
            self.get_logger().debug(f'Publishing Angles: {new_msg.angles}')
            self.get_logger().debug(f'IDs length: {len(new_msg.ids)}, Angles length: {len(new_msg.angles)}')
        except Exception as e:
            self.get_logger().error(f"Error in listener_callback: {e}")
            return
        finally:
            # Update previous buttons for edge detection
            try:
                self.prev_buttons = curr_buttons
            except Exception:
                pass

    def send_feedback(self, cmd_dict):
        msg = String()
        msg.data = json.dumps(cmd_dict)
        self.feedback_pub.publish(msg)


    def loadMotorLimits(self):
        with open(os.path.expanduser("~/CS_Animatronics/Motor_Limits.json"), "r", encoding="utf-8") as file:
            data = json.load(file)

        for key, subdict in data.items():
            subdict["ini"] = int(subdict["ini"])
            subdict["min"] = int(subdict["min"])
            subdict["max"] = int(subdict["max"])
            subdict["acc"] = int(subdict["acc"])
            subdict["vel"] = int(subdict["vel"])

        self.motorLimits = data
        self.get_logger().info(f"Loaded motor limits: {self.motorLimits}")
        
        # Debug: Check data types
        for motor_id, limits in self.motorLimits.items():
            self.get_logger().info(f"Motor {motor_id}: min={limits['min']} ({type(limits['min'])}), max={limits['max']} ({type(limits['max'])}), ini={limits['ini']} ({type(limits['ini'])})")
    
    # Recording function removed

    """
    def AssignMotion(self):
        # Assign recorded motion to a button
        
        # Show current mapping of controller
        file = open(self.controllerMap, "r")
        data = json.load(file)
        self.get_logger().info(f"Currently motions areassigned like this: {data}")

        selectedButton = input("Select button to assign motion [0:Cross, 1:Circle, 2:Square, 3:Triangle, 4:LeftBumper, 5:RightBumper, 6:LeftTrigger, 7:RightTrigger, 8:Share, 9:Options, 10:PS, 11:LeftStick, 12:RightStick]: ")

        if int(selectedButton) in range(0,12):
            # Search recorded motion files
            fileFounded = os.listdir(os.path.expanduser("~/CS_Animatronics/MotionFiles"))
            # Chose a file to assign
            fileSelected = input(f"Chose file to assign {fileFounded}: ")
            path = os.path.join(os.path.expanduser("~/CS_Animatronics/MotionFiles"), fileSelected)
            data[selectedButton] = path
            # path to assign
            file = open(os.path.expanduser("~/CS_Animatronics/ControllerMap.json"), "w")
            self.get_logger().info(f"{fileFounded}")
            json.dump(data, file, indent=4)
            self.get_logger().info(f"Update: {data}")
    """
            
    def list_bag_records(self):
        if not os.path.isdir(self.record_dir):
            return []
        records = []
        for entry in sorted(os.listdir(self.record_dir)):
            if entry.endswith(".json"):
                records.append(entry)
        return records

    def assign_motion(self, filepath, button):
        if not os.path.exists(filepath) or not filepath.endswith(".json"):
            self.get_logger().error(f"Cannot assign motion; invalid JSON file: {filepath}")
            return
        with open(self.controllerMap, "r+") as f:
            data = json.load(f)
            data[button] = filepath
            f.seek(0); json.dump(data, f, indent=4); f.truncate()
        self.get_logger().info(f"Assigned '{os.path.basename(filepath)}' → Button {button}")

    def PlayMotion(self, button):
        self.get_logger().info(f"Start playing motion for button {button}")
        self.send_feedback({"type": "led", "r": 0, "g": 255, "b": 0})
        
        try:
            with open(self.controllerMap, "r") as file:
                data = json.load(file)
        except Exception as e:
            self.get_logger().error(f"Failed to load map: {e}")
            self.send_feedback({"type": "led", "r": 255, "g": 255, "b": 0})
            return
            
        path = data.get(button, "")
        if not path or not os.path.exists(path) or not path.endswith(".json"):
            self.get_logger().warn(f"Invalid motion file for button {button}: {path}")
            self.send_feedback({"type": "led", "r": 255, "g": 255, "b": 0})
            return

        try:
            with open(path, "r") as f:
                motion_data = json.load(f)
            if not motion_data:
                return

            msg = JointTrajectory()
            # Collect unique joints
            all_joints = set()
            for e in motion_data:
                for k in e.get("angles", {}).keys():
                    all_joints.add(str(k))
            msg.joint_names = list(all_joints)
            
            for entry in sorted(motion_data, key=lambda x: x["timestamp"]):
                point = JointTrajectoryPoint()
                sec = int(entry["timestamp"])
                nanosec = int((entry["timestamp"] - sec) * 1e9)
                point.time_from_start = Duration(sec=sec, nanosec=nanosec)
                point.positions = []
                for j in msg.joint_names:
                    # Provide default value safely or interpolation (for now default to 2048 or closest)
                    # For simplicity, if a joint is missing in a keypose, we just fall back to standard 'ini' from motorLimits.
                    ini_val = self.motorLimits.get(j, {}).get("ini", 2048)
                    val = entry["angles"].get(j, ini_val)
                    point.positions.append(float(val))
                msg.points.append(point)

            self.traj_publisher.publish(msg)
            self.get_logger().info(f"Published trajectory with {len(msg.points)} points to animatronics_trajectory.")
            
        except Exception as e:
            self.get_logger().error(f"Error playing motion: {e}")
            self.send_feedback({"type": "led", "r": 255, "g": 0, "b": 0})
            return

        self.get_logger().info("Finished triggering motion.")
        self.send_feedback({"type": "led", "r": 0, "g": 0, "b": 255})

    def traj_callback(self, msg: JointTrajectory):
        """Track motion playback to avoid fighting with manual commands."""
        if not msg.points:
            self.traj_active = False
            self.traj_end_time = 0.0
            self.get_logger().debug("Trajectory STOP signal received; manual control restored.")
            return

        # Determine how long playback should be considered active
        last_point = msg.points[-1]
        duration = last_point.time_from_start.sec + (last_point.time_from_start.nanosec * 1e-9)
        # Defensive: avoid negative durations
        duration = max(0.0, duration)
        self.traj_active = True
        self.traj_end_time = time.time() + duration
        self.get_logger().debug(f"Trajectory playback active for {duration:.2f}s.")

    def translate(self, axes, buttons):
        # Stop sending commands if controller disconnected for 2 seconds
        if not self.controller_connected:
            return [], []

        # Clear trajectory active flag if playback time has expired
        if self.traj_active and time.time() > self.traj_end_time:
            self.traj_active = False

        # Debug: Check MODE and axes values
        self.get_logger().debug(f"translate() called - MODE: {MODE}, axes: {axes[:6]}")
        
        # Buttons event
        # Cross
        if buttons[0]:
            self.get_logger().debug(f'Cross was pressed')
            self.PlayMotion("0")
            # self.play_dinosaur_sound(1)  # Basic roar - DISABLED

        # Circle
        elif buttons[1]:
            self.get_logger().debug(f'Circle was pressed')
            self.PlayMotion("1")
            # self.play_dinosaur_sound(2)  # Aggressive roar - DISABLED

        # Square
        elif buttons[2]:
            self.get_logger().debug(f'Square was pressed')
            self.PlayMotion("2")
            # self.play_dinosaur_sound(3)  # Growl - DISABLED

        # Triangle
        elif buttons[3]:
            self.get_logger().debug(f'Triangle was pressed')
            self.PlayMotion("3")
            # self.play_dinosaur_sound(4)  # Hiss - DISABLED

        # LeftBumper
        elif buttons[4]:
            self.get_logger().debug(f'LeftBumper was pressed')
            self.PlayMotion("4")
            # self.play_dinosaur_sound(5)  # Chomp - DISABLED

        # RightBumper
        elif buttons[5]:
            self.get_logger().debug(f'RightBumper was pressed')
            self.PlayMotion("5")
            # self.play_dinosaur_sound(6)  # Footstep - DISABLED

        # LeftTrigger
        elif buttons[6]:
            self.get_logger().debug(f'*** CONTROLLER LEFTTRIGGER *** was pressed - playing sound ID 7')
            # self.play_dinosaur_sound(7)  # Ground shake - DISABLED

        # RightTrigger
        elif buttons[7]:
            self.get_logger().debug(f'RightTrigger was pressed')
            # self.play_dinosaur_sound(8)  # Heavy breathing - DISABLED

        # Share
        elif buttons[8]:
            self.get_logger().debug(f'Share was pressed')
            """
            self.AssignMotion()
            """

        # Options
        elif buttons[9]:
            self.get_logger().debug(f'Options was pressed')
            # self.play_dinosaur_sound(9)  # Warning call - DISABLED

        # PS (removed recording toggle)
        elif buttons[10]:
            pass

        # LeftStick
        elif buttons[11]:
            self.get_logger().debug(f'LeftStick was pressed')
            self.PlayMotion("11")
            # self.play_dinosaur_sound(11)  # Pain sound - DISABLED

        # RightStick
        elif buttons[12]:
            self.get_logger().debug(f'RightStick was pressed')
            self.PlayMotion("12")
            # self.play_dinosaur_sound(12)  # Victory roar - DISABLED

        # Motor position control (always execute regardless of button state)
        if MODE == -1:
            # Test mode
            ids = [11]
            angles = [1024]
        elif MODE == 0:
            # FullManual mode - always execute for continuous control
            self.get_logger().debug(f"Executing MODE==0 (FullManual) with axes: {axes[:6]}")
            
            # Head/Neck (existing)
            jaw = self.jaw(axes[2])
            blinkRU, blinkRL, blinkLU, blinkLL = self.blink(axes[5])
            eyeR, eyeL = self.eyes(axes[3])
            neck31, neck32, neck33, neck34 = self.neck(axes[0], axes[4], axes[1])
            
            # Arms (New - Placeholder)
            # Default to center/initial for now. Can map to axes later.
            arm41, arm42, arm43, arm44 = self.arms()
            
            # Tail (New - Placeholder)
            tail51, tail52 = self.tail()
            
            # Legs (New - Placeholder)
            leg60, leg61, leg62, leg63, leg64, leg65, leg66, leg67, leg68, leg69 = self.legs()

            # Debug: Log motor command values (Sample)
            self.get_logger().debug(f"Motor commands - Jaw: {jaw}, Eyes: {eyeR}/{eyeL}, Neck: {neck31}/{neck32}")
            
            ids = [
                11, 12, 13, 
                21, 22, 23, 24, 
                31, 32, 33, 34,
                41, 42, 43, 44,
                51, 52,
                60, 61, 62, 63, 64,
                65, 66, 67, 68, 69
            ]
            
            angles = [
                jaw, eyeR, eyeL, 
                blinkRU, blinkRL, blinkLU, blinkLL, 
                neck31, neck32, neck33, neck34,
                arm41, arm42, arm43, arm44,
                tail51, tail52,
                leg60, leg61, leg62, leg63, leg64,
                leg65, leg66, leg67, leg68, leg69
            ]
            
            # Debug: Check for None values that might become 0
            # self.get_logger().info(f"IDs before publish: {ids} (length: {len(ids)})")
            # self.get_logger().info(f"Angles before publish: {angles} (length: {len(angles)})")
            
            # Check if any angle is None or 0
            for i, (id_val, angle_val) in enumerate(zip(ids, angles)):
                if angle_val is None:
                    self.get_logger().error(f"  [{i}] ID: {id_val} has None angle!")
                elif angle_val == 0:
                    self.get_logger().error(f"  [{i}] ID: {id_val} has 0 angle!")
                # self.get_logger().info(f"  [{i}] ID: {id_val} ({type(id_val)}), Angle: {angle_val} ({type(angle_val)})")
        else:
            # Default case
            ids = []
            angles = []

        if self.traj_active and ids:
            filtered_ids = []
            filtered_angles = []
            for motor_id, angle in zip(ids, angles):
                if motor_id in self.motion_playback_lock_ids:
                    continue
                filtered_ids.append(motor_id)
                filtered_angles.append(angle)

            if len(filtered_ids) != len(ids):
                self.get_logger().debug(
                    f"Skipping manual commands for IDs {set(ids) - set(filtered_ids)} during trajectory playback."
                )

            ids = filtered_ids
            angles = filtered_angles

        return ids, angles

    def publish_initial_pose_until_ready(self):
        """Send initial pose repeatedly so one command certainly arrives after torque ON."""
        if self.initial_pose_attempts >= self.initial_pose_max_attempts:
            if self.initial_pose_timer is not None:
                self.initial_pose_timer.cancel()
                self.initial_pose_timer = None
            return

        msg = IdAngle()
        for motor_id_str, limits in sorted(self.motorLimits.items(), key=lambda kv: int(kv[0])):
            try:
                motor_id = int(motor_id_str)
            except ValueError:
                continue
            ini = limits.get("ini")
            if ini is None:
                continue
            msg.ids.append(motor_id)
            msg.angles.append(int(ini))

        if not msg.ids:
            self.get_logger().warn("Initial pose publish skipped: no motor limits loaded.")
            if self.initial_pose_timer is not None:
                self.initial_pose_timer.cancel()
                self.initial_pose_timer = None
            return

        self.publisher.publish(msg)
        self.initial_pose_attempts += 1
        self.get_logger().info(
            f"Initial pose publish #{self.initial_pose_attempts}/{self.initial_pose_max_attempts} "
            f"({len(msg.ids)} motors)."
        )

        if self.initial_pose_attempts >= self.initial_pose_max_attempts and self.initial_pose_timer is not None:
            self.initial_pose_timer.cancel()
            self.initial_pose_timer = None

    def enter_selection_mode(self):
        self.selecting = True
        self.file_list = self.list_bag_records()
        self.cursor_index = 0
        self.print_selection()
        self.get_logger().info("Enter file selection mode")

    def print_selection(self):
        os.system('clear')
        # Assignment mode: stage 0 shows button names + current mapping
        if self.assigning and self.assign_stage == 0:
            # Load current mapping (if exists)
            mapping = {}
            try:
                if os.path.exists(self.controllerMap):
                    with open(self.controllerMap, 'r', encoding='utf-8') as f:
                        mapping = json.load(f)
            except Exception as e:
                self.get_logger().warn(f"Failed to load controller map: {e}")

            print("Select a button to assign:\n")
            for i, bid in enumerate(self.button_list):
                prefix = "▶ " if i == self.cursor_index else "  "
                label = self.button_labels.get(bid, f"Button {bid}")
                assigned = mapping.get(bid)
                assigned_name = os.path.basename(assigned) if assigned else "(none)"
                print(f"{prefix}{bid}: {label}  ->  {assigned_name}")
            print("\nUse R1/L1 to move, Cross to select.")
            return

        # File selection (assignment stage 1) or generic selection listing
        header = "Select a motion file:" if (self.assigning and self.assign_stage == 1) else "Select a file:"
        print(header + "\n")
        for i, fname in enumerate(self.file_list):
            prefix = "▶ " if i == self.cursor_index else "  "
            print(f"{prefix}{fname}")
        print("\nUse R1/L1 to move, Cross to select.")

    def print_record_mode_prompt(self):
        os.system('clear')
        print("=== 録画モード選択 ===\n")
        print("Cross  : コントローラー入力をそのまま rosbag に保存")
        print("Circle : トルクを OFF にして手で誘導したモーションを記録")
        print("PS     : キャンセルして通常操作に戻る")

    def blink(self, angle):
        # R2 mapping
        # 0.0 (Open/Up) to 1.0 (Closed/Down)
        
        # Feedback: Light click at end of travel to confirm 'closed' state?
        # Trigger Pulse mode at end?
        if angle > 0.9:
             if not getattr(self, 'blink_clicked', False):
                 self.send_feedback({"type": "trigger", "target": "R2", "mode": "pulse"})
                 self.blink_clicked = True
        else:
             if getattr(self, 'blink_clicked', False):
                 self.send_feedback({"type": "trigger", "target": "R2", "mode": "off"})
                 self.blink_clicked = False
        
        # Servo mapping (same 0-1 adjustment)
        blinkRU_min = self.motorLimits["21"]["min"]
        blinkRU_max = self.motorLimits["21"]["max"]
        
        # Assuming 0=Open, 1=Closed
        # Original: (1 - (angle+1)/2) -> 
        # If angle=-1(Open?), (1-0)=1 -> max? 
        # Actually standard servo:
        # Let's assume simpler linear map:
        # Blink usually 0 (Open) -> 1 (Closed)
        
        val = angle # 0.0 to 1.0
        
        angleRU = int(blinkRU_min + (val * (blinkRU_max - blinkRU_min)))
        angleRL = int(self.motorLimits["22"]["min"] + (val * (self.motorLimits["22"]["max"] - self.motorLimits["22"]["min"])))
        angleLU = int(self.motorLimits["23"]["min"] + (val * (self.motorLimits["23"]["max"] - self.motorLimits["23"]["min"]))) 
        angleLL = int(self.motorLimits["24"]["min"] + (val * (self.motorLimits["24"]["max"] - self.motorLimits["24"]["min"])))
        
        self.get_logger().debug(f"blink() returning: RU={angleRU}, RL={angleRL}, LU={angleLU}, LL={angleLL}")
        return angleRU, angleRL, angleLU, angleLL

    def jaw(self, angle):
        jaw_min = self.motorLimits["11"]["min"] # open (1536)
        jaw_max = self.motorLimits["11"]["max"] # close (2048)
        jaw_range = jaw_max - jaw_min  # Should be 512 now
        
        # Adaptive Trigger Logic (L2)
        # 1.0 (Open) to 0.0 (Closed)
        # angle ranges from -1 (Closed) to +1 (Open)
        
        # Let's map Resistance (Force) to Closing (more closed = harder to squeeze?)
        # Or, simulate "biting": Resistance starts low, increases as it closes (angle -> -1).
        
        # angle: -1.0 (Closed) ... +1.0 (Open)
        # trigger range: 0 (start) to 255 (end)
        
        # If angle is +1 (Open), trigger is at rest (0 force).
        # As you pull L2 (input increases), jaw closes (angle decreases).
        # We want more resistance as you pull deeper.
        
        # Simply set Rigid mode with force proportional to input?
        # Note: 'angle' here IS the input axis from controller (-1 to 1).
        # controller_publisher normalizes L2 to 0.0-1.0 range, but `translate` passes it raw?
        # wait, translate receives msg.axes.
        # In my new controller_publisher, axes[2] is L2 (0.0 to 1.0). Correct.
        # So 'angle' passed from translate is actually 0.0 to 1.0?
        # Let's check translate call:
        # translate(msg.axes...) calls jaw(axes[2])
        # In my new publisher, axes[2] is L2 (0.0 to 1.0).
        
        # Logic:
        # L2=0.0 (Open) -> Force=0
        # L2=1.0 (Closed) -> Force=255 (Max biting force)
        
        force_val = int(angle * 255) # angle is 0.0-1.0 from L2
        
        # Only update if changed significantly to reduce traffic
        if not hasattr(self, 'last_trigger_force') or abs(self.last_trigger_force - force_val) > 10:
             self.send_feedback({
                "type": "trigger", 
                "target": "L2", 
                "mode": "rigid", 
                "force": [0, force_val] # Start at 0, force scales with input
             })
             self.last_trigger_force = force_val
             
        # Re-calc position based on 0-1 input (invert for servo if needed)
        # If L2=0(Open), Pos=min (or max depending on mount).
        # Original logic: ((angle + 1)/2) assumed -1 to 1 range.
        # IF input is 0-1, we need to adjust formula.
        # Assuming original code worked with -1 to 1, I should map 0-1 to -1-1 for compatibility OR adjust formula.
        # Let's adjust formula for 0.0 (Open) to 1.0 (Closed).
        
        # Jaw: 0.0(Open) -> 1.0(Closed)
        # Servo: min(Open) -> max(Closed) usually? Or vice versa.
        # Original: jaw_max - ((angle+1)/2)*range
        # If angle was -1 (Closed?), result = jaw_max - 0 = jaw_max. So -1 was Closed?
        # If angle was 1 (Open?), result = jaw_min.
        # My new L2 is 0.0 (Released) to 1.0 (Pressed).
        # If Released(0.0) -> Open. If Pressed(1.0) -> Closed.
        # So 0.0 -> Open (min), 1.0 -> Closed (max).
        
        # current = jaw_min + (angle * range)  (if min=open, max=closed)
        # Check original comment: "jaw_min # open", "jaw_max # close".
        # So: target = jaw_min + (angle * jaw_range)
        
        current_jaw_position = int(jaw_min + (angle * jaw_range))
        
        # Safety clamp to prevent motor damage
        current_jaw_position = max(jaw_min, min(jaw_max, current_jaw_position))
        
        # Debug: Log jaw values for troubleshooting
        self.get_logger().info(f"Jaw: angle={angle:.2f}, position={current_jaw_position}, min={jaw_min}, max={jaw_max}, range={jaw_range}")
        
        # Calculate jaw opening percentage (0 = closed, 1 = fully open)
        jaw_opening = (jaw_max - current_jaw_position) / jaw_range
        
        # Check if jaw opened beyond threshold for roar
        previous_opening = (jaw_max - self.last_jaw_position) / jaw_range
        
        # Debug logging for jaw movement
        if abs(jaw_opening - previous_opening) > 0.1:  # Log significant jaw movements
            self.get_logger().info(f"Jaw movement: {previous_opening:.2f} → {jaw_opening:.2f}, threshold: {self.jaw_roar_threshold}")
        
        # Check roar trigger conditions
        current_time = time.time()
        condition1 = jaw_opening > self.jaw_roar_threshold
        condition2 = previous_opening <= self.jaw_roar_threshold  
        condition3 = current_time - self.last_roar_time > self.roar_cooldown
        
        # Debug log for roar conditions
        if condition1 and condition2:
            self.get_logger().info(f"Roar conditions: opening={condition1}, threshold_crossed={condition2}, cooldown_ok={condition3}")
        
        if (condition1 and condition2 and condition3):
            
            # Check for available roar files and select randomly
            import random
            import os
            
            if self.audio_dir is None:
                self.get_logger().warn("No AudioFiles directory found - skipping roar")
                self.last_jaw_position = current_jaw_position
                return current_jaw_position
            
            self.get_logger().info(f"Checking for roar files in: {self.audio_dir}")
            # Find available roar_X.wav files
            available_roars = []
            for i in range(1, 4):  # Check roar_1.wav to roar_3.wav
                roar_file = f"roar_{i}.wav"
                full_path = os.path.join(self.audio_dir, roar_file)
                self.get_logger().debug(f"Checking: {full_path}")
                if os.path.exists(full_path):
                    available_roars.append(f"roar_{i}")
                    self.get_logger().info(f"Found roar file: {roar_file}")
            
            # Only play if roar files are available
            if available_roars:
                selected_roar = random.choice(available_roars)
                self.get_logger().info(f"*** JAW AUTO ROAR *** Available: {available_roars}, Selected: {selected_roar}")
                self.play_dinosaur_sound_by_name(selected_roar)
                self.last_roar_time = current_time
                self.get_logger().info(f"*** JAW AUTO ROAR *** Opening: {jaw_opening:.2f}, Sound: {selected_roar}.wav")
            else:
                self.get_logger().warn(f"No roar_X.wav files found in AudioFiles directory: {self.audio_dir}")
        
        self.last_jaw_position = current_jaw_position
        self.get_logger().info(f"jaw() returning: {current_jaw_position}")
        return current_jaw_position
    
    def check_breathing_sound(self):
        """Check and play breathing sound when appropriate"""
        if not self.breathing_active:
            return
            
        current_time = time.time()
        
        # Check if it's time for next breath
        if current_time >= self.next_breathing_time:
            # Check if we're not in the middle of other sounds (roar cooldown)
            if current_time - self.last_roar_time > 3.0:  # No roar in last 3 seconds
                # Check for available breath_X.wav files
                import os
                import random
                
                if self.audio_dir is None:
                    self.get_logger().warn("No AudioFiles directory found - skipping breathing")
                    return
                
                # Find available breath_X.wav files
                available_breaths = []
                for i in range(1, 4):  # Check breath_1.wav to breath_3.wav
                    breath_file = f"breath_{i}.wav"
                    if os.path.exists(os.path.join(self.audio_dir, breath_file)):
                        available_breaths.append(f"breath_{i}")
                
                if available_breaths:
                    selected_breath = random.choice(available_breaths)
                    self.get_logger().info(f"Available breaths: {available_breaths}, Selected: {selected_breath}")
                    self.play_dinosaur_sound_by_name(selected_breath)
                    self.last_breathing_time = current_time
                    self.get_logger().info(f"Playing breathing sound: {selected_breath}.wav")
                else:
                    self.get_logger().warn(f"No breath_X.wav files found in AudioFiles directory: {self.audio_dir}")
                
                # Schedule next breath with random interval
                next_interval = random.uniform(self.breathing_interval_min, self.breathing_interval_max)
                self.next_breathing_time = current_time + next_interval
                self.get_logger().debug(f"Next breath scheduled in {next_interval:.1f} seconds")

    def eyes(self, angle):
        # 12: 右目 眼球Yaw（XL330）
        eyeR_min = self.motorLimits["12"]["min"]
        eyeR_max = self.motorLimits["12"]["max"]
        rangeR = eyeR_max - eyeR_min

        # 13: 左目 眼球Yaw（XL330）
        eyeL_min = self.motorLimits["13"]["min"]
        eyeL_max = self.motorLimits["13"]["max"]
        rangeL = eyeL_max - eyeL_min

        angleR = int(eyeR_min + (rangeR//2) - (angle/2)*rangeR)
        angleL = int(eyeL_min + (rangeL//2) + (angle/2)*rangeL)
        self.get_logger().debug(f"eyes() returning: R={angleR}, L={angleL}")
        return angleR, angleL

    def neck(self, leftStick_x, leftStick_y, rightStick_y):
        # 31: 首ベース Yaw（XM430） ← 左スティック上下
        neck31_min = self.motorLimits["31"]["min"]
        neck31_max = self.motorLimits["31"]["max"]
        range31 = neck31_max - neck31_min

        # 32: 首ミドル Pitch（XL430） ← 左スティック右左
        neck32_min = self.motorLimits["32"]["min"]
        neck32_max = self.motorLimits["32"]["max"]
        range32 = neck32_max - neck32_min

        # 33: 首ミドル Roll（2XC430-A） ← 左スティック上下
        neck33_min = self.motorLimits["33"]["min"]
        neck33_max = self.motorLimits["33"]["max"]
        range33 = neck33_max - neck33_min
        
        # 34: 首トップ Pitch（2XC430-B） ← 右スティック上下
        neck34_min = self.motorLimits["34"]["min"]
        neck34_max = self.motorLimits["34"]["max"]
        range34 = neck34_max - neck34_min
        
        neck31 = int(neck31_min + (range31//2) + (leftStick_y/2)*range31)  # Yaw ← 左スティック上下
        neck32 = int(neck32_min + (range32//2) + (-leftStick_x/2)*range32)  # Pitch ← 左スティック右左（反転）
        neck33 = int(neck33_min + (range33//2) + (leftStick_y/2)*range33)  # Roll ← 左スティック上下
        neck34 = int(neck34_min + (range34//2) + (rightStick_y/2)*range34)  # Top Pitch ← 右スティック上下
        self.get_logger().debug(f"neck() returning: 31={neck31}, 32={neck32}, 33={neck33}, 34={neck34}")
        return neck31, neck32, neck33, neck34
    
    def arms(self):
        # 41: 右肩, 42: 右肘, 43: 左肩, 44: 左肘
        # Placeholder: Return initial positions
        arm41 = self.motorLimits["41"]["ini"]
        arm42 = self.motorLimits["42"]["ini"]
        arm43 = self.motorLimits["43"]["ini"]
        arm44 = self.motorLimits["44"]["ini"]
        return arm41, arm42, arm43, arm44

    def tail(self):
        # 51: 尻尾右, 52: 尻尾左
        tail51 = self.motorLimits["51"]["ini"]
        tail52 = self.motorLimits["52"]["ini"]
        return tail51, tail52

    def legs(self):
        # 60-64: 左脚, 65-69: 右脚
        l60 = self.motorLimits.get("60", {}).get("ini", 2048)
        l61 = self.motorLimits.get("61", {}).get("ini", 2048)
        l62 = self.motorLimits.get("62", {}).get("ini", 2048)
        l63 = self.motorLimits.get("63", {}).get("ini", 2048)
        l64 = self.motorLimits.get("64", {}).get("ini", 2048)
        l65 = self.motorLimits.get("65", {}).get("ini", 2048)
        l66 = self.motorLimits.get("66", {}).get("ini", 2048)
        l67 = self.motorLimits.get("67", {}).get("ini", 2048)
        l68 = self.motorLimits.get("68", {}).get("ini", 2048)
        l69 = self.motorLimits.get("69", {}).get("ini", 2048)
        return l60, l61, l62, l63, l64, l65, l66, l67, l68, l69
    
    def play_dinosaur_sound(self, sound_id):
        """Play dinosaur sound with cooldown to prevent rapid triggering"""
        current_time = time.time()
        cooldown_key = f"sound_{sound_id}"
        
        # Check cooldown (minimum 1 second between same sound)
        if cooldown_key in self.audio_cooldown:
            if current_time - self.audio_cooldown[cooldown_key] < 1.0:
                return  # Skip if too soon
        
        # Update cooldown
        self.audio_cooldown[cooldown_key] = current_time
        
        # If this is not a breathing sound, delay next breath
        if sound_id != 8:  # 8 is breathing sound ID
            # Delay next breathing by 5 seconds to avoid overlap
            self.next_breathing_time = max(self.next_breathing_time, current_time + 5.0)
        
        # Publish audio command
        audio_msg = Int32()
        audio_msg.data = sound_id
        self.audio_publisher.publish(audio_msg)
        self.get_logger().info(f'Playing dinosaur sound ID: {sound_id}')
    
    def play_dinosaur_sound_by_name(self, sound_name):
        """Play dinosaur sound by filename (without .wav extension)"""
        current_time = time.time()
        cooldown_key = f"sound_{sound_name}"
        
        # Check cooldown (minimum 1 second between same sound)
        if cooldown_key in self.audio_cooldown:
            if current_time - self.audio_cooldown[cooldown_key] < 1.0:
                return  # Skip if too soon
        
        # Update cooldown
        self.audio_cooldown[cooldown_key] = current_time
        
        # If this is not a breathing sound, delay next breath
        if not sound_name.startswith("breath_"):
            # Delay next breathing by 5 seconds to avoid overlap
            self.next_breathing_time = max(self.next_breathing_time, current_time + 5.0)
        
        # Publish audio command by name
        from std_msgs.msg import String
        audio_msg = String()
        audio_msg.data = f"{sound_name}.wav"
        
        # Create name-based publisher if not exists
        if not hasattr(self, 'audio_name_publisher'):
            self.audio_name_publisher = self.create_publisher(String, 'play_audio_name', 10)
        
        self.audio_name_publisher.publish(audio_msg)
        self.get_logger().info(f'Playing dinosaur sound by name: {sound_name}.wav')

def main(args=None):
    rclpy.init(args=args)
    node = SystemController()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

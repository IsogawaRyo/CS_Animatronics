#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2024 Ryo Isogawa 　　　　　
# SPDX-License-Identifier: BSD-3-Clause

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Joy
from motor_commands.msg import IdAngle
from motor_commands.srv import GetMotorStates
from motor_commands.srv import SetTorque
from rosbag2_py import (
    SequentialReader,
    SequentialWriter,
    StorageOptions,
    ConverterOptions,
    TopicMetadata,
)
from rclpy.serialization import serialize_message, deserialize_message
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
        self.controllerMap = "/home/csanimatronics/CS_Animatronics/ControllerMap.json"

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
        
        # Audio publisher for dinosaur sounds
        self.audio_publisher = self.create_publisher(
            Int32,
            'play_audio_id',
            10
        )

        # Selection mode
        self.selecting = False
        self.file_list = []
        self.cursor_index = 0
        self.record_dir = "/home/csanimatronics/CS_Animatronics/MotionFiles"
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

        # ===== New Recording (torque-off, hand-guided) =====
        self.is_recording = False
        self.record_ids = [int(k) for k in self.motorLimits.keys()]
        self.record_start_time = None
        self.record_calling = False
        self.motion_dir = "/home/csanimatronics/CS_Animatronics/MotionFiles"
        self.bag_writer = None
        self.current_bag_uri = None
        self.bag_topic_name = "/recorded_motor_states"

        # Service clients
        self.get_motor_states_client = self.create_client(GetMotorStates, 'get_motor_states')
        self.set_torque_client = self.create_client(SetTorque, 'set_torque')
        
        # Background timer for recording sampling (20 Hz)
        self.record_timer = self.create_timer(0.05, self.record_timer_callback)
    
    def find_audio_directory(self):
        """Find the correct audio directory"""
        import os
        audio_dirs = [
            "/home/csanimatronics/CS_Animatronics/AudioFiles",
            "/Users/isogawaryou/CS_Animatronics/AudioFiles"
        ]
        for dir_path in audio_dirs:
            if os.path.exists(dir_path):
                return dir_path
        return None

    
    def listener_callback(self, msg):
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
 
            # Check for breathing sound (background ambient sound)
            self.check_breathing_sound()
 
            # publish IdAngle
            new_msg = IdAngle()
            new_msg.ids = ids
            new_msg.angles = angles

            # Debug: Check new_msg contents AFTER assignment
            self.get_logger().info(f'After assignment - new_msg.ids: {new_msg.ids} (length: {len(new_msg.ids)})')
            self.get_logger().info(f'After assignment - new_msg.angles: {new_msg.angles} (length: {len(new_msg.angles)})')
            
            # Check if ROS2 added any extra elements
            if len(new_msg.ids) != len(ids):
                self.get_logger().error(f'ROS2 modified IDs length! Original: {len(ids)}, ROS2: {len(new_msg.ids)}')
            if len(new_msg.angles) != len(angles):
                self.get_logger().error(f'ROS2 modified angles length! Original: {len(angles)}, ROS2: {len(new_msg.angles)}')

            self.publisher.publish(new_msg)
            self.get_logger().info(f'Publishing IDs: {new_msg.ids}')
            self.get_logger().info(f'Publishing Angles: {new_msg.angles}')
            self.get_logger().info(f'IDs length: {len(new_msg.ids)}, Angles length: {len(new_msg.angles)}')
        except Exception as e:
            self.get_logger().error(f"Error in listener_callback: {e}")
            return
        finally:
            # Update previous buttons for edge detection
            try:
                self.prev_buttons = curr_buttons
            except Exception:
                pass

    # ===== Recording helpers =====
    def start_recording(self):
        if self.is_recording:
            return
        os.makedirs(self.motion_dir, exist_ok=True)
        bag_folder = time.strftime("record_%Y%m%d_%H%M%S")
        bag_uri = os.path.join(self.motion_dir, bag_folder)

        try:
            storage_options = StorageOptions(uri=bag_uri, storage_id='sqlite3')
            converter_options = ConverterOptions(input_serialization_format='cdr', output_serialization_format='cdr')
            writer = SequentialWriter()
            writer.open(storage_options, converter_options)
            topic_metadata = TopicMetadata(
                name=self.bag_topic_name,
                type='motor_commands/msg/IdAngle',
                serialization_format='cdr',
            )
            writer.create_topic(topic_metadata)
        except Exception as exc:
            self.get_logger().error(f"Failed to start rosbag recording: {exc}")
            return

        self.bag_writer = writer
        self.current_bag_uri = bag_uri
        self.is_recording = True
        self.record_start_time = time.time()
        self.get_logger().info(f"Recording START (torque OFF) → {bag_uri}")
        # Request torque OFF
        if self.set_torque_client.service_is_ready():
            req = SetTorque.Request()
            req.ids = [int(i) for i in self.record_ids]
            req.enable = False
            self.set_torque_client.call_async(req)
        else:
            self.get_logger().warn("set_torque service not ready; cannot disable torque")

    def stop_recording(self):
        if not self.is_recording:
            return
        self.is_recording = False
        # Request torque ON
        if self.set_torque_client.service_is_ready():
            req = SetTorque.Request()
            req.ids = [int(i) for i in self.record_ids]
            req.enable = True
            self.set_torque_client.call_async(req)
        else:
            self.get_logger().warn("set_torque service not ready; cannot re-enable torque")

        self.record_start_time = None
        if self.bag_writer is not None:
            self.get_logger().info(f"Recording SAVED: {self.current_bag_uri}")
            self.bag_writer = None
        else:
            self.get_logger().warn("Recording stopped but no bag writer was active")
        self.current_bag_uri = None

    def record_timer_callback(self):
        # Periodically sample positions during recording
        if not self.is_recording or self.bag_writer is None:
            return
        if self.record_calling:
            return
        if not self.get_motor_states_client.service_is_ready():
            return

        self.record_calling = True
        req = GetMotorStates.Request()
        req.ids = [int(i) for i in self.record_ids]

        future = self.get_motor_states_client.call_async(req)

        def on_response(fut):
            try:
                resp = fut.result()
                if resp is None:
                    return

                ids = list(resp.ids)
                positions = list(resp.positions)
                if not ids or not positions:
                    return

                if len(ids) != len(positions):
                    self.get_logger().error(
                        f"record sample mismatch: ids={len(ids)} positions={len(positions)}"
                    )
                    return

                if not self.is_recording or self.bag_writer is None:
                    return

                bag_msg = IdAngle()
                bag_msg.ids = ids
                bag_msg.angles = positions

                timestamp_ns = int(time.time() * 1_000_000_000)
                serialized = serialize_message(bag_msg)
                self.bag_writer.write(self.bag_topic_name, serialized, timestamp_ns)
            except Exception as e:
                self.get_logger().error(f"record sample failed: {e}")
            finally:
                self.record_calling = False

        future.add_done_callback(on_response)

    def loadMotorLimits(self):
        with open("/home/csanimatronics/CS_Animatronics/Motor_Limits.json", "r", encoding="utf-8") as file:
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
            self.get_logger().info(f"Motor {motor_id}: min={limits['min']} ({type(limits['min'])}), max={limits['max']} ({type(limits['max'])})")
    
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
            fileFounded = os.listdir("/home/csanimatronics/CS_Animatronics/MotionFiles")
            # Chose a file to assign
            fileSelected = input(f"Chose file to assign {fileFounded}: ")
            path = os.path.join("/home/csanimatronics/CS_Animatronics/MotionFiles", fileSelected)
            data[selectedButton] = path
            # path to assign
            file = open("/home/csanimatronics/CS_Animatronics/ControllerMap.json", "w")
            self.get_logger().info(f"{fileFounded}")
            json.dump(data, file, indent=4)
            self.get_logger().info(f"Update: {data}")
    """
            
    def list_bag_records(self):
        if not os.path.isdir(self.record_dir):
            return []

        records = []
        for entry in sorted(os.listdir(self.record_dir)):
            full_path = os.path.join(self.record_dir, entry)
            metadata_path = os.path.join(full_path, "metadata.yaml")
            if os.path.isdir(full_path) and os.path.exists(metadata_path):
                records.append(entry)
        return records

    def assign_motion(self, filepath, button):
        if not os.path.isdir(filepath):
            self.get_logger().error(f"Cannot assign motion; directory missing: {filepath}")
            return
        if not os.path.exists(os.path.join(filepath, "metadata.yaml")):
            self.get_logger().error(f"Cannot assign motion; metadata.yaml missing in {filepath}")
            return

        with open(self.controllerMap, "r+") as f:
            data = json.load(f)
            data[button] = filepath
            f.seek(0); json.dump(data, f, indent=4); f.truncate()
        self.get_logger().info(f"Assigned '{os.path.basename(filepath)}' → Button {button}")

    def PlayMotion(self, button):
        self.get_logger().info(f"Start playing recorded motion for button {button}")
        
        # Load motion file mapping
        try:
            with open(self.controllerMap, "r") as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            self.get_logger().error(f"Failed to load controller mapping: {e}")
            return
            
        path = data.get(button, "")
        
        # Check if button has assigned motion
        if not path or path.strip() == "":
            self.get_logger().info(f"No motion assigned to button {button}")
            return
            
        if path.endswith('.json'):
            self.get_logger().warn(f"Legacy JSON motion detected; please re-record using rosbag: {path}")
            return

        if not os.path.isdir(path):
            self.get_logger().error(f"Motion bag directory not found: {path}")
            return

        metadata_path = os.path.join(path, "metadata.yaml")
        if not os.path.exists(metadata_path):
            self.get_logger().error(f"Invalid bag directory (missing metadata.yaml): {path}")
            return

        storage_options = StorageOptions(uri=path, storage_id='sqlite3')
        converter_options = ConverterOptions(input_serialization_format='cdr', output_serialization_format='cdr')
        reader = SequentialReader()

        try:
            reader.open(storage_options, converter_options)
        except Exception as e:
            self.get_logger().error(f"Failed to open rosbag {path}: {e}")
            return

        last_timestamp = None

        try:
            while reader.has_next():
                topic, raw, timestamp = reader.read_next()
                if topic != self.bag_topic_name:
                    continue

                msg = deserialize_message(raw, IdAngle)
                if last_timestamp is not None:
                    delta = (timestamp - last_timestamp) / 1_000_000_000
                    if delta > 0:
                        time.sleep(delta)
                last_timestamp = timestamp

                new_msg = IdAngle()
                new_msg.ids = list(msg.ids)
                new_msg.angles = list(msg.angles)

                self.publisher.publish(new_msg)
                self.get_logger().info(f'Playing recorded motion: {new_msg.ids}, Angles: {new_msg.angles}')
        except Exception as e:
            self.get_logger().error(f"Error during motion playback: {e}")
            return
        finally:
            del reader

        self.get_logger().info("Finish playing recorded motion") 

    def translate(self, axes, buttons):
        # Debug: Check MODE and axes values
        self.get_logger().info(f"translate() called - MODE: {MODE}, axes: {axes[:6]}")
        
        # Buttons event
        # Cross
        if buttons[0]:
            self.get_logger().info(f'Cross was pressed')
            self.PlayMotion("0")
            # self.play_dinosaur_sound(1)  # Basic roar - DISABLED

        # Circle
        elif buttons[1]:
            self.get_logger().info(f'Circle was pressed')
            self.PlayMotion("1")
            # self.play_dinosaur_sound(2)  # Aggressive roar - DISABLED

        # Square
        elif buttons[2]:
            self.get_logger().info(f'Square was pressed')
            self.PlayMotion("2")
            # self.play_dinosaur_sound(3)  # Growl - DISABLED

        # Triangle
        elif buttons[3]:
            self.get_logger().info(f'Triangle was pressed')
            self.PlayMotion("3")
            # self.play_dinosaur_sound(4)  # Hiss - DISABLED

        # LeftBumper
        elif buttons[4]:
            self.get_logger().info(f'LeftBumper was pressed')
            self.PlayMotion("4")
            # self.play_dinosaur_sound(5)  # Chomp - DISABLED

        # RightBumper
        elif buttons[5]:
            self.get_logger().info(f'RightBumper was pressed')
            self.PlayMotion("5")
            # self.play_dinosaur_sound(6)  # Footstep - DISABLED

        # LeftTrigger
        elif buttons[6]:
            self.get_logger().info(f'*** CONTROLLER LEFTTRIGGER *** was pressed - playing sound ID 7')
            # self.play_dinosaur_sound(7)  # Ground shake - DISABLED

        # RightTrigger
        elif buttons[7]:
            self.get_logger().info(f'RightTrigger was pressed')
            # self.play_dinosaur_sound(8)  # Heavy breathing - DISABLED

        # Share
        elif buttons[8]:
            self.get_logger().info(f'Share was pressed')
            """
            self.AssignMotion()
            """

        # Options
        elif buttons[9]:
            self.get_logger().info(f'Options was pressed')
            # self.play_dinosaur_sound(9)  # Warning call - DISABLED

        # PS (record toggle) — rising-edge only (buttons passed are just_pressed)
        elif buttons[10]:
            if not self.is_recording:
                self.start_recording()
            else:
                self.stop_recording()

        # LeftStick
        elif buttons[11]:
            self.get_logger().info(f'LeftStick was pressed')
            self.PlayMotion("11")
            # self.play_dinosaur_sound(11)  # Pain sound - DISABLED

        # RightStick
        elif buttons[12]:
            self.get_logger().info(f'RightStick was pressed')
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
            jaw = self.jaw(axes[2])
            blinkRU, blinkRL, blinkLU, blinkLL = self.blink(axes[5])
            eyeR, eyeL = self.eyes(axes[3])
            neck31, neck32, neck33, neck34 = self.neck(axes[0], axes[4], axes[1])
            
            # Debug: Log motor command values
            self.get_logger().info(f"Motor commands - Jaw: {jaw}, Eyes: {eyeR}/{eyeL}, Blink: {blinkRU}/{blinkRL}/{blinkLU}/{blinkLL}, Neck: {neck31}/{neck32}/{neck33}/{neck34}")
            
            ids = [11, 12, 13, 21, 22, 23, 24, 31, 32, 33, 34]
            angles = [jaw, eyeR, eyeL, blinkRU, blinkRL, blinkLU, blinkLL, neck31, neck32, neck33, neck34]
            
            # Debug: Check for None values that might become 0
            self.get_logger().info(f"IDs before publish: {ids} (length: {len(ids)})")
            self.get_logger().info(f"Angles before publish: {angles} (length: {len(angles)})")
            
            # Check if any angle is None or 0
            for i, (id_val, angle_val) in enumerate(zip(ids, angles)):
                if angle_val is None:
                    self.get_logger().error(f"  [{i}] ID: {id_val} has None angle!")
                elif angle_val == 0:
                    self.get_logger().error(f"  [{i}] ID: {id_val} has 0 angle!")
                self.get_logger().info(f"  [{i}] ID: {id_val} ({type(id_val)}), Angle: {angle_val} ({type(angle_val)})")
        else:
            # Default case
            ids = []
            angles = []

        return ids, angles

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

    def blink(self, angle):
        # 21: 右 上まぶた（XL330）
        blinkRU_min = self.motorLimits["21"]["min"]
        blinkRU_max = self.motorLimits["21"]["max"]
        rangeRU = blinkRU_max - blinkRU_min
        
        # 22: 右 下まぶた（XL330）
        blinkRL_min = self.motorLimits["22"]["min"]
        blinkRL_max = self.motorLimits["22"]["max"]
        rangeRL = blinkRL_max - blinkRL_min
        
        # 23: 左 上まぶた（XL330）
        blinkLU_min = self.motorLimits["23"]["min"]
        blinkLU_max = self.motorLimits["23"]["max"]
        rangeLU = blinkLU_max - blinkLU_min

        # 24: 左 下まぶた（XL330）
        blinkLL_min = self.motorLimits["24"]["min"]
        blinkLL_max = self.motorLimits["24"]["max"]
        rangeLL = blinkLL_max - blinkLL_min
 
        # 修正版：min/maxの範囲をフル活用
        # angle=-1: 初期位置, angle=+1: 最大開閉
        angleRU = int(blinkRU_min + (blinkRU_max - blinkRU_min) * (1 - (angle+1)/2))  # 21: 右上まぶた
        angleRL = int(blinkRL_min + (blinkRL_max - blinkRL_min) * (1 - (angle+1)/2))  # 22: 右下まぶた  
        angleLU = int(blinkLU_min + (blinkLU_max - blinkLU_min) * ((angle+1)/2))      # 23: 左上まぶた
        angleLL = int(blinkLL_min + (blinkLL_max - blinkLL_min) * ((angle+1)/2))      # 24: 左下まぶた
   
        print(f"{self.motorLimits['24']['ini']} - {(angle+1)/2} * {rangeLL} = {angleLL}")

        self.get_logger().debug(f"blink() returning: RU={angleRU}, RL={angleRL}, LU={angleLU}, LL={angleLL}")
        return angleRU, angleRL, angleLU, angleLL

    def jaw(self, angle):
        jaw_min = self.motorLimits["11"]["min"] # open (1536)
        jaw_max = self.motorLimits["11"]["max"] # close (2048)
        jaw_range = jaw_max - jaw_min  # Should be 512 now
        
        # angle: -1 = fully closed, +1 = fully open
        # Convert to motor position: jaw_max (closed) to jaw_min (open)
        current_jaw_position = int(jaw_max - ((angle + 1)/2)*jaw_range)
        
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

#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2024 Ryo Isogawa 　　　　　
# SPDX-License-Identifier: BSD-3-Clause

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Joy
from motor_commands.msg import IdAngle
from motor_commands.srv import GetMotorStates
from std_msgs.msg import Int32, String
import os
import time
from datetime import datetime
import json

# Operation Mode
# -1: Test
# 0: FullManual
# 2: Assist
MODE = 0

# Recording Check
# 0: not recording
# 1: recording
# 2: signal for starting
IS_RECORDING = 0

class SystemController(Node):
    def __init__(self):
        super().__init__('system_controller')
        self.get_logger().info('Run system controller node')
        
        # Initialize variables used for record function 
        self.start_time = None
        self.recorded_data = []
        self.record_file = None
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
        self.ignore_cross = False
        self.assigning = False
        self.assign_stage = 0  # 0=button選択, 1=file選択
        self.button_list = ["0","1","2","3","4","5","6","7","8","9","11","12"]
        self.selected_button = None
        
        # Audio mapping for dinosaur sounds
        self.audio_cooldown = {}  # Prevent rapid audio triggering
        
        # Jaw roar tracking
        self.last_jaw_position = self.motorLimits["11"]["max"]  # Start closed
        self.jaw_roar_threshold = 0.6  # Threshold for triggering roar (0-1 range)
        self.last_roar_time = 0.0
        self.roar_cooldown = 3.0  # 3 seconds cooldown for jaw roar

    
    def listener_callback(self, msg):
        try:
            # Log axes and buttons
            # Axes [0:LeftStick_X, 1:LeftStick_Y, 2:LeftTrigger, 3:RightStick_X, 4:RightStick_Y, 5:RightTrigger]
            # Buttons [0:Cross, 1:Circle, 2:Square, 3:Triangle, 4:LeftBumper, 5:RightBumper, 6:LeftTrigger, 7:RightTrigger, 8:Share, 9:Options, 10:PS, 11:LeftStick, 12:RightStick]
            # Hat/D-pad [X:down-up, Y:left-right]
            #self.get_logger().info(f'Axes: {msg.axes}')
            #self.get_logger().info(f'Buttons: {msg.buttons}')

            # Cross 決定後、リリースを待
            if self.ignore_cross:
                if not msg.buttons[0]:
                    self.ignore_cross = False
                return

            # Select motion file
            if self.selecting:
                now = time.time()
                # press R1 to move up
                if now -self.last_nav_time > 0.3:
                    if msg.buttons[5] and self.cursor_index > 0:
                        self.cursor_index -= 1
                        self.print_selection()
                        self.last_nav_time = now
                    # press L1 to move down
                    elif msg.buttons[4] and self.cursor_index < len(self.file_list)-1:
                        self.cursor_index += 1
                        self.print_selection()
                        self.last_nav_time = now
                # Cross ボタン（buttons[0]）で選択確定
                if msg.buttons[0]:
                    self.selecting = False
                    self.ignore_cross = True 
                    self.get_logger().info("Exit file selection mode")
                return

            # Share 押下で割当モード開始
            if not self.selecting and not self.assigning and msg.buttons[8]:
                self.assigning = True; self.assign_stage = 0; self.cursor_index = 0
                self.file_list = self.button_list
                self.print_selection(); return

            if self.assigning:
                now = time.time()
                if now - self.last_nav_time > 0.3:
                    if msg.buttons[5] and self.cursor_index > 0:
                        self.cursor_index -= 1; self.print_selection(); self.last_nav_time = now
                    elif msg.buttons[4] and self.cursor_index < len(self.file_list)-1:
                        self.cursor_index += 1; self.print_selection(); self.last_nav_time = now

                if msg.buttons[0]:  # Cross
                    if self.assign_stage == 0:
                        self.selected_button = self.file_list[self.cursor_index]
                        self.assign_stage = 1
                        self.file_list = sorted(os.listdir(self.record_dir))
                        self.cursor_index = 0
                        self.print_selection()
                    else:
                        self.assign_motion(os.path.join(self.record_dir, self.file_list[self.cursor_index]), self.selected_button)
                        self.assigning = False
                    time.sleep(0.2)
                return

            # translate values
            ids, angles = self.translate(msg.axes, msg.buttons)
 
            # Record
            self.record(ids, angles)

            # publish IdAngle
            new_msg = IdAngle()
            new_msg.ids = ids
            new_msg.angles = angles

            self.publisher.publish(new_msg)
            self.get_logger().info(f'Publishing IDs: {new_msg.ids}, Angles: {new_msg.angles}')
        except Exception as e:
            self.get_logger().error(f"Error in listener_callback: {e}")
            return

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
        print(f"{self.motorLimits}")
    
    def record(self, ids, angles):
        # Record motion
        global IS_RECORDING
        if IS_RECORDING != 0:
            # Initialize
            if IS_RECORDING == 2:
                # This event called once when recording started
                IS_RECORDING = 1 
                self.start_time = time.time()
                self.recorded_data = []

                # Open recording file
                filename = datetime.now().strftime("record_%Y%m%d_%H%M%S.json")
                self.record_file = open(f"/home/csanimatronics/CS_Animatronics/MotionFiles/{filename}", "w")
                self.get_logger().info(f"Start recording {self.start_time}")

            time_passed = time.time() - self.start_time
            self.get_logger().info(f"On recording [{time_passed}]")

        # Save data
            angles_ = {}
            for i, id in enumerate(ids):
                angles_[id] = angles[i]
            dict_ = {str(motor_id): angle for motor_id, angle in zip(ids, angles)}
            entry = {
                "timestamp": time_passed,
                "angles": dict_,
            }
            self.recorded_data.append(entry)
            print(self.recorded_data)

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
            
    def assign_motion(self, filepath, button):
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
            
        # Check if file exists
        if not os.path.exists(path):
            self.get_logger().error(f"Motion file not found: {path}")
            return

        # Load and play motion
        try:
            with open(path, "r") as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError, PermissionError) as e:
            self.get_logger().error(f"Failed to load motion file {path}: {e}")
            return

        timestamps = [entry["timestamp"] for entry in data]
        angles = [entry["angles"] for entry in data]

        # Caluculate time diff
        timediffs = [timestamps[0]]
        for i in range(len(timestamps) - 1):
            timediffs.append(timestamps[i+1] - timestamps[i])
        print(timediffs)
 
        try:
            for i, timediff in enumerate(timediffs):
                ###
                timediffs = 0.02
                ###
                time.sleep(timediff)
                dict_ = angles[i]
                buttons = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                ids = []
                angles_ = []
                for id, angle in dict_.items():
                    try:
                        ids.append(int(id))
                        angles_.append(angle)
                    except (ValueError, TypeError) as e:
                        self.get_logger().error(f"Invalid data in motion file: id={id}, angle={angle}, error={e}")
                        continue

                # publish IdAngle
                new_msg = IdAngle()
                new_msg.ids = ids
                new_msg.angles = angles_

                self.publisher.publish(new_msg)
                self.get_logger().info(f'Playing recorded motion: {new_msg.ids}, Angles: {new_msg.angles}')
        except Exception as e:
            self.get_logger().error(f"Error during motion playback: {e}")
            return

        self.get_logger().info(f"Finish playing recorded motion") 

    def translate(self, axes, buttons):
        # Buttons event
        # Cross
        if buttons[0]:
            self.get_logger().info(f'Cross was pressed')
            self.PlayMotion("0")
            self.play_dinosaur_sound(1)  # Basic roar

        # Circle
        elif buttons[1]:
            self.get_logger().info(f'Circle was pressed')
            self.PlayMotion("1")
            self.play_dinosaur_sound(2)  # Aggressive roar

        # Square
        elif buttons[2]:
            self.get_logger().info(f'Square was pressed')
            self.PlayMotion("2")
            self.play_dinosaur_sound(3)  # Growl

        # Triangle
        elif buttons[3]:
            self.get_logger().info(f'Triangle was pressed')
            self.PlayMotion("3")
            self.play_dinosaur_sound(4)  # Hiss

        # LeftBumper
        elif buttons[4]:
            self.get_logger().info(f'LeftBumper was pressed')
            self.PlayMotion("4")
            self.play_dinosaur_sound(5)  # Chomp

        # RightBumper
        elif buttons[5]:
            self.get_logger().info(f'RightBumper was pressed')
            self.PlayMotion("5")
            self.play_dinosaur_sound(6)  # Footstep

        # LeftTrigger
        elif buttons[6]:
            self.get_logger().info(f'LeftTrigger was pressed')
            self.play_dinosaur_sound(7)  # Ground shake

        # RightTrigger
        elif buttons[7]:
            self.get_logger().info(f'RightTrigger was pressed')
            self.play_dinosaur_sound(8)  # Heavy breathing

        # Share
        elif buttons[8]:
            self.get_logger().info(f'Share was pressed')
            """
            self.AssignMotion()
            """

        # Options
        elif buttons[9]:
            self.get_logger().info(f'Options was pressed')
            self.play_dinosaur_sound(9)  # Warning call

        # PS
        elif buttons[10]:
            self.get_logger().info(f'PS was pressed')
            time.sleep(1)
            global IS_RECORDING
            if IS_RECORDING == 0:
                IS_RECORDING = 2
                self.play_dinosaur_sound(10)  # Hunt call (start recording)
            else:
                IS_RECORDING = 0
                json.dump(self.recorded_data, self.record_file, indent=4)
                # Write buffa to record file
                self.record_file.flush()
                self.record_file.close()
                self.start_time = None
                self.record_file = None
                self.recorded_data = []
                # Start selection mode
                self.enter_selection_mode()
                self.play_dinosaur_sound(12)  # Victory roar (end recording)

        # LeftStick
        elif buttons[11]:
            self.get_logger().info(f'LeftStick was pressed')
            self.PlayMotion("11")
            self.play_dinosaur_sound(11)  # Pain sound

        # RightStick
        elif buttons[12]:
            self.get_logger().info(f'RightStick was pressed')
            self.PlayMotion("12")
            self.play_dinosaur_sound(12)  # Victory roar

        # Test
        if MODE == -1:
            #ids = [11, 21, 22, 23, 24, 31, 32, 41, 42, 43, 44]
            #angles = [3000, 3000, 3000, 3000, 3000, 3000, 3000, 3000, 3000, 3000, 3000]
            print(f"{self.motorLimits}")
            ids = 11
            angles = 1024

        # FullMaual
        elif MODE == 0:
            jaw = self.jaw(axes[2])
            blinkRU, blinkRL, blinkLU, blinkLL = self.blink(axes[5])
            eyeR, eyeL = self.eyes(axes[3])
            neck31, neck32, neck33, neck34 = self.neck(axes[0], axes[4], axes[1])
            
            ids = [11, 12, 13, 21, 22, 23, 24, 31, 32, 33, 34]
            angles = [jaw, eyeR, eyeL, blinkRU, blinkRL, blinkLU, blinkLL, neck31, neck32, neck33, neck34]

        return ids, angles

    def enter_selection_mode(self):
        self.selecting = True
        self.file_list = sorted(os.listdir(self.record_dir))
        self.cursor_index = 0
        self.print_selection()
        self.get_logger().info("Enter file selection mode")

    def print_selection(self):
        os.system('clear')
        for i, fname in enumerate(self.file_list):
            prefix = "▶ " if i == self.cursor_index else "  "
            print(f"{prefix}{fname}")

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

        return angleRU, angleRL, angleLU, angleLL

    def jaw(self, angle):
        jaw_min = self.motorLimits["11"]["min"] # open
        jaw_max = self.motorLimits["11"]["max"] # close
        range = jaw_max - jaw_min
        
        current_jaw_position = int(jaw_max - ((angle + 1)/2)*range)
        
        # Calculate jaw opening percentage (0 = closed, 1 = fully open)
        jaw_opening = (jaw_max - current_jaw_position) / range
        
        # Check if jaw opened beyond threshold for roar
        previous_opening = (jaw_max - self.last_jaw_position) / range
        
        if (jaw_opening > self.jaw_roar_threshold and 
            previous_opening <= self.jaw_roar_threshold and
            time.time() - self.last_roar_time > self.roar_cooldown):
            
            # Trigger roar sound when jaw opens wide (randomize roar types)
            import random
            roar_sounds = [1, 2, 3, 4]  # Basic roar, aggressive roar, growl, hiss
            selected_roar = random.choice(roar_sounds)
            self.play_dinosaur_sound(selected_roar)
            self.last_roar_time = time.time()
            self.get_logger().info(f"Jaw roar triggered! Opening: {jaw_opening:.2f}, Sound: {selected_roar}")
        
        self.last_jaw_position = current_jaw_position
        return current_jaw_position

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
        
        # Publish audio command
        audio_msg = Int32()
        audio_msg.data = sound_id
        self.audio_publisher.publish(audio_msg)
        self.get_logger().info(f'Playing dinosaur sound ID: {sound_id}')

def main(args=None):
    rclpy.init(args=args)
    node = SystemController()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()


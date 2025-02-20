#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2024 Ryo Isogawa 　　　　　
# SPDX-License-Identifier: BSD-3-Clause

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Joy
from motor_command_msg.msg import IdAngle
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
            11
        )
    
    def listener_callback(self, msg):
        # Log axes and buttons
        # Axes [0:LeftStick_X, 1:LeftStick_Y, 2:LeftTrigger, 3:RightStick_X, 4:RightStick_Y, 5:RightTrigger]
        # Buttons [0:Cross, 1:Circle, 2:Square, 3:Triangle, 4:LeftBumper, 5:RightBumper, 6:LeftTrigger, 7:RightTrigger, 8:Share, 9:Options, 10:PS, 11:LeftStick, 12:RightStick]
        # Hat/D-pad [X:down-up, Y:left-right]
        #self.get_logger().info(f'Axes: {msg.axes}')
        #self.get_logger().info(f'Buttons: {msg.buttons}')

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
                self.record_file = open(f"/home/csanimatronics/CS_Animatronics/RecordedLog/{filename}", "w")
                self.get_logger().info(f"Start recording {self.start_time}")

            time_passed = time.time() - self.start_time
            self.get_logger().info(f"On recording [{time_passed}]")

        # Save data
            angles_ =[]
            for i, id in enumerate(ids):
                angles_[id] = angle[i]
            dict = {str(motor_id): angle for motor_id, angle in zip(ids, angles)}
            entry = {
                "timestamp": time_passed,
                "angles": angles_,
            }
            self.recorded_data.append(entry)
            print(self.recorded_data)

    def AssignMotion(self):
        # Assign recorded motion to a button
        
        # Show current mapping of controller
        file = open(self.controllerMap, "r")
        data = json.load(file)
        self.get_logger().info(f"Currently motions areassigned like this: {data}")

        selectedButton = input("Select button to assign motion [0:Cross, 1:Circle, 2:Square, 3:Triangle, 4:LeftBumper, 5:RightBumper, 6:LeftTrigger, 7:RightTrigger, 8:Share, 9:Options, 10:PS, 11:LeftStick, 12:RightStick]: ")

        if int(selectedButton) in range(0,12):
            # Search recorded motion files
            fileFounded = os.listdir("/home/csanimatronics/CS_Animatronics/RecordedLog")
            # Chose a file to assign
            fileSelected = input(f"Chose file to assign {fileFounded}: ")
            path = os.path.join("/home/csanimatronics/CS_Animatronics/RecordedLog", fileSelected)
            data[selectedButton] = path
            # path to assign
            file = open("/home/csanimatronics/CS_Animatronics/ControllerMap.json", "w")
            self.get_logger().info(f"{fileFounded}")
            json.dump(data, file, indent=4)
            self.get_logger().info(f"Update: {data}")

    def PlayMotion(self, button):
        self.get_logger().info(f"Start playing recorded motion")
        # Load motion file
        file = open(self.controllerMap, "r")
        data = json.load(file)
        print(data)
        path = data[button]
        print(path)

        # play motion
        try:
            file = open(path, "r")
            data = json.load(file)
        except FileNotFoundError:
            print(f"No motion has assigned to this button")
            return

        timestamps = [entry["timestamp"] for entry in data]
        angles = [entry["angles"] for entry in data]

        # Caluculate time diff
        timediffs = [timestamps[0]]
        for i in range(len(timestamps) - 1):
            timediffs.append(timestamps[i+1] - timestamps[i])
        print(timediffs)
 
        for i, timediff in enumerate(timediffs):
            time.sleep(timediff)
            buttons = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            ids = []
            angles_ = []
            for id in angles:
                ids.append(id)
                angles_.append(angles[id])

            # publish IdAngle
            new_msg = IdAngle()
            new_msg.ids = ids
            new_msg.angles = angles

            self.publisher.publish(new_msg)
            self.get_logger().info(f'Playing recorded motion: {new_msg.ids}, Angles: {new_msg.angles}')


        self.get_logger().info(f"Finish playing recorded moiton") 

    def translate(self, axes, buttons):
        # Buttons event
        # Cross
        if buttons[0]:
            self.get_logger().info(f'Cross was pressed')
            self.PlayMotion("0")

        # Circle
        elif buttons[1]:
            self.get_logger().info(f'Circle was pressed')
            self.PlayMotion("1")

        # Square
        elif buttons[2]:
            self.get_logger().info(f'Square was pressed')
            self.PlayMotion("2")

        # Triangle
        elif buttons[3]:
            self.get_logger().info(f'Triangle was pressed')
            self.PlayMotion("3")

        # LeftBumper
        elif buttons[4]:
            self.get_logger().info(f'LeftBumper was pressed')
            self.PlayMotion("4")

        # RightBumper
        elif buttons[5]:
            self.get_logger().info(f'RightBumper was pressed')
            self.PlayMotion("5")

        # LeftTrigger
        elif buttons[6]:
            self.get_logger().info(f'LeftTrigger was pressed')

        # RightTrigger
        elif buttons[7]:
            self.get_logger().info(f'RightTrigger was pressed')

        # Share
        elif buttons[8]:
            self.get_logger().info(f'Share was pressed')
            self.AssignMotion()

        # Options
        elif buttons[9]:
            self.get_logger().info(f'Options was pressed')

        # PS
        elif buttons[10]:
            self.get_logger().info(f'PS was pressed')
            time.sleep(1)
            global IS_RECORDING
            if IS_RECORDING == 0:
                IS_RECORDING = 2
            else:
                IS_RECORDING = 0
                json.dump(self.recorded_data, self.record_file, indent=4)
                # Write buffa to record file
                self.record_file.flush()
                self.record_file.close()
                self.start_time = None
                self.record_file = None
                self.recorded_data = []

        # LeftStick
        elif buttons[11]:
            self.get_logger().info(f'LeftStick was pressed')
            self.PlayMotion("11")

        # RightStick
        elif buttons[12]:
            self.get_logger().info(f'RightStick was pressed')
            self.PlayMotion("12")

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
            neckX, neckY, neckZ = self.neck(axes[0], axes[4], axes[1])
            
            ids = [11, 21, 22, 23, 24,  31, 32, 43, 44, 41, 42]
            angles = [jaw, neckX, neckY, neckZ, neckY, eyeR, eyeL, blinkRU, blinkRL, blinkLU, blinkLL]

        return ids, angles

    def blink(self, angle):
        blinkRU_min = self.motorLimits["43"]["min"] # close
        blinkRU_max = self.motorLimits["43"]["max"] # open
        rangeRU = blinkRU_max - blinkRU_min
        
        blinkRL_min = self.motorLimits["44"]["min"] # close
        blinkRL_max = self.motorLimits["44"]["max"] # open
        rangeRL = blinkRL_max - blinkRL_min
        
        blinkLU_min = self.motorLimits["41"]["min"] # open
        blinkLU_max = self.motorLimits["41"]["max"] # close
        rangeLU = blinkLU_max - blinkLU_min

        blinkLL_min = self.motorLimits["42"]["min"] # open
        blinkLL_max = self.motorLimits["42"]["max"] # close
        rangeLL = blinkLL_max - blinkLL_min
 
        angleRU = int(self.motorLimits["43"]["ini"] - ((angle+1)/2*rangeRU))
        angleRL = int(self.motorLimits["44"]["ini"] - ((angle+1)/2*rangeRL))
        angleLU = int(self.motorLimits["41"]["ini"] + ((angle+1)/2*rangeLU))
        angleLL = int(self.motorLimits["42"]["ini"] + ((angle+1)/2*rangeLL))
   
        print(f"{self.motorLimits["42"]["ini"]} - {(angle+1)/2} * {rangeLL} = {angleLL}")

        return angleRU, angleRL, angleLU, angleLL

    def jaw(self, angle):
        jaw_min = self.motorLimits["11"]["min"] # open
        jaw_max = self.motorLimits["11"]["max"] # close
        range = jaw_max - jaw_min
        
        angle = int(jaw_max - ((angle + 1)/2)*range)
        return angle

    def eyes(self, angle):
        eyeR_min = self.motorLimits["31"]["min"] # F
        eyeR_max = self.motorLimits["31"]["max"] # R
        rangeR = eyeR_max - eyeR_min

        eyeL_min = self.motorLimits["32"]["min"] # F
        eyeL_max = self.motorLimits["32"]["max"] # R
        rangeL = eyeL_max - eyeL_min

        angleR = int(eyeR_min + (rangeR//2) - (angle/2)*rangeR)
        angleL = int(eyeL_min + (rangeL//2) + (angle/2)*rangeL)
        return angleR, angleL

    def neck(self, x, y, z):
        neckX_min = self.motorLimits["21"]["min"] # R
        neckX_max = self.motorLimits["21"]["max"] # L
        rangeX = neckX_max - neckX_min

        neckY_min = self.motorLimits["22"]["min"]
        neckY_max = self.motorLimits["22"]["max"]
        rangeY = neckY_max - neckY_min

        neckZ_min = self.motorLimits["23"]["min"] # L
        neckZ_max = self.motorLimits["23"]["max"] # R
        rangeZ = neckZ_max - neckZ_min
        
        neckX = int(neckX_min + (rangeX//2) + (x/2)*rangeX)
        neckZ = int(neckZ_min + (rangeZ//2) + (z/2)*rangeZ)
        neckY = int(neckY_min + (rangeY//2) + (y/2)*rangeY)
        return neckX, neckY, neckZ

def main(args=None):
    rclpy.init(args=args)
    node = SystemController()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()


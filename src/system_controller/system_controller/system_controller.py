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
        
        self.start_time = None
        self.recorded_data = []
        self.record_file = None

        self.controllerMap = "/home/csanimatronics/CS_Animatronics/ControllerMap.json"

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
            10
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
        self.record(msg.axes)

        # publish IdAngle
        new_msg = IdAngle()
        new_msg.ids = ids
        new_msg.angles = angles

        self.publisher.publish(new_msg)
        self.get_logger().info(f'Publishing IDs: {new_msg.ids}, Angles: {new_msg.angles}')

    def record(self, axes):
        # Record
        global IS_RECORDING
        if IS_RECORDING != 0:
            # Initialize
            if IS_RECORDING == 2:
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
            entry = {
                "timestamp": time_passed,
                "axes": list(axes),
            }
            self.recorded_data.append(entry)
            print(self.recorded_data)

            #if IS_RECORDING == 0 and self.record_file:
                #json.dump(self.recorded_data, self.record_file, indent=4)
                # Write buffa
                #self.record_file.flush()

    def AssignMotion(self):
        file = open(self.controllerMap, "r")
        data = json.load(file)
        self.get_logger().info(f"Currently motions areassigned like this: {data}")

        selectedButton = input("Select button to assign motion [0:Cross, 1:Circle, 2:Square, 3:Triangle, 4:LeftBumper, 5:RightBumper, 6:LeftTrigger, 7:RightTrigger, 8:Share, 9:Options, 10:PS, 11:LeftStick, 12:RightStick]: ")

        if int(selectedButton) not in range(0,12):
            pass

        else:
            fileFounded = os.listdir("/home/csanimatronics/CS_Animatronics/RecordedLog")
            fileSelected = input(f"Chose file to assign {fileFounded}: ")
            path = os.path.join("/home/csanimatronics/CS_Animatronics/RecordedLog", fileSelected)
            data[selectedButton] = path
            # path to 
            file = open("/home/csanimatronics/CS_Animatronics/ControllerMap.json", "w")
            self.get_logger().info(f"{fileFounded}")
            json.dump(data, file, indent=4)
            self.get_logger().info(f"Update: {data}")

    def PlayMotion(self, button):
        self.get_logger().info(f"Start playing recorded motion")
        # load motion file
        file = open(self.controllerMap, "r")
        data = json.load(file)
        print(data)
        path = data[button]
        print(path)

        # play motion
        file = open(path, "r")
        data = json.load(file)

        timestamps = [entry["timestamp"] for entry in data]
        axes = [entry["axes"] for entry in data]

        # Caluculate time diff
        timediffs = [timestamps[0]]
        for i in range(len(timestamps) - 1):
            timediffs.append(timestamps[i+1] - timestamps[i])
        print(timediffs)
 
        for i, timediff in enumerate(timediffs):
            time.sleep(timediff)
            buttons = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            ids, angles = self.translate(axes[i], buttons)

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
 

        # RightBumper
        elif buttons[5]:
            self.get_logger().info(f'RightBumper was pressed')

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
                # Write buffa
                self.record_file.flush()
                self.record_file.close()
                self.start_time = None
                self.record_file = None
                self.recorded_data = []

        # LeftStick
        elif buttons[11]:
            self.get_logger().info(f'LeftStick was pressed')

        # RightStick
        elif buttons[12]:
            self.get_logger().info(f'RightStick was pressed')

        # Test
        if MODE == -1:
            ids = [11, 21, 22, 23, 31, 32, 41, 42, 43, 44]
            angles = [3000, 3000, 3000, 3000, 3000, 3000, 3000, 3000, 3000, 3000]
            ids = 31
            angles = 3000

        # FullMaual
        elif MODE == 0:
            jaw = self.jaw(axes[2])
            blinkRU, blinkRL, blinkLU, blinkLL = self.blink(axes[5])
            eyeR, eyeL = self.eyes(axes[3])
            neckX, neckY, neckZ = self.neck(axes[0], axes[4], axes[1])
            
            ids = [11, 21, 22, 23, 31, 32, 41, 42, 43, 44]
            angles = [jaw, neckX, neckY, neckZ, eyeR, eyeL, blinkRU, blinkRL, blinkLU, blinkLL]

        return ids, angles

    def blink(self, angle):
        blinkRU_min = -30 *(4095//360) # close
        blinkRU_max = 40 *(4095//360) # open
        rangeRU = blinkRU_max - blinkRU_min
        
        blinkRL_min = 145 *(4095//360) # close
        blinkRL_max = 180 *(4095//360) # open
        rangeRL = blinkRL_max - blinkRL_min
        
        blinkLU_min = 320 *(4095//360) # open
        blinkLU_max = 400 *(4095//360) # close
        rangeLU = blinkLU_max - blinkLU_min

        blinkLL_min = 170 *(4095//360) # open
        blinkLL_max = 200 *(4095//360) # close
        rangeLL = blinkLL_max - blinkLL_min
 
        angleRU = int(blinkRU_max - ((angle + 1)/2)*rangeRU)
        angleRL = int(blinkRL_max - ((angle + 1)/2)*rangeRL)
        angleLU = int(blinkLU_min + ((angle + 1)/2)*rangeLU)
        angleLL = int(blinkLL_min + ((angle + 1)/2)*rangeLL)
        return angleRU, angleRL, angleLU, angleLL

    def jaw(self, angle):
        jaw_min = 15 *(4095//360) # open
        jaw_max = 90 *(4095//360) # close
        range = jaw_max - jaw_min
        
        angle = int(jaw_max - ((angle + 1)/2)*range)
        return angle

    def eyes(self, angle):
        eyeR_min = 70 *(4095//360) # F
        eyeR_max = 150 *(4095//360) # R
        rangeR = eyeR_max - eyeR_min

        eyeL_min = 200 *(4095//360) # F
        eyeL_max = 300 *(4095//360) # R
        rangeL = eyeL_max - eyeL_min

        angleR = int(eyeR_min + (rangeR//2) - (angle/2)*rangeR)
        angleL = int(eyeL_min + (rangeL//2) + (angle/2)*rangeL)
        return angleR, angleL

    def neck(self, x, y, z):
        neckX_min = 300 *(4095//360) # R
        neckX_max = 420 *(4095//360) # L
        rangeX = neckX_max - neckX_min

        #neckY_min = 160 *(4095//360)
        #neckY_max = 200 *(4095//360)
        #rangeY = neckY_max - neckY_min

        neckZ_min = 154 *(4095//360) # L
        neckZ_max = 206 *(4095//360) # R
        rangeZ = neckZ_max - neckZ_min
        
        neckX = int(neckX_min + (rangeX//2) + (x/2)*rangeX)
        neckZ = int(neckZ_min + (rangeZ//2) + (z/2)*rangeZ)
        neckY = 140 *(4095//360)
        return neckX, neckY, neckZ

def main(args=None):
    rclpy.init(args=args)
    node = SystemController()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()


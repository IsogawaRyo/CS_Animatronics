#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2024 Ryo Isogawa 　　　　　
# SPDX-License-Identifier: BSD-3-Clause

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Joy
from motor_command_msg.msg import IdAngle
#import numpy as np

# Operation Mode
# -1: Test
# 0: FullManual
# 2: Assist
MODE = 0

class SystemController(Node):
    def __init__(self):
        super().__init__('system_controller')
        self.get_logger().info('Run system controller node')
        
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
 
        # publish IdAngle
        new_msg = IdAngle()
        new_msg.ids = ids
        new_msg.angles = angles

        self.publisher.publish(new_msg)
        self.get_logger().info(f'Publishing IDs: {new_msg.ids}, Angles: {new_msg.angles}')

    def translate(self, axes, buttons):
        # Buttons event
        # Cross
        if buttons[0]:
            self.get_logger().info(f'Cross was pressed')

        # Circle
        elif buttons[1]:
            self.get_logger().info(f'Circle was pressed')

        # Square
        elif buttons[2]:
            self.get_logger().info(f'Square was pressed')

        # Triangle
        elif buttons[3]:
            self.get_logger().info(f'Triangle was pressed')

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

        # Options
        elif buttons[9]:
            self.get_logger().info(f'Options was pressed')

        # PS
        elif buttons[10]:
            self.get_logger().info(f'PS was pressed')

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
        
        blinkLU_min = -35 *(4095//360) # open
        blinkLU_max = 40 *(4095//360) # close
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
        neckX_min = -60 *(4095//360) # R
        neckX_max = 60 *(4095//360) # L
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
        
    def checkRange(angle, max, min):
        pass

def main(args=None):
    rclpy.init(args=args)
    node = SystemController()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()


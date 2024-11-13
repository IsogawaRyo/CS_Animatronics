#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2024 Ryo Isogawa 　　　　　
# SPDX-License-Identifier: BSD-3-Clause

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Joy
from motor_command_msg.msg import IdAngle
import math

# Operation Mode
# -1: Test
# 0: InitialPosition
# 1: FullManual
# 2: Assist
MODE = 1

class SystemController(Node):
    def __init__(self):
        super().__init__('system_controller')

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
        self.get_logger().info(f'Axes: {msg.axes}')
        self.get_logger().info(f'Buttons: {msg.buttons}')

        # translate values
        ids, angles = self.translate(msg.axes, msg.buttons)
 
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
            ids = [31, 32, 41, 42, 43, 44]
            angles = [3000, 3000, 3000, 3000, 3000, 3000]

        # Initialize
        elif MODE == 0:
            ids = [31, 32, 41, 42, 43, 44]
            angles = [0, 0, 0, 0, 0, 0]

        # FullMaual
        elif MODE == 1:
            angle = math.floor((0.5*(axes[0] + 1))*4095)

            jaw = self.jaw(axes[2])
            blinkU, blinkL = self.blink(axes[5])
            
            ids = [31, 32, 41, 42, 43, 44]
            angles = [jaw, blinkU, blinkL, blinkU, blinkL, angle]

        return ids, angles

    def blink(self, angle):
        blinkU_min = 0
        blinkU_max = 4095
        rangeU = blinkU_max - blinkU_min

        blinkL_min = 0
        blinkL_max = 4095
        rangeL = blinkL_max - blinkL_min
        
        angleU = math.floor((0.5*(angle + 1))*rangeU)
        angleL = math.floor((0.5*(angle + 1))*rangeL)
        return angleU, angleL

    def jaw(self, angle):
        jaw_min = 0
        jaw_max = 4095
        range = jaw_max - jaw_min
        
        angle = math.floor((0.5*(angle + 1))*range)
        return angle

    def eyes(self):
        pass

    def neck(self):
        pass

def main(args=None):
    rclpy.init(args=args)
    node = SystemController()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()


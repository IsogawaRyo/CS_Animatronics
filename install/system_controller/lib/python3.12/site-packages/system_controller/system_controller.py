#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2024 Ryo Isogawa 　　　　　
# SPDX-License-Identifier: BSD-3-Clause

# Operation Mode
# 0: InitialPosition
# 1: Full Manual
# 2: Assist
MODE = 0

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Joy
from motor_command_msg.msg import IdAngle

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
            'output_topic',
            10
        )

    def listener_callback(self, msg):
        # Log the axes and buttons
        # Axes [0:LeftStick_X, 1:LeftStick_Y, 2:LeftTrigger, 3:RightStick_X, 4:RightStick_Y, 5:RightTrigger]
        # Buttons [0:Cross, 1:Circle, 2:Square, 3:Triangle, 4:LeftBumper, 5:RightBumper, 6:LeftTrigger, 7:RightTrigger, 8:Share, 9:Options, 10:PS, 11:LeftStick, 12:RightStick]
        # Hat/D-pad [X:down-up, Y:left-right]
        self.get_logger().info(f'Axes: {msg.axes}')
        self.get_logger().info(f'Buttons: {msg.buttons}')
       
        ###############################
        ids, angles = self.translate(msg.axes, msg.buttons)
 
        new_msg = IdAngle()
        new_msg.ids = ids
        new_msg.angles = angles

        self.publisher.publish(new_msg)
        self.get_logger().info(f'Publishing IDs: {new_msg.ids}, Angles: {new_msg.angles}')

    def translate(self, axes, buttons):
        if MODE == 0:
            ids = [0, 0]
            angles = [100, 100]

        return ids, angles

    def blink(self):
        pass

    def jaw(self):
        pass

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


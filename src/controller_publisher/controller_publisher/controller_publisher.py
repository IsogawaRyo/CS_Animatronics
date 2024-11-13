#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2024 Ryo Isogawa 　　　　　
# SPDX-License-Identifier: BSD-3-Claus

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Joy
import pygame

class ControllerPublisher(Node):
    def __init__(self):
        super().__init__('controller_publisher')
        self.publisher_ = self.create_publisher(Joy, 'controller_input', 10)
        self.timer = self.create_timer(0.05, self.timer_callback)
        pygame.init()
        pygame.joystick.init()

        # check connections 
        if pygame.joystick.get_count() == 0:
            self.get_logger().error('No joystick detected. Please connect a PS5 controller.')
            exit()

        self.controller = pygame.joystick.Joystick(0)
        self.controller.init()
        self.get_logger().info('PS5 controller initialized')

    def timer_callback(self):
        pygame.event.pump()
        msg = Joy()

        # Joy Axes(RStickx, RSticky, RTriger, LStickx, ,LSticky, LTriger)
        axes = []
        for i in range(self.controller.get_numaxes()):
            axes.append(self.controller.get_axis(i))
        msg.axes = axes

        # Buttons(circle, cross, square, triangle,...)
        buttons = []
        for i in range(self.controller.get_numbuttons()):
            buttons.append(self.controller.get_button(i))
        msg.buttons = buttons

        # Publish message
        self.publisher_.publish(msg)
        self.get_logger().info('Published controller state')

def main(args=None):
    rclpy.init(args=args)
    node = ControllerPublisher()
    rclpy.spin(node)
    
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()


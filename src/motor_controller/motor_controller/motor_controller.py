#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2024 Ryo Isogawa 　　　　　
# SPDX-License-Identifier: BSD-3-Claus

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Joy
from motor_command_msg.msg import IdAngle
from dynamixel_sdk import *
from dynamixel_sdk_custom_interfaces.msg import SetPosition
from dynamixel_sdk_custom_interfaces.srv import GetPosition


PROTOCOL_VERSION = 2.0
DEVICE_NAME = '/dev/ttyUSB0'

port_handler = PortHandler(DEVICE_NAME)
packet_handler = PacketHandler(PROTOCOL_VERSION)

class MotorController(Node):
    def __init__(self):
        super().__init__('motor_controller')
        self.get_logger().info('Run motor controller node')

        # Setting subscriber
        self.subscription = self.create_subscription(
            IdAngle,
            'IdAngle',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning  

        # Subscription set position
        self.set_position_subscriber_ = self.create_publisher(
            SetPosition,
            'set_position',
            10)

        # Service get position
        self.get_position_server_ = self.create_service(
            GetPosition,
            'get_position',
            self.get_position_callback)

    def listener_callback(self, msg):
        self.get_logger().info(f'Ids: {msg.ids}')
        self.get_logger().info(f'Angles: {msg.angles}')
        
        # publish SetPosition for each id
        i = 0 
        for id in msg.ids:
            angle = msg.angles[i]
        
            new_msg = SetPosition()
            new_msg.id = int(id)
            new_msg.position = int(angle)

            self.set_position_subscriber_.publish(new_msg)
            self.get_logger().info(f'Publishing IDs: {new_msg.id}, Angles: {new_msg.position}')
            i = i + 1

    def get_position_callback(self, request, response):
        ####### Example ######
        response.position = 0
        self.get_logger().info(f'Responding with position: {response.position}')
        return response

def main(args=None):
    rclpy.init(args=args)
    node = MotorController()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()

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

# Control table address for X series (except XL-320)
ADDR_OPERATING_MODE = 11
ADDR_TORQUE_ENABLE = 64
ADDR_GOAL_POSITION = 116
ADDR_PRESENT_POSITION = 132

# Protocol version
PROTOCOL_VERSION = 2.0  # Default Protocol version of DYNAMIXEL X series.

# Default setting
BAUDRATE = 57600  # Default Baudrate of DYNAMIXEL X series
DEVICE_NAME = "/dev/ttyUSB0"  # [Linux]: "/dev/ttyUSB*", [Windows]: "COM*"

# Initialize PortHandler instance
port_handler = PortHandler(DEVICE_NAME)

# Initialize PacketHandler instance (specify protocol version)
packet_handler = PacketHandler(PROTOCOL_VERSION)

# Define variables
dxl_error = 0  # Equivalent to uint8_t for error checking
goal_position = 0  # Equivalent to uint32_t for goal position
dxl_comm_result = COMM_TX_FAIL  # Initialize with COMM_TX_FAIL status

class MotorController(Node):
    def __init__(self):
        super().__init__('motor_controller')
        self.get_logger().info('Run motor controller node')

        # Declare and initialize the parameter with a default value
        self.declare_parameter('qos_depth', 10)
        
        # Retrieve the parameter's value
        qos_depth = self.get_parameter('qos_depth').get_parameter_value().integer_value

        # Now you can use qos_depth as an int
        self.get_logger().info(f'QoS Depth: {qos_depth}')

        # QoS
        qos_profile = QoSProfile(
            depth=qos_depth,
            reliability=ReliabilityPolicy.RELIABLE,
            durability=DurabilityPolicy.VOLATILE
        )
        
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

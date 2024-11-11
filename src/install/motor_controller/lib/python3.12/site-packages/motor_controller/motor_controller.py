#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2024 Ryo Isogawa 　　　　　
# SPDX-License-Identifier: BSD-3-Claus

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Joy
from motor_command_msg.msg import IdAngle
from dynamixel_sdk import *  # Uses Dynamixel SDK library
from dynamixel_sdk_custom_interfaces.msg import SetPosition
from dynamixel_sdk_custom_interfaces.srv import GetPosition

ADDR_OPERATING_MODE = 11
ADDR_TORQUE_ENABLE = 64
ADDR_GOAL_POSITION = 116
ADDR_PRESENT_POSITION = 132

PROTOCOL_VERSION = 2.0

BAUDRATE = 57600
DEVICE_NAME = '/dev/ttyUSB0'

class MotorController(Node):
    def __init__(self):
        super().__init__('motor_controller')
        self.get_logger().info('Run motor controller node')

        # Setting for subscriber
        self.subscription = self.create_subscription(
            Joy,
            'controller_input',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning  

        self.declare_parameter('qos_depth', 10)
        qos_depth = self.get_parameter('qos_depth').get_parameter_value().integer_value

        qos_rkl10v = rclpy.qos.QoSProfile(depth=qos_depth, reliability=rclpy.qos.QoSReliabilityPolicy.RELIABLE, durability=rclpy.qos.QoSDurabilityPolicy.VOLATILE)

        self.port_handler = PortHandler(DEVICE_NAME)
        self.packet_handler = PacketHandler(PROTOCOL_VERSION)

        # Open Serial Port
        if not self.port_handler.openPort():
            self.get_logger().error('Failed to open the port!')
            raise RuntimeError('Failed to open the port!')
        else:
            self.get_logger().info('Succeeded to open the port.')

        # Set the baudrate of the serial port (use DYNAMIXEL Baudrate)
        if not self.port_handler.setBaudRate(BAUDRATE):
            self.get_logger().error('Failed to set the baudrate!')
            raise RuntimeError('Failed to set the baudrate!')
        else:
            self.get_logger().info('Succeeded to set the baudrate.')

        self.setup_dynamixel(BROADCAST_ID)

        # Subscription to set position
        self.set_position_subscriber_ = self.create_subscription(
            SetPosition,
            'set_position',
            self.set_position_callback,
            qos_rkl10v
        )

        # Service to get position
        self.get_position_server_ = self.create_service(
            GetPosition,
            'get_position',
            self.get_present_position_callback
        )

    def setup_dynamixel(self, dxl_id):
        # Use Position Control Mode
        dxl_comm_result, dxl_error = self.packet_handler.write1ByteTxRx(
            self.port_handler, dxl_id, ADDR_OPERATING_MODE, 3
        )

        if dxl_comm_result != COMM_SUCCESS:
            self.get_logger().error('Failed to set Position Control Mode.')
        else:
            self.get_logger().info('Succeeded to set Position Control Mode.')

        # Enable Torque of DYNAMIXEL
        dxl_comm_result, dxl_error = self.packet_handler.write1ByteTxRx(
            self.port_handler, dxl_id, ADDR_TORQUE_ENABLE, 1
        )

        if dxl_comm_result != COMM_SUCCESS:
            self.get_logger().error('Failed to enable torque.')
        else:
            self.get_logger().info('Succeeded to enable torque.')

    def set_position_callback(self, msg):
        goal_position = int(msg.position)  # Convert int32 -> uint32

        # Write Goal Position (length : 4 bytes)
        dxl_comm_result, dxl_error = self.packet_handler.write4ByteTxRx(
            self.port_handler, msg.id, ADDR_GOAL_POSITION, goal_position
        )

        if dxl_comm_result != COMM_SUCCESS:
            self.get_logger().info(self.packet_handler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            self.get_logger().info(self.packet_handler.getRxPacketError(dxl_error))
        else:
            self.get_logger().info(f'Set [ID: {msg.id}] [Goal Position: {msg.position}]')

    def get_present_position_callback(self, request, response):
        # Read Present Position (length : 4 bytes) and Convert uint32 -> int32
        present_position, dxl_comm_result, dxl_error = self.packet_handler.read4ByteTxRx(
            self.port_handler, request.id, ADDR_PRESENT_POSITION
        )

        if dxl_comm_result != COMM_SUCCESS:
            self.get_logger().error('Failed to read position.')
        else:
            self.get_logger().info(f'Get [ID: {request.id}] [Present Position: {present_position}]')

        response.position = present_position
        return response

    def __del__(self):
        # Disable Torque of DYNAMIXEL
        self.packet_handler.write1ByteTxRx(
            self.port_handler, BROADCAST_ID, ADDR_TORQUE_ENABLE, 0
        )
        self.port_handler.closePort()

def main(args=None):
    rclpy.init(args=args)
    motor_controller = MotorController()
    try:
        rclpy.spin(motor_controller)
    except KeyboardInterrupt:
        pass
    finally:
        motor_controller.destroy_node()
        rclpy.shutdown()

if __name__ == "__main__":
    main()

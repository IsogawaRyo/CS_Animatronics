#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2024 Ryo Isogawa 　　　　　
# SPDX-License-Identifier: BSD-3-Claus

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, DurabilityPolicy
from sensor_msgs.msg import Joy
from motor_command_msg.msg import IdAngle
from dynamixel_sdk import *
from dynamixel_sdk_custom_interfaces.msg import SetPosition
from dynamixel_sdk_custom_interfaces.srv import GetPosition
import numpy as np
from time import sleep

# Control table address
ADDR_OPERATING_MODE = 11
ADDR_TORQUE_ENABLE = 64
ADDR_LED = 65
ADDR_GOAL_POSITION = 116
ADDR_PRESENT_POSITION = 132

# Protocol version
PROTOCOL_VERSION = 2.0 

# Default setting
BAUDRATE = 57600 
DEVICE_NAME0 = "/dev/ttyUSB0"
DEVICE_NAME1 = "/dev/ttyUSB1"

# Initialize PortHandler
port_handler0 = PortHandler(DEVICE_NAME0)
port_handler1 = PortHandler(DEVICE_NAME1)

# Initialize PacketHandler
packet_handler = PacketHandler(PROTOCOL_VERSION)

# Define variables
dxl_error = 0 
goal_position = 0  
dxl_comm_result = COMM_TX_FAIL  

class MotorController(Node):
    def __init__(self):
        super().__init__('motor_controller')
        self.get_logger().info('Run motor controller node')

        # Setting GetPosition service
        self.get_position_server_ = self.create_service(
            GetPosition, 
            'get_position', 
            self.get_present_position)
        
        # Setting subscriber
        self.subscription = self.create_subscription(
            IdAngle,
            'IdAngle',
            self.listener_callback,
            10)
        self.subscription

    def listener_callback(self, msg):
        self.get_logger().info(f'Ids: {msg.ids}')
        self.get_logger().info(f'Angles: {msg.angles}')
        
        # publish SetPosition for each id
        i = 0 
        for id in msg.ids:
            angle = msg.angles[i]

            if id in [31, 32, 41, 42, 43, 44]:  # Port1
                selected_port_handler = port_handler0
            elif id in [11, 21, 22, 23]:  # Port2
                selected_port_handler = port_handler1
            else:
                self.get_logger().info(f"Unknown ID: {id}")
                continue
            
            goal_position = int(angle) 
            dxl_comm_result, dxl_error = packet_handler.write4ByteTxRx(selected_port_handler, id, ADDR_GOAL_POSITION, goal_position)

            if dxl_comm_result != COMM_SUCCESS:
                self.get_logger().info(f"Communication error: {packet_handler.getTxRxResult(dxl_comm_result)}")
            elif dxl_error != 0:
                self.get_logger().info(f"Error: {packet_handler.getRxPacketError(dxl_error)}")
            else:
                #self.get_logger().info(f"Set [ID: {id}] [Goal Position: {goal_position}]")
                pass
    
            i = i + 1
            sleep(0.00000001) # delay to solve time-out issue (0.01 us)

    def get_present_position(self, request, response):
        present_position, dxl_error = packet_handler.read4ByteTxRx(port_handler, request.id, ADDR_PRESENT_POSITION)
        
        if dxl_comm_result != COMM_SUCCESS:
            self.get_logger().info(f"Communication error: {packet_handler.getTxRxResult(dxl_comm_result)}")
        elif dxl_error != 0:
            self.get_logger().info(f"Error: {packet_handler.getRxPacketError(dxl_error)}")
        else:
            self.get_logger().info(f"Get [ID: {request.id}] [Present Position: {present_position}]")
        
        response.position = present_position
        return response

def main(args=None):
    # Open Serial Port
    if not port_handler0.openPort():
        print("Failed to open the port0")
        return
    if not port_handler1.openPort():
        print("Failed to open the port1")
        return
    print("Succeeded to open the port")
    
    # Set Baudrate
    if not port_handler0.setBaudRate(BAUDRATE):
        print("Failed to set the baudrate")
        return
    if not port_handler1.setBaudRate(BAUDRATE):
        print("Failed to set the baudrate")
        return
    print("Succeeded to open the port")

    # initialize each id
    for id in np.array([11, 21, 22, 23, 31, 32, 41, 42, 43, 44], dtype=np.uint8):
        if id in [31, 32, 41, 42, 43, 44]:  # Port1
            selected_port_handler = port_handler0
        elif id in [11, 21, 22, 23]:  # Port2
            selected_port_handler = port_handler1
        else:
            self.get_logger().info(f"Unknown ID: {id}")
            continue
        
        # Set Position Control Mode
        dxl_comm_result, dxl_error = packet_handler.write1ByteTxRx(selected_port_handler, id, ADDR_OPERATING_MODE, 4)
        if dxl_comm_result != COMM_SUCCESS:
            print("Failed to set Position Control Mode")
        else:
            packet_handler.write1ByteTxRx(selected_port_handler, id, ADDR_LED, 1)
            print("Succeeded to set Position Control Mode")
        
        # Enable Torque
        dxl_comm_result, dxl_error = packet_handler.write1ByteTxRx(selected_port_handler, id, ADDR_TORQUE_ENABLE, 1)
        if dxl_comm_result != COMM_SUCCESS:
            print("Failed to enable torque")
        else:
            print("Succeeded to enable torque")
    
    rclpy.init(args=args)
    node = MotorController()
    rclpy.spin(node)

    for id in np.array([11, 21, 22, 23, 31, 32, 41, 42, 43, 44], dtype=np.uint8):
        if id in [31, 32, 41, 42, 43, 44]:  # Port1
            selected_port_handler = port_handler0
        elif id in [11, 21, 22, 23]:  # Port2
            selected_port_handler = port_handler1
        else:
            self.get_logger().info(f"Unknown ID: {id}")
            continue
        
        packet_handler.write1ByteTxRx(selected_port_handler, id, ADDR_TORQUE_ENABLE, 0)  # Disable torque
        packet_handler.write1ByteTxRx(selected_port_handler, id, ADDR_LED, 0)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()

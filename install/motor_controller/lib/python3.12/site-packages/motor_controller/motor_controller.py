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
ADDR_PROFILE_VELOCITY = 112
ADDR_PROFILE_ACCELERATION = 108
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

LEN_GOAL_POSITION = 4
groupSyncWrite0 = GroupSyncWrite(port_handler0, packet_handler, ADDR_GOAL_POSITION, LEN_GOAL_POSITION)
groupSyncWrite1 = GroupSyncWrite(port_handler1, packet_handler, ADDR_GOAL_POSITION, LEN_GOAL_POSITION)

INITIAL_POSITIONS = [1024, 0, 2048, 1593, 1251, 2844, -341, 1706, 455, 2389]

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
        
        groupSyncWrite0.clearParam()
        groupSyncWrite1.clearParam()
        
        for i, id in enumerate(msg.ids):
            angle = int(msg.angles[i])
            
            # Preparation
            param_goal_position = [
                DXL_LOBYTE(DXL_LOWORD(angle)),
                DXL_HIBYTE(DXL_LOWORD(angle)),
                DXL_LOBYTE(DXL_HIWORD(angle)),
                DXL_HIBYTE(DXL_HIWORD(angle))
            ]
            
            # Assigning
            if id in [31, 32, 41, 42, 43, 44]:
                if not groupSyncWrite0.addParam(id, param_goal_position):
                    self.get_logger().error(f"Failed to addParam for ID: {id} on port_handler0")
            elif id in [11, 21, 22, 23]:
                if not groupSyncWrite1.addParam(id, param_goal_position):
                    self.get_logger().error(f"Failed to addParam for ID: {id} on port_handler1")
            else:
                self.get_logger().info(f"Unknown ID: {id}")
                continue
        
        # Send Sync Write
        dxl_comm_result0 = groupSyncWrite0.txPacket()
        if dxl_comm_result0 != COMM_SUCCESS:
            self.get_logger().error(f"Sync Write Error on port_handler0: {packet_handler.getTxRxResult(dxl_comm_result0)}")
        
        dxl_comm_result1 = groupSyncWrite1.txPacket()
        if dxl_comm_result1 != COMM_SUCCESS:
            self.get_logger().error(f"Sync Write Error on port_handler1: {packet_handler.getTxRxResult(dxl_comm_result1)}")
        
        # Clear parameter
        groupSyncWrite0.clearParam()
        groupSyncWrite1.clearParam()

    def get_present_position(self, request, response):
        pass

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
    i = 0
    for id in np.array([11, 21, 22, 23, 31, 32, 41, 42, 43, 44], dtype=np.uint8):
        if id in [31, 32, 41, 42, 43, 44]:  # Port1
            selected_port_handler = port_handler0
        elif id in [11, 21, 22, 23]:  # Port2
            selected_port_handler = port_handler1
        else:
            self.get_logger().info(f"Unknown ID: {id}")
            continue
        print(id)
        
        # Set Position Control Mode
        dxl_comm_result, dxl_error = packet_handler.write1ByteTxRx(selected_port_handler, id, ADDR_OPERATING_MODE, 4)
        if dxl_comm_result != COMM_SUCCESS:
            print("Failed to set Position Control Mode")
        else:
            print("Succeeded to set Position Control Mode")

        
        # Set Velocity
        dxl_comm_result, dxl_error = packet_handler.write1ByteTxRx(selected_port_handler, id, ADDR_PROFILE_VELOCITY, 50)
        if dxl_comm_result != COMM_SUCCESS:
            print("Failed to set Maximum Velocity")
        else:
            print("Succeeded to set Maximum Velocity")


        # Set Acceleration
        dxl_comm_result, dxl_error = packet_handler.write1ByteTxRx(selected_port_handler, id, ADDR_PROFILE_ACCELERATION, 50)
        if dxl_comm_result != COMM_SUCCESS:
            print("Failed to set Maximum Acceleration")
        else:
            print("Succeeded to set Maximum Acceleration")


        # Set Initial Position
        dxl_comm_result, dxl_error = packet_handler.write4ByteTxRx(selected_port_handler, id, ADDR_GOAL_POSITION, INITIAL_POSITIONS[i])
        if dxl_comm_result != COMM_SUCCESS:
            print("Failed to set Initial Position")
        else:
            print("Succeeded to set Initial Position")

        # Enable Torque
        dxl_comm_result, dxl_error = packet_handler.write1ByteTxRx(selected_port_handler, id, ADDR_TORQUE_ENABLE, 1)
        if dxl_comm_result != COMM_SUCCESS:
            print("Failed to enable torque")
        else:
            packet_handler.write1ByteTxRx(selected_port_handler, id, ADDR_LED, 1)
            print("Succeeded to enable torque")

        i = i + 1
    
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

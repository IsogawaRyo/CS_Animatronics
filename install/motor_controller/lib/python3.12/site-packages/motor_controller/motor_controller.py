#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2024 Ryo Isogawa 　　　　　
# SPDX-License-Identifier: BSD-3-Clause

import rclpy
from rclpy.node import Node
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
ADDR_MIN = 52
ADDR_MAX = 48

# Protocol version
PROTOCOL_VERSION = 2.0 

# Default setting
BAUDRATE = 57600 
DEVICE_NAME0 = "/dev/ttyUSB0"
DEVICE_NAME1 = "/dev/ttyUSB1"

# Initialize PortHandler
port_handler0 = PortHandler(DEVICE_NAME0)
port_handler1 = PortHandler(DEVICE_NAME1)

# Initialize list ofmotor on each port
PORT0 = []
PORT1 = []

# Initialize PacketHandler
packet_handler = PacketHandler(PROTOCOL_VERSION)

# Define variables
dxl_error = 0 
goal_position = 0  
dxl_comm_result = COMM_TX_FAIL  

LEN_GOAL_POSITION = 4
groupSyncWrite0 = GroupSyncWrite(port_handler0, packet_handler, ADDR_GOAL_POSITION, LEN_GOAL_POSITION)
groupSyncWrite1 = GroupSyncWrite(port_handler1, packet_handler, ADDR_GOAL_POSITION, LEN_GOAL_POSITION)

MOTOR_LIMITS = {
    11: {"ini": 1024, "min": 171,  "max": 1023},
    21: {"ini": 0,    "min": -682, "max": 682},
    22: {"ini": 1592, "min": 1500, "max": 1650},
    23: {"ini": 1593, "min": 1751, "max": 2343},
    24: {"ini": 1592, "min": 1500, "max": 1650},
    31: {"ini": 1251, "min": 910,  "max": 1592},
    32: {"ini": 2844, "min": 2502, "max": 3185},
    41: {"ini": -341, "min": -341, "max": 341},
    42: {"ini": 1706,  "min": 1706, "max": 1990},
    43: {"ini": 455,  "min": 3640, "max": 4550},
    44: {"ini": 2388, "min": 2047,  "max": 2388}
}

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
        # Check Limits
            angle = int(msg.angles[i])
            if angle <= MOTOR_LIMITS[id]["min"]:
                angleP = angle
                angle = MOTOR_LIMITS[id]["min"]
                self.get_logger().error(f"Exceed minimum motor {id}: {angleP} => {angle}")

            elif angle >= MOTOR_LIMITS[id]["max"]:
                angleP = angle
                angle = MOTOR_LIMITS[id]["max"]
                self.get_logger().error(f"Exceed maximum motor {id}: {angleP} => {angle}")
            self.get_logger().info(f"{id}: {angle}")

            # Preparation
            param_goal_position = [
                DXL_LOBYTE(DXL_LOWORD(angle)),
                DXL_HIBYTE(DXL_LOWORD(angle)),
                DXL_LOBYTE(DXL_HIWORD(angle)),
                DXL_HIBYTE(DXL_HIWORD(angle))
            ]
            
            # Assigning
            if id in PORT0:
                if not groupSyncWrite0.addParam(id, param_goal_position):
                    self.get_logger().error(f"Failed to addParam for ID: {id}")
            elif id in PORT1:
                if not groupSyncWrite1.addParam(id, param_goal_position):
                    self.get_logger().error(f"Failed to addParam for ID: {id}")
            else:
                self.get_logger().info(f"Unknown ID: {id}")
                continue
        
        # Send Sync Write
        dxl_comm_result = groupSyncWrite0.txPacket()
        if dxl_comm_result != COMM_SUCCESS:
            self.get_logger().error(f"Sync Write Error: {packet_handler.getTxRxResult(dxl_comm_result)}")
        
        dxl_comm_result = groupSyncWrite1.txPacket()
        if dxl_comm_result != COMM_SUCCESS:
            self.get_logger().error(f"Sync Write Error: {packet_handler.getTxRxResult(dxl_comm_result)}")
        
        # Clear parameter
        groupSyncWrite0.clearParam()
        groupSyncWrite1.clearParam()

    def get_present_position(self, request, response):
        positions = []
        ids = []

        # Get position of motors on PORT0
        for id in PORT0:
            position, dxl_comm_result, dxl_error = self.packet_handler.read4ByteTxRx(port_handler0, id, ADDR_PRESENT_POSITION)
            if dxl_comm_result == COMM_SUCCESS:
                positions.append(position)
                ids.append(id)
                self.get_logger().info(f"ID {id}: {position}")
            else:
                self.get_logger().error(f"ID {id} Failed: {self.packet_handler.getTxRxResult(dxl_comm_result)}")

        # Get position of motors on PORT1
        for id in PORT1:
            position, dxl_comm_result, dxl_error = self.packet_handler.read4ByteTxRx(port_handler1, id, ADDR_PRESENT_POSITION)
            if dxl_comm_result == COMM_SUCCESS:
                positions.append(position)
                ids.append(id)
                self.get_logger().info(f"ID {id}: {position}")
            else:
                self.get_logger().error(f"ID {id} Failed: {self.packet_handler.getTxRxResult(dxl_comm_result)}")

        # Prepare data
        response.header = Header()
        response.header.stamp = self.get_clock().now().to_msg()
        response.ids = ids
        response.positions = positions

        self.get_logger().info(f"Get current positions")
        return response


def set_motor1(port_handler, id, addr, num):
    port_handler.clearPort()
    sleep(0.1)
    dxl_comm_result, dxl_error = packet_handler.write1ByteTxRx(port_handler, id, addr, num)
    if dxl_comm_result != COMM_SUCCESS:
        print(f"Failed: {packet_handler.getTxRxResult(dxl_comm_result)}")
    else:
        print(f"Succeeded: {packet_handler.getTxRxResult(dxl_comm_result)}")

def set_motor4(port_handler, id, addr, num):
    port_handler.clearPort()
    sleep(0.1)
    dxl_comm_result, dxl_error = packet_handler.write4ByteTxRx(port_handler, id, addr, num)
    if dxl_comm_result != COMM_SUCCESS:
        print(f"Failed: {packet_handler.getTxRxResult(dxl_comm_result)}")
    else:
        print(f"Succeeded: {packet_handler.getTxRxResult(dxl_comm_result)}")

def ping(port_handler, id):
    port_handler.clearPort()
    sleep(0.1)
    dxl_comm_number, dxl_comm_result, dxl_error = packet_handler.ping(port_handler, id)
    if dxl_comm_result != COMM_SUCCESS:
        print(f"Failed: {packet_handler.getTxRxResult(dxl_comm_result)}")
    else:
        print(f"{id} answered")
            
def initialize_motor():
    print("Start initializing motors")
     # initialize each id
    for id in [11, 21, 22, 23, 24, 31, 32, 41, 42, 43, 44]:
        if id in PORT0:  # Port0
            selected_port_handler = port_handler0
        elif id in PORT1:  # Port1
            selected_port_handler = port_handler1
        else:
            pass
        
        print(f"\nStart initializing motor for {id} on {selected_port_handler}")

        # Disable Torque
        set_motor1(selected_port_handler, id, ADDR_TORQUE_ENABLE, 0)
        sleep(0.1)
        
        # Check ping
        #ping(selected_port_handler, id)
        #sleep(0.1)

        # Set Position Control Mode
        set_motor1(selected_port_handler, id, ADDR_OPERATING_MODE, 4)        
        sleep(0.1)

        # Set Maximum Velocity
        set_motor1(selected_port_handler, id, ADDR_PROFILE_VELOCITY, 50)
        sleep(0.1)

        # Set Maximum Acceleration
        set_motor1(selected_port_handler, id, ADDR_PROFILE_ACCELERATION, 50)
        sleep(0.1)

        # Set Initial Position
        set_motor4(selected_port_handler, id, ADDR_GOAL_POSITION, MOTOR_LIMITS[id]["ini"])
        sleep(0.1)

        # Set Minimum (no use for mode 4)
        set_motor4(selected_port_handler, id, ADDR_MIN, MOTOR_LIMITS[id]["min"])
        sleep(0.1)

        # Set Maximum (no use for mode 4)
        set_motor4(selected_port_handler, id, ADDR_MAX, MOTOR_LIMITS[id]["max"])
        sleep(0.1)

        # Enable Torque
        set_motor1(selected_port_handler, id, ADDR_TORQUE_ENABLE, 1)
        sleep(0.1)

        # Set Initial Position
        #print(f"Set {id} to {MOTOR_LIMITS[id]["ini"]}. [MIN]: {MOTOR_LIMITS[id]["min"]}, [MAX]: {MOTOR_LIMITS[id]["max"]} ")
        #set_motor4(selected_port_handler, id, ADDR_GOAL_POSITION, MOTOR_LIMITS[id]["ini"])
        #sleep(0.1)

        # LED on
        set_motor1(selected_port_handler, id, ADDR_LED, 1)
        sleep(0.1)
        
        print(f"Done initializng motor for id: {id}")
    print("Done initializing motors")

def scan_motors():
    print("\nStart scaning motors on /dev/ttyUSB0")
    for id in range(0,254):
        dxl_model_number, dxl_comm_result, dxl_error = packet_handler.ping(port_handler0, id)
        if dxl_comm_result == COMM_SUCCESS:
            PORT0.append(id)
        prog = id/254 *100
        print(f"\rScaning /dev/ttyUSB0 [{prog} %]", end="")
    print(f"{PORT0} was found on /dev/ttyUSB0")

    print("\nStart scaning motors on /dev/ttyUSB1")
    for id in range(0,254):
        dxl_model_number, dxl_comm_result, dxl_error = packet_handler.ping(port_handler1, id)
        if dxl_comm_result == COMM_SUCCESS:
            PORT1.append(id)
        prog = id/254 *100
        print(f"\rScaning /dev/ttyUSB1 [{prog} %]", end="")
    print(f"{PORT1} was found on /dev/ttyUSB1")

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
        print(f"Failed to set the baudrate: {BAUDRATE}")
        return
    if not port_handler1.setBaudRate(BAUDRATE):
        print(f"Failed to set the baudrate: {BAUDRATE}")
        return
    print(f"Succeeded to set baudrate: {BAUDRATE}")

    scan_motors()

    initialize_motor()
    
    rclpy.init(args=args)
    node = MotorController()
    rclpy.spin(node)

    for id in np.array([11, 21, 22, 23, 24, 31, 32, 41, 42, 43, 44], dtype=np.uint8):
        if id in [31, 32, 41, 42, 43, 44]:  # Port1
            selected_port_handler = port_handler0
        elif id in [11, 21, 22, 23, 24]:  # Port2
            selected_port_handler = port_handler1
        
        packet_handler.write1ByteTxRx(selected_port_handler, id, ADDR_TORQUE_ENABLE, 0)  # Disable torque
        packet_handler.write1ByteTxRx(selected_port_handler, id, ADDR_LED, 0)
    node.destroy_node()
    rclpy.shutdown()
    port_handler0.closePort()
    port_handler1.closePort()


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2024 Ryo Isogawa
# SPDX-License-Identifier: BSD-3-Clause

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Joy
from motor_commands.msg import IdAngle
from dynamixel_sdk import *
from dynamixel_sdk_custom_interfaces.msg import SetPosition
from motor_commands.srv import GetMotorStates
import numpy as np
from time import sleep
import json
import random
import os

# Control table address
ADDR_OPERATING_MODE     = 11   # Set動作モード
ADDR_MAX_POSITION_LIMIT = 48   # 最大位置リミット
ADDR_MIN_POSITION_LIMIT = 52   # 最小位置リミット
ADDR_TORQUE_ENABLE      = 64   # トルク有効化
ADDR_LED                = 65   # LED
ADDR_GOAL_POSITION      = 116  # 目標位置
ADDR_PROFILE_VELOCITY   = 112  # プロファイル速度
ADDR_PROFILE_ACCELERATION = 108  # プロファイル加速度
ADDR_PRESENT_LOAD       = 128  # 現在の負荷
ADDR_PRESENT_POSITION   = 132  # 現在の位置
ADDR_PRESENT_TEMPERATURE = 146 # 現在の温度

# Protocol version
PROTOCOL_VERSION = 2.0 

# Default setting
BAUDRATE     = 57600 
DEVICE_NAME0 = "/dev/ttyUSB0"
DEVICE_NAME1 = "/dev/ttyUSB1"

# Initialize PortHandler and PacketHandler
port_handler0 = PortHandler(DEVICE_NAME0)
port_handler1 = PortHandler(DEVICE_NAME1)
packet_handler = PacketHandler(PROTOCOL_VERSION)

# Global lists for motor IDs found on each port
PORT0 = []
PORT1 = []

# GroupSyncWrite for sending commands to multiple motors at once
LEN_GOAL_POSITION = 4
groupSyncWrite0 = GroupSyncWrite(port_handler0, packet_handler, ADDR_GOAL_POSITION, LEN_GOAL_POSITION)
groupSyncWrite1 = GroupSyncWrite(port_handler1, packet_handler, ADDR_GOAL_POSITION, LEN_GOAL_POSITION)

# List of motor IDs to initialize/control
MOTOR_IDS = [11, 21, 22, 23, 24, 31, 32, 41, 42, 43, 44]

class MotorController(Node):
    def __init__(self, port0_open: bool, port1_open: bool):
        super().__init__('motor_controller')
        self.get_logger().info('Run motor controller node')
        self.port0_open = port0_open
        self.port1_open = port1_open

        self.motor_limits = {}
        self.load_motor_limits()

        # Service: GetMotorStates
        self.get_motor_states_service = self.create_service(
            GetMotorStates, 'get_motor_states', self.get_motor_states)
        self.get_logger().info('Run GetMotorStates server')

        # Subscriber: IdAngle
        self.subscription = self.create_subscription(
            IdAngle, 'IdAngle', self.listener_callback, 12)
        
    def load_motor_limits(self):
        limits_path = "/home/csanimatronics/CS_Animatronics/Motor_Limits.json"
        if not os.path.exists(limits_path):
            self.get_logger().error("Motor_Limits.json not found.")
            return
        with open(limits_path, "r", encoding="utf-8") as file:
            data = json.load(file)
        # Convert values to int
        for key, subdict in data.items():
            subdict["ini"] = int(subdict["ini"])
            subdict["min"] = int(subdict["min"])
            subdict["max"] = int(subdict["max"])
            subdict["acc"] = int(subdict["acc"])
            subdict["vel"] = int(subdict["vel"])
        self.motor_limits = data
        self.get_logger().info(f"Loaded motor limits: {self.motor_limits}")

    def listener_callback(self, msg: IdAngle):
        self.get_logger().info(f'Received Ids: {msg.ids}')
        self.get_logger().info(f'Received Angles: {msg.angles}')

        groupSyncWrite0.clearParam()
        groupSyncWrite1.clearParam()

        # Process each motor id from the message
        for idx, motor_id in enumerate(msg.ids):
            # Limit Check
            angle = int(msg.angles[idx])
            min_limit = self.motor_limits.get(f"{motor_id}", {}).get("min", angle)
            max_limit = self.motor_limits.get(f"{motor_id}", {}).get("max", angle)
            original_angle = angle

            if angle < min_limit:
                angle = min_limit
                self.get_logger().error(f"Below minimum motor {motor_id}: {original_angle} => {angle}")
            elif angle > max_limit:
                angle = max_limit
                self.get_logger().error(f"Above maximum motor {motor_id}: {original_angle} => {angle}")
            self.get_logger().info(f"Motor {motor_id}: angle set to {angle}")

            # Check port availability
            if not (self.port0_open and self.port1_open):
                return

            # Prepare parameter (little endian conversion)
            param_goal_position = [
                DXL_LOBYTE(DXL_LOWORD(angle)),
                DXL_HIBYTE(DXL_LOWORD(angle)),
                DXL_LOBYTE(DXL_HIWORD(angle)),
                DXL_HIBYTE(DXL_HIWORD(angle))
            ]

            # Add parameter to corresponding port
            if motor_id in PORT0:
                if not groupSyncWrite0.addParam(motor_id, param_goal_position):
                    self.get_logger().error(f"Failed to addParam for ID: {motor_id}")
            elif motor_id in PORT1:
                if not groupSyncWrite1.addParam(motor_id, param_goal_position):
                    self.get_logger().error(f"Failed to addParam for ID: {motor_id}")
            else:
                self.get_logger().info(f"Unknown motor ID: {motor_id}")
                continue

        # Send Sync Write
        dxl_comm_result = groupSyncWrite0.txPacket()
        if dxl_comm_result != COMM_SUCCESS:
            self.get_logger().error(f"Sync Write Error on port0: {packet_handler.getTxRxResult(dxl_comm_result)}")
        dxl_comm_result = groupSyncWrite1.txPacket()
        if dxl_comm_result != COMM_SUCCESS:
            self.get_logger().error(f"Sync Write Error on port1: {packet_handler.getTxRxResult(dxl_comm_result)}")
        
        groupSyncWrite0.clearParam()
        groupSyncWrite1.clearParam()

    def get_motor_states(self, request, response):
        self.get_logger().info(f"get_motor_states service called: {request}")
        ids, positions, temperatures, torques = [], [], [], []

        # If port is not open, return simulated values
        if not (self.port0_open and self.port1_open):
            self.get_logger().warn('Port not opened, returning simulated states.')
            for motor_id in request.ids:
                ids.append(motor_id)
                limits = self.motor_limits.get(f"{motor_id}", {})
                positions.append(random.randint(limits.get("min", 0), limits.get("max", 0)))
                temperatures.append(random.randint(0, 80))
                torques.append(random.randint(0, 100))
            response.ids = ids
            response.positions = positions
            response.temperatures = temperatures
            response.torques = torques
            return response

        # Read actual states
        for motor_id in request.ids:
            # Select port based on motor id
            selected_port_handler = port_handler0 if motor_id in PORT0 else port_handler1 if motor_id in PORT1 else None
            if selected_port_handler is None:
                self.get_logger().info(f"Unknown motor ID: {motor_id}")
                continue

            # Get position
            position, comm_result, _ = packet_handler.read4ByteTxRx(selected_port_handler, motor_id, ADDR_PRESENT_POSITION)
            if comm_result != COMM_SUCCESS:
                self.get_logger().error(f"Read position error on ID: {motor_id}")
                position = self.motor_limits.get(f"{motor_id}", {}).get("ini", 0)
            positions.append(position)

            # Get temperature
            temperature, comm_result, _ = packet_handler.read1ByteTxRx(selected_port_handler, motor_id, ADDR_PRESENT_TEMPERATURE)
            if comm_result != COMM_SUCCESS:
                self.get_logger().error(f"Read temperature error on ID: {motor_id}")
                temperature = 0
            temperatures.append(temperature)

            # Get torque (load)
            torque, comm_result, _ = packet_handler.read2ByteTxRx(selected_port_handler, motor_id, ADDR_PRESENT_LOAD)
            if comm_result != COMM_SUCCESS:
                self.get_logger().error(f"Read torque error on ID: {motor_id}")
                torque = 0
            torques.append(torque)
            ids.append(motor_id)

        response.ids = ids
        response.positions = positions
        response.temperatures = temperatures
        response.torques = torques
        return response

def set_motor1(port_handler, motor_id, addr, value):
    port_handler.clearPort()
    sleep(0.1)
    dxl_comm_result, _ = packet_handler.write1ByteTxRx(port_handler, motor_id, addr, value)
    if dxl_comm_result != COMM_SUCCESS:
        print(f"[Motor {motor_id}] Write1Byte failed: {packet_handler.getTxRxResult(dxl_comm_result)}")
    else:
        print(f"[Motor {motor_id}] Write1Byte succeeded.")

def set_motor4(port_handler, motor_id, addr, value):
    port_handler.clearPort()
    sleep(0.1)
    dxl_comm_result, _ = packet_handler.write4ByteTxRx(port_handler, motor_id, addr, value)
    if dxl_comm_result != COMM_SUCCESS:
        print(f"[Motor {motor_id}] Write4Byte failed: {packet_handler.getTxRxResult(dxl_comm_result)}")
    else:
        print(f"[Motor {motor_id}] Write4Byte succeeded.")

def ping_motor(port_handler, motor_id):
    port_handler.clearPort()
    sleep(0.1)
    dxl_model_number, dxl_comm_result, _ = packet_handler.ping(port_handler, motor_id)
    if dxl_comm_result != COMM_SUCCESS:
        print(f"[Motor {motor_id}] Ping failed: {packet_handler.getTxRxResult(dxl_comm_result)}")
    else:
        print(f"[Motor {motor_id}] Ping succeeded.")

def initialize_motor():
    # Load motor limits
    limits_path = "/home/csanimatronics/CS_Animatronics/Motor_Limits.json"
    if not os.path.exists(limits_path):
        print("Motor_Limits.json not found.")
        return
    with open(limits_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    for key, subdict in data.items():
        subdict["ini"] = int(subdict["ini"])
        subdict["min"] = int(subdict["min"])
        subdict["max"] = int(subdict["max"])
        subdict["acc"] = int(subdict["acc"])
        subdict["vel"] = int(subdict["vel"])
    motor_limits = data
    print(f"Loaded motor limits: {motor_limits}")

    print("Start initializing motors")
    for motor_id in MOTOR_IDS:
        # Select corresponding port
        if motor_id in PORT0:
            selected_port_handler = port_handler0
        elif motor_id in PORT1:
            selected_port_handler = port_handler1
        else:
            print(f"Motor ID {motor_id} not found on any port.")
            continue

        print(f"\nInitializing motor {motor_id} on {selected_port_handler.device_name}")
        # Disable torque
        set_motor1(selected_port_handler, motor_id, ADDR_TORQUE_ENABLE, 0)
        sleep(0.1)
        # Set position control mode
        set_motor1(selected_port_handler, motor_id, ADDR_OPERATING_MODE, 3)
        sleep(0.1)
        # Set profile velocity and acceleration
        set_motor4(selected_port_handler, motor_id, ADDR_PROFILE_VELOCITY, motor_limits[f"{motor_id}"]["vel"])
        sleep(0.1)
        set_motor4(selected_port_handler, motor_id, ADDR_PROFILE_ACCELERATION, motor_limits[f"{motor_id}"]["acc"])
        sleep(0.1)
        # Set initial position
        set_motor4(selected_port_handler, motor_id, ADDR_GOAL_POSITION, motor_limits[f"{motor_id}"]["ini"])
        sleep(0.1)
        # Set position limits
        set_motor4(selected_port_handler, motor_id, ADDR_MIN_POSITION_LIMIT, motor_limits[f"{motor_id}"]["min"])
        sleep(0.1)
        set_motor4(selected_port_handler, motor_id, ADDR_MAX_POSITION_LIMIT, motor_limits[f"{motor_id}"]["max"])
        sleep(0.1)
        # Enable torque
        set_motor1(selected_port_handler, motor_id, ADDR_TORQUE_ENABLE, 1)
        sleep(0.1)
        # LED on
        set_motor1(selected_port_handler, motor_id, ADDR_LED, 1)
        sleep(0.1)
        print(f"Finished initializing motor {motor_id}")
    print("Finished initializing motors")

def scan_motors():
    try:
        print("\nScanning motors on /dev/ttyUSB0")
        for motor_id in range(1, 254):
            _, comm_result, _ = packet_handler.ping(port_handler0, motor_id)
            if comm_result == COMM_SUCCESS:
                PORT0.append(motor_id)
            # Progress update
            prog = motor_id / 254 * 100
            print(f"\rScanning /dev/ttyUSB0 [{prog:.1f}%]", end="")
        print(f"\nFound on /dev/ttyUSB0: {PORT0}")

        print("\nScanning motors on /dev/ttyUSB1")
        for motor_id in range(1, 254):
            _, comm_result, _ = packet_handler.ping(port_handler1, motor_id)
            if comm_result == COMM_SUCCESS:
                PORT1.append(motor_id)
            prog = motor_id / 254 * 100
            print(f"\rScanning /dev/ttyUSB1 [{prog:.1f}%]", end="")
        print(f"\nFound on /dev/ttyUSB1: {PORT1}")
    except Exception as e:
        print(f"Scanning error: {e}")

def main(args=None):
    port0_open = False
    port1_open = False

    # Open Serial Ports and set Baudrate
    try:
        if not port_handler0.openPort():
            print("Failed to open port0")
            return
        else:
            port0_open = True

        if not port_handler1.openPort():
            print("Failed to open port1")
            return
        else:
            port1_open = True

        print("Serial ports opened successfully.")
    except Exception as e:
        print(f"Port open exception: {e}")
        return

    if not port_handler0.setBaudRate(BAUDRATE):
        print(f"Failed to set baudrate {BAUDRATE} on port0")
        return
    if not port_handler1.setBaudRate(BAUDRATE):
        print(f"Failed to set baudrate {BAUDRATE} on port1")
        return
    print(f"Baudrate set to {BAUDRATE} on both ports.")

    scan_motors()

    try:
        initialize_motor()
    except Exception as e:
        print(f"Motor initialization failed: {e}")

    rclpy.init(args=args)
    node = MotorController(port0_open, port1_open)
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        print("Shutting down motor controller node.")
    finally:
        # Disable motors and turn off LED
        for motor_id in MOTOR_IDS:
            if motor_id in PORT0:
                selected_port_handler = port_handler0
            elif motor_id in PORT1:
                selected_port_handler = port_handler1
            else:
                continue
            packet_handler.write1ByteTxRx(selected_port_handler, motor_id, ADDR_TORQUE_ENABLE, 0)
            packet_handler.write1ByteTxRx(selected_port_handler, motor_id, ADDR_LED, 0)
        node.destroy_node()
        rclpy.shutdown()
        port_handler0.closePort()
        port_handler1.closePort()

if __name__ == "__main__":
    main()

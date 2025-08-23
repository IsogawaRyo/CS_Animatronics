#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2024 Ryo Isogawa
# SPDX-License-Identifier: BSD-3-Clause

import rclpy
from rclpy.node import Node
from motor_commands.msg import IdAngle
from dynamixel_sdk import *
from dynamixel_sdk import GroupSyncRead
from dynamixel_sdk_custom_interfaces.msg import SetPosition
from motor_commands.srv import GetMotorStates
import numpy as np
from time import sleep
import json
import random
import os

# Control table address
ADDR_OPERATING_MODE       = 11   # 動作モード設定
ADDR_MAX_POSITION_LIMIT   = 48   # 最大位置リミット
ADDR_MIN_POSITION_LIMIT   = 52   # 最小位置リミット
ADDR_TORQUE_ENABLE        = 64   # トルク有効化
ADDR_LED                  = 65   # LED
ADDR_GOAL_POSITION        = 116  # 目標位置
ADDR_PROFILE_VELOCITY     = 112  # プロファイル速度
ADDR_PROFILE_ACCELERATION = 108  # プロファイル加速度
ADDR_PRESENT_LOAD         = 128  # 負荷
ADDR_PRESENT_POSITION     = 132  # 位置
ADDR_PRESENT_TEMPERATURE  = 146  # 温度

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

# GroupSyncRead for reading states from multiple motors at once
LEN_PRESENT_POSITION = 4
LEN_PRESENT_TEMPERATURE = 1  
LEN_PRESENT_LOAD = 2
groupSyncRead0_pos = GroupSyncRead(port_handler0, packet_handler, ADDR_PRESENT_POSITION, LEN_PRESENT_POSITION)
groupSyncRead1_pos = GroupSyncRead(port_handler1, packet_handler, ADDR_PRESENT_POSITION, LEN_PRESENT_POSITION)
groupSyncRead0_temp = GroupSyncRead(port_handler0, packet_handler, ADDR_PRESENT_TEMPERATURE, LEN_PRESENT_TEMPERATURE)
groupSyncRead1_temp = GroupSyncRead(port_handler1, packet_handler, ADDR_PRESENT_TEMPERATURE, LEN_PRESENT_TEMPERATURE)
groupSyncRead0_load = GroupSyncRead(port_handler0, packet_handler, ADDR_PRESENT_LOAD, LEN_PRESENT_LOAD)
groupSyncRead1_load = GroupSyncRead(port_handler1, packet_handler, ADDR_PRESENT_LOAD, LEN_PRESENT_LOAD)

# List of motor IDs to initialize/control
MOTOR_IDS = [11, 12, 13, 21, 22, 23, 24, 31, 32, 33, 34]

class MotorController(Node):
    def __init__(self, port0_open: bool, port1_open: bool):
        super().__init__('motor_controller')
        self.get_logger().info('Run motor controller node')
        self.port0_open = port0_open
        self.port1_open = port1_open

        # simulation mode if any port is not open
        self.simulation = not (self.port0_open and self.port1_open)

        self.motor_limits = {}
        self.load_motor_limits()
        
        # Cache for GetMotorStates to reduce communication overhead
        self.motor_states_cache = {}
        self.last_cache_time = 0.0
        self.cache_duration = 0.05  # 50ms cache duration

        # Initialize dummy motor states (simulation)
        self.dummy_motor_states = {}
        for motor_id in MOTOR_IDS:
            # 初期値はJSONで定義された初期位置、なければ0
            self.dummy_motor_states[motor_id] = self.motor_limits.get(f"{motor_id}", {}).get("ini", 0)

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
        self.get_logger().info(f"Received Ids: {msg.ids}")
        self.get_logger().info(f"Received Angles: {msg.angles}")

        # シミュレーションモードの場合は物理通信せずに内部状態を更新
        if self.simulation:
            for idx, motor_id in enumerate(msg.ids):
                angle = int(msg.angles[idx])
                limits = self.motor_limits.get(f"{motor_id}", {})
                min_limit = limits.get("min", angle)
                max_limit = limits.get("max", angle)
                original_angle = angle

                if angle < min_limit:
                    angle = min_limit
                    self.get_logger().error(f"Below minimum motor {motor_id}: {original_angle} => {angle}")
                elif angle > max_limit:
                    angle = max_limit
                    self.get_logger().error(f"Above maximum motor {motor_id}: {original_angle} => {angle}")

                self.dummy_motor_states[motor_id] = angle
                self.get_logger().info(f"Simulated motor {motor_id}: angle set to {angle}")
            return

        # 物理ポートが開いている場合
        groupSyncWrite0.clearParam()
        groupSyncWrite1.clearParam()

        for idx, motor_id in enumerate(msg.ids):
            angle = int(msg.angles[idx])
            limits = self.motor_limits.get(f"{motor_id}", {})
            min_limit = limits.get("min", angle)
            max_limit = limits.get("max", angle)
            original_angle = angle

            if angle < min_limit:
                angle = min_limit
                self.get_logger().error(f"Below minimum motor {motor_id}: {original_angle} => {angle}")
            elif angle > max_limit:
                angle = max_limit
                self.get_logger().error(f"Above maximum motor {motor_id}: {original_angle} => {angle}")
            self.get_logger().info(f"Motor {motor_id}: angle set to {angle}")

            # little endian conversion
            param_goal_position = [
                DXL_LOBYTE(DXL_LOWORD(angle)),
                DXL_HIBYTE(DXL_LOWORD(angle)),
                DXL_LOBYTE(DXL_HIWORD(angle)),
                DXL_HIBYTE(DXL_HIWORD(angle))
            ]

            if motor_id in PORT0:
                if not groupSyncWrite0.addParam(motor_id, param_goal_position):
                    self.get_logger().error(f"Failed to addParam for ID: {motor_id}")
            elif motor_id in PORT1:
                if not groupSyncWrite1.addParam(motor_id, param_goal_position):
                    self.get_logger().error(f"Failed to addParam for ID: {motor_id}")
            else:
                self.get_logger().info(f"Unknown motor ID: {motor_id}")
                continue

        dxl_comm_result = groupSyncWrite0.txPacket()
        if dxl_comm_result != COMM_SUCCESS:
            self.get_logger().error(f"Sync Write Error on port0: {packet_handler.getTxRxResult(dxl_comm_result)}")
        dxl_comm_result = groupSyncWrite1.txPacket()
        if dxl_comm_result != COMM_SUCCESS:
            self.get_logger().error(f"Sync Write Error on port1: {packet_handler.getTxRxResult(dxl_comm_result)}")

        groupSyncWrite0.clearParam()
        groupSyncWrite1.clearParam()

    def get_motor_states(self, request, response):
        import time
        current_time = time.time()
        
        # Check cache first to reduce communication overhead
        if (current_time - self.last_cache_time < self.cache_duration and 
            self.motor_states_cache and 
            all(mid in self.motor_states_cache for mid in request.ids)):
            
            ids, positions, temperatures, torques = [], [], [], []
            for motor_id in request.ids:
                if motor_id in self.motor_states_cache:
                    cached_data = self.motor_states_cache[motor_id]
                    ids.append(motor_id)
                    positions.append(cached_data['position'])
                    temperatures.append(cached_data['temperature'])
                    torques.append(cached_data['torque'])
            
            response.ids = ids
            response.positions = positions
            response.temperatures = temperatures
            response.torques = torques
            return response

        self.get_logger().debug(f"get_motor_states service called: {request}")
        ids, positions, temperatures, torques = [], [], [], []

        if self.simulation:
            for motor_id in request.ids:
                ids.append(motor_id)
                positions.append(self.dummy_motor_states.get(motor_id, random.randint(0, 4095)))
                temperatures.append(random.randint(0, 80))
                torques.append(random.randint(0, 100))
            response.ids = ids
            response.positions = positions
            response.temperatures = temperatures
            response.torques = torques
            return response

        # Optimized bulk reading using GroupSyncRead
        try:
            ids, positions, temperatures, torques = self._bulk_read_motor_states(request.ids)
            
            # Update cache
            self.last_cache_time = current_time
            for i, motor_id in enumerate(ids):
                self.motor_states_cache[motor_id] = {
                    'position': positions[i],
                    'temperature': temperatures[i],
                    'torque': torques[i]
                }
                
        except Exception as e:
            self.get_logger().error(f"Bulk read failed, falling back to individual reads: {e}")
            ids, positions, temperatures, torques = self._individual_read_motor_states(request.ids)

        response.ids = ids
        response.positions = positions
        response.temperatures = temperatures
        response.torques = torques
        return response
    
    def _bulk_read_motor_states(self, requested_ids):
        """Optimized bulk reading using GroupSyncRead"""
        ids, positions, temperatures, torques = [], [], [], []
        
        # Separate motors by port
        port0_motors = [mid for mid in requested_ids if mid in PORT0]
        port1_motors = [mid for mid in requested_ids if mid in PORT1]
        
        # Read positions from both ports
        pos_data = self._bulk_read_parameter(port0_motors, port1_motors, 
                                           groupSyncRead0_pos, groupSyncRead1_pos, 
                                           ADDR_PRESENT_POSITION, LEN_PRESENT_POSITION)
        
        # For observe mode, prioritize position data and use cached/default values for temp/torque
        for motor_id in requested_ids:
            if motor_id in pos_data:
                ids.append(motor_id)
                positions.append(pos_data[motor_id])
                # Use cached values or defaults for less critical data
                cached = self.motor_states_cache.get(motor_id, {})
                temperatures.append(cached.get('temperature', 25))  # Default room temperature
                torques.append(cached.get('torque', 0))  # Default no load
            else:
                self.get_logger().warn(f"Failed to read motor {motor_id}")
        
        return ids, positions, temperatures, torques
    
    def _bulk_read_parameter(self, port0_motors, port1_motors, sync_read0, sync_read1, addr, length):
        """Helper method for bulk parameter reading"""
        result_data = {}
        
        # Setup and read from port0
        if port0_motors:
            sync_read0.clearParam()
            for motor_id in port0_motors:
                sync_read0.addParam(motor_id)
            
            if sync_read0.txRxPacket() == COMM_SUCCESS:
                for motor_id in port0_motors:
                    if sync_read0.isAvailableData(motor_id, addr, length):
                        if length == 4:
                            result_data[motor_id] = sync_read0.getData(motor_id, addr, length)
                        elif length == 2:
                            result_data[motor_id] = sync_read0.getData(motor_id, addr, length)
                        else:
                            result_data[motor_id] = sync_read0.getData(motor_id, addr, length)
        
        # Setup and read from port1  
        if port1_motors:
            sync_read1.clearParam()
            for motor_id in port1_motors:
                sync_read1.addParam(motor_id)
                
            if sync_read1.txRxPacket() == COMM_SUCCESS:
                for motor_id in port1_motors:
                    if sync_read1.isAvailableData(motor_id, addr, length):
                        if length == 4:
                            result_data[motor_id] = sync_read1.getData(motor_id, addr, length)
                        elif length == 2:
                            result_data[motor_id] = sync_read1.getData(motor_id, addr, length)
                        else:
                            result_data[motor_id] = sync_read1.getData(motor_id, addr, length)
        
        return result_data
    
    def _individual_read_motor_states(self, requested_ids):
        """Fallback individual reading method"""
        ids, positions, temperatures, torques = [], [], [], []
        
        for motor_id in requested_ids:
            selected_port_handler = (port_handler0 if motor_id in PORT0 
                                       else port_handler1 if motor_id in PORT1 
                                       else None)
            if selected_port_handler is None:
                continue

            # Read position (most important for observe mode)
            position, comm_result, _ = packet_handler.read4ByteTxRx(selected_port_handler, motor_id, ADDR_PRESENT_POSITION)
            if comm_result != COMM_SUCCESS:
                position = self.motor_limits.get(f"{motor_id}", {}).get("ini", 0)

            # For performance, use cached/default values for temperature and torque
            cached = self.motor_states_cache.get(motor_id, {})
            temperature = cached.get('temperature', 25)  # Use cached or default
            torque = cached.get('torque', 0)  # Use cached or default
            
            positions.append(position)
            temperatures.append(temperature)
            torques.append(torque)
            ids.append(motor_id)

        return ids, positions, temperatures, torques

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
        if motor_id in PORT0:
            selected_port_handler = port_handler0
        elif motor_id in PORT1:
            selected_port_handler = port_handler1
        else:
            print(f"Motor ID {motor_id} not found on any port.")
            continue

        print(f"\nInitializing motor {motor_id} on")
        set_motor1(selected_port_handler, motor_id, ADDR_TORQUE_ENABLE, 0)
        sleep(0.1)
        set_motor1(selected_port_handler, motor_id, ADDR_OPERATING_MODE, 3)
        sleep(0.1)
        set_motor4(selected_port_handler, motor_id, ADDR_PROFILE_VELOCITY, motor_limits[f"{motor_id}"]["vel"])
        sleep(0.1)
        set_motor4(selected_port_handler, motor_id, ADDR_PROFILE_ACCELERATION, motor_limits[f"{motor_id}"]["acc"])
        sleep(0.1)
        set_motor4(selected_port_handler, motor_id, ADDR_GOAL_POSITION, motor_limits[f"{motor_id}"]["ini"])
        sleep(0.1)
        set_motor4(selected_port_handler, motor_id, ADDR_MIN_POSITION_LIMIT, motor_limits[f"{motor_id}"]["min"])
        sleep(0.1)
        set_motor4(selected_port_handler, motor_id, ADDR_MAX_POSITION_LIMIT, motor_limits[f"{motor_id}"]["max"])
        sleep(0.1)
        set_motor1(selected_port_handler, motor_id, ADDR_TORQUE_ENABLE, 1)
        sleep(0.1)
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
    # シリアルポートのオープン処理をtry/exceptで行い、例外発生時にもフラグを更新
    try:
        port0_open = port_handler0.openPort()
    except Exception as e:
        print(f"Exception opening port0: {e}")
        port0_open = False

    if not port0_open:
        print("Failed to open port0. Running in simulation mode.")

    try:
        port1_open = port_handler1.openPort()
    except Exception as e:
        print(f"Exception opening port1: {e}")
        port1_open = False

    if not port1_open:
        print("Failed to open port1. Running in simulation mode.")

    # 各ポートがオープンしている場合のみbaudrate設定
    if port0_open:
        if not port_handler0.setBaudRate(BAUDRATE):
            print(f"Failed to set baudrate {BAUDRATE} on port0")
            port0_open = False
    if port1_open:
        if not port_handler1.setBaudRate(BAUDRATE):
            print(f"Failed to set baudrate {BAUDRATE} on port1")
            port1_open = False

    if port0_open and port1_open:
        print(f"Baudrate set to {BAUDRATE} on both ports.")
        scan_motors()
        try:
            initialize_motor()
        except Exception as e:
            print(f"Motor initialization failed: {e}")
    else:
        print("One or more ports not open; operating in simulation mode.")

    rclpy.init(args=args)
    node = MotorController(port0_open, port1_open)
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        print("Shutting down motor controller node.")
    finally:
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
        if port0_open:
            port_handler0.closePort()
        if port1_open:
            port_handler1.closePort()

if __name__ == "__main__":
    main()

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
from motor_commands.srv import SetTorque
from std_srvs.srv import Trigger
from serial import SerialException
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
ADDR_PRESENT_CURRENT      = 126  # 現在電流（トルク相当）
ADDR_PRESENT_LOAD         = 128  # 負荷（古い形式）
ADDR_PRESENT_POSITION     = 132  # 位置
ADDR_PRESENT_TEMPERATURE  = 146  # 温度
ADDR_HARDWARE_ERROR_STATUS = 70   # ハードウェアエラーステータス

# Protocol version
PROTOCOL_VERSION = 2.0 

# Default setting
BAUDRATE     = 115200 
import glob
available_ports = sorted(glob.glob('/dev/ttyUSB*') + glob.glob('/dev/ttyACM*'))
DEVICE_NAME0 = available_ports[0] if len(available_ports) > 0 else "/dev/ttyUSB0"
DEVICE_NAME1 = available_ports[1] if len(available_ports) > 1 else "/dev/ttyUSB1"
DEVICE_NAME2 = available_ports[2] if len(available_ports) > 2 else "/dev/ttyUSB2"

# Initialize PortHandler and PacketHandler
port_handler0 = PortHandler(DEVICE_NAME0)
port_handler1 = PortHandler(DEVICE_NAME1)
port_handler2 = PortHandler(DEVICE_NAME2)
packet_handler = PacketHandler(PROTOCOL_VERSION)

# Global lists for motor IDs found on each port
PORT0 = []
PORT1 = []
PORT2 = []

# GroupSyncWrite for sending commands to multiple motors at once
LEN_GOAL_POSITION = 4
groupSyncWrite0 = GroupSyncWrite(port_handler0, packet_handler, ADDR_GOAL_POSITION, LEN_GOAL_POSITION)
groupSyncWrite1 = GroupSyncWrite(port_handler1, packet_handler, ADDR_GOAL_POSITION, LEN_GOAL_POSITION)
groupSyncWrite2 = GroupSyncWrite(port_handler2, packet_handler, ADDR_GOAL_POSITION, LEN_GOAL_POSITION)

# GroupSyncRead for reading states from multiple motors at once
LEN_PRESENT_POSITION = 4
LEN_PRESENT_TEMPERATURE = 1  
LEN_PRESENT_CURRENT = 2  # Current/torque is 2 bytes
LEN_PRESENT_LOAD = 2
LEN_HARDWARE_ERROR = 1   # Hardware error status is 1 byte
groupSyncRead0_pos = GroupSyncRead(port_handler0, packet_handler, ADDR_PRESENT_POSITION, LEN_PRESENT_POSITION)
groupSyncRead1_pos = GroupSyncRead(port_handler1, packet_handler, ADDR_PRESENT_POSITION, LEN_PRESENT_POSITION)
groupSyncRead2_pos = GroupSyncRead(port_handler2, packet_handler, ADDR_PRESENT_POSITION, LEN_PRESENT_POSITION)
groupSyncRead0_temp = GroupSyncRead(port_handler0, packet_handler, ADDR_PRESENT_TEMPERATURE, LEN_PRESENT_TEMPERATURE)
groupSyncRead1_temp = GroupSyncRead(port_handler1, packet_handler, ADDR_PRESENT_TEMPERATURE, LEN_PRESENT_TEMPERATURE)
groupSyncRead2_temp = GroupSyncRead(port_handler2, packet_handler, ADDR_PRESENT_TEMPERATURE, LEN_PRESENT_TEMPERATURE)
# Try both current and load addresses for better compatibility
groupSyncRead0_current = GroupSyncRead(port_handler0, packet_handler, ADDR_PRESENT_CURRENT, LEN_PRESENT_CURRENT)
groupSyncRead1_current = GroupSyncRead(port_handler1, packet_handler, ADDR_PRESENT_CURRENT, LEN_PRESENT_CURRENT)
groupSyncRead2_current = GroupSyncRead(port_handler2, packet_handler, ADDR_PRESENT_CURRENT, LEN_PRESENT_CURRENT)
groupSyncRead0_load = GroupSyncRead(port_handler0, packet_handler, ADDR_PRESENT_LOAD, LEN_PRESENT_LOAD)
groupSyncRead1_load = GroupSyncRead(port_handler1, packet_handler, ADDR_PRESENT_LOAD, LEN_PRESENT_LOAD)
groupSyncRead2_load = GroupSyncRead(port_handler2, packet_handler, ADDR_PRESENT_LOAD, LEN_PRESENT_LOAD)
groupSyncRead0_error = GroupSyncRead(port_handler0, packet_handler, ADDR_HARDWARE_ERROR_STATUS, LEN_HARDWARE_ERROR)
groupSyncRead1_error = GroupSyncRead(port_handler1, packet_handler, ADDR_HARDWARE_ERROR_STATUS, LEN_HARDWARE_ERROR)
groupSyncRead2_error = GroupSyncRead(port_handler2, packet_handler, ADDR_HARDWARE_ERROR_STATUS, LEN_HARDWARE_ERROR)

# List of motor IDs to initialize/control
MOTOR_IDS = [
    11, 12, 13, 
    21, 22, 23, 24, 
    31, 32, 33, 34,
    41, 42, 43, 44,
    51, 52,
    60, 61, 62, 63, 64,
    65, 66, 67, 68, 69
]

OBSERVE_CACHE_DURATION = 0.3  # seconds MotionEditor Observe result may be reused

class MotorController(Node):
    def __init__(self, port0_open: bool, port1_open: bool, port2_open: bool):
        super().__init__('motor_controller')
        self.get_logger().info('Run motor controller node')
        self.port0_open = port0_open
        self.port1_open = port1_open
        self.port2_open = port2_open

        # simulation mode if NO port is open (allow partial connection)
        self.simulation = not (self.port0_open or self.port1_open or self.port2_open)

        self.motor_limits = {}
        self.load_motor_limits()
        
        # Cache for GetMotorStates to reduce communication overhead  
        self.motor_states_cache = {}
        self.last_cache_time = 0.0
        self.cache_duration = OBSERVE_CACHE_DURATION
        
        # Read cycle counter for interleaving optimization
        self.read_cycle = 0

        # Initialize dummy motor states (simulation)
        self.dummy_motor_states = {}
        for motor_id in MOTOR_IDS:
            # 初期値はJSONで定義された初期位置、なければ0
            self.dummy_motor_states[motor_id] = self.motor_limits.get(f"{motor_id}", {}).get("ini", 0)

        # Service: GetMotorStates
        self.get_motor_states_service = self.create_service(
            GetMotorStates, 'get_motor_states', self.get_motor_states)
        self.get_logger().info('Run GetMotorStates server')

        # Service: SetTorque (enable/disable torque for multiple motors)
        self.set_torque_service = self.create_service(
            SetTorque, 'set_torque', self.set_torque)
        self.get_logger().info('Run SetTorque server')

        # Service: Reconnect Ports
        self.reconnect_service = self.create_service(
            Trigger, 'reconnect_ports', self.reconnect_ports_callback)
        self.get_logger().info('Run ReconnectPorts server')

        # Subscriber: IdAngle
        self.subscription = self.create_subscription(
            IdAngle, 'IdAngle', self.listener_callback, 12)

        # Subscriber: motor_reboot (uses IdAngle.ids; angles ignored)
        self.reboot_subscription = self.create_subscription(
            IdAngle, 'motor_reboot', self.reboot_callback, 10)
        self.get_logger().info('Reboot subscriber ready on /motor_reboot')
        
    def load_motor_limits(self):
        limits_path = os.path.expanduser("~/CS_Animatronics/Motor_Limits.json")
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
        # self.get_logger().debug(f"Received Ids: {msg.ids} (length: {len(msg.ids)})")
        # self.get_logger().debug(f"Received Angles: {msg.angles} (length: {len(msg.angles)})")
        
        # Debug: Check each ID/angle pair
        # for i, (id_val, angle_val) in enumerate(zip(msg.ids, msg.angles)):
        #     self.get_logger().debug(f"  [{i}] Motor ID: {id_val}, Angle: {angle_val}")

        # シミュレーションモードの場合は物理通信せずに内部状態を更新
        if self.simulation:
            for idx, motor_id in enumerate(msg.ids):
                # Skip motor ID 0 (invalid/padding motor ID)
                if motor_id == 0:
                    # self.get_logger().debug(f"Skipping invalid motor ID: {motor_id}")
                    continue
                    
                angle = int(msg.angles[idx])
                limits = self.motor_limits.get(f"{motor_id}", {})
                min_limit = limits.get("min", angle)
                max_limit = limits.get("max", angle)
                original_angle = angle

                if angle < min_limit:
                    angle = min_limit
                    self.get_logger().debug(f"Below minimum motor {motor_id}: {original_angle} => {angle}")
                elif angle > max_limit:
                    angle = max_limit
                    self.get_logger().debug(f"Above maximum motor {motor_id}: {original_angle} => {angle}")

                self.dummy_motor_states[motor_id] = angle
                # self.get_logger().debug(f"Simulated motor {motor_id}: angle set to {angle}")
            return

        # 物理ポートが開いている場合
        groupSyncWrite0.clearParam()
        groupSyncWrite1.clearParam()
        groupSyncWrite2.clearParam()

        for idx, motor_id in enumerate(msg.ids):
            # Skip motor ID 0 (invalid/padding motor ID)
            if motor_id == 0:
                # self.get_logger().debug(f"Skipping invalid motor ID: {motor_id}")
                continue
                
            angle = int(msg.angles[idx])
            limits = self.motor_limits.get(f"{motor_id}", {})
            min_limit = limits.get("min", angle)
            max_limit = limits.get("max", angle)
            original_angle = angle

            if angle < min_limit:
                angle = min_limit
                self.get_logger().debug(f"Below minimum motor {motor_id}: {original_angle} => {angle}")
            elif angle > max_limit:
                angle = max_limit
                self.get_logger().debug(f"Above maximum motor {motor_id}: {original_angle} => {angle}")
            # self.get_logger().debug(f"Motor {motor_id}: angle set to {angle}")

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
            elif motor_id in PORT2:
                if not groupSyncWrite2.addParam(motor_id, param_goal_position):
                    self.get_logger().error(f"Failed to addParam for ID: {motor_id}")
            else:
                self.get_logger().info(f"Unknown motor ID: {motor_id}")
                continue

        # Only transmit if at least one motor param was added for that port
        port0_motors_added = any(mid in PORT0 for mid in msg.ids if mid != 0)
        port1_motors_added = any(mid in PORT1 for mid in msg.ids if mid != 0)
        port2_motors_added = any(mid in PORT2 for mid in msg.ids if mid != 0)

        if port0_motors_added:
            dxl_comm_result = groupSyncWrite0.txPacket()
            if dxl_comm_result != COMM_SUCCESS:
                self.get_logger().error(f"Sync Write Error on port0: {packet_handler.getTxRxResult(dxl_comm_result)}")
        if port1_motors_added:
            dxl_comm_result = groupSyncWrite1.txPacket()
            if dxl_comm_result != COMM_SUCCESS:
                self.get_logger().error(f"Sync Write Error on port1: {packet_handler.getTxRxResult(dxl_comm_result)}")
        if port2_motors_added:
            dxl_comm_result = groupSyncWrite2.txPacket()
            if dxl_comm_result != COMM_SUCCESS:
                self.get_logger().error(f"Sync Write Error on port2: {packet_handler.getTxRxResult(dxl_comm_result)}")

        groupSyncWrite0.clearParam()
        groupSyncWrite1.clearParam()
        groupSyncWrite2.clearParam()

    def get_motor_states(self, request, response):
        import time
        current_time = time.time()
        
        # Check cache first to reduce communication overhead
        if (current_time - self.last_cache_time < self.cache_duration and 
            self.motor_states_cache and 
            all(mid in self.motor_states_cache for mid in request.ids)):
            
            ids, positions, temperatures, torques, error_statuses = [], [], [], [], []
            for motor_id in request.ids:
                if motor_id in self.motor_states_cache:
                    cached_data = self.motor_states_cache[motor_id]
                    ids.append(motor_id)
                    positions.append(cached_data['position'])
                    temperatures.append(cached_data['temperature'])
                    torques.append(cached_data['torque'])
                    error_statuses.append(cached_data.get('error_status', 'NO_ERROR'))
            
            # Calculate total currents from cached data
            port0_total, port1_total, system_total = self._calculate_total_currents(ids, torques)
            
            response.ids = ids
            response.positions = positions
            response.temperatures = temperatures
            response.torques = torques
            response.error_status = error_statuses
            response.port0_total_current = port0_total
            response.port1_total_current = port1_total
            response.system_total_current = system_total
            return response

        self.get_logger().debug(f"get_motor_states service called: {request}")
        ids, positions, temperatures, torques = [], [], [], []

        if self.simulation:
            error_statuses = []
            for motor_id in request.ids:
                ids.append(motor_id)
                positions.append(self.dummy_motor_states.get(motor_id, random.randint(0, 4095)))
                temperatures.append(random.randint(0, 80))
                torques.append(random.randint(0, 100))
                error_statuses.append("NO_ERROR")  # Simulation - no errors
            
            # Calculate total currents for simulation mode
            port0_total, port1_total, system_total = self._calculate_total_currents(ids, torques)
            
            response.ids = ids
            response.positions = positions
            response.temperatures = temperatures
            response.torques = torques
            response.error_status = error_statuses
            response.port0_total_current = port0_total
            response.port1_total_current = port1_total
            response.system_total_current = system_total
            return response

        # Optimized bulk reading using GroupSyncRead
        try:
            ids, positions, temperatures, torques, error_statuses = self._bulk_read_motor_states(request.ids)
            
            # Update cache
            self.last_cache_time = current_time
            for i, motor_id in enumerate(ids):
                self.motor_states_cache[motor_id] = {
                    'position': positions[i],
                    'temperature': temperatures[i],
                    'torque': torques[i],
                    'error_status': error_statuses[i] if i < len(error_statuses) else 'NO_ERROR'
                }
                
        except Exception as e:
            self.get_logger().error(f"Bulk read failed, falling back to individual reads: {e}")
            ids, positions, temperatures, torques, error_statuses = self._individual_read_motor_states(request.ids)

        # Calculate total currents for each port and system
        port0_total, port1_total, system_total = self._calculate_total_currents(ids, torques)

        response.ids = ids
        response.positions = positions
        response.temperatures = temperatures
        response.torques = torques
        response.error_status = error_statuses
        response.port0_total_current = port0_total
        response.port1_total_current = port1_total  
        response.system_total_current = system_total
        return response

    def reboot_callback(self, msg: IdAngle):
        """Reboot each requested motor ID via Dynamixel reboot packet."""
        for motor_id in msg.ids:
            if motor_id == 0:
                continue
            if motor_id in PORT0:
                ph = port_handler0
            elif motor_id in PORT1:
                ph = port_handler1
            elif motor_id in PORT2:
                ph = port_handler2
            else:
                self.get_logger().warn(f"Reboot: unknown motor ID {motor_id}")
                continue

            comm_result, error = packet_handler.reboot(ph, motor_id)
            if comm_result == COMM_SUCCESS:
                self.get_logger().info(f"Motor {motor_id} rebooted successfully.")
                # Brief delay for motor to come back online
                sleep(0.5)
                # Re-enable torque and LED after reboot
                limits = self.motor_limits.get(f"{motor_id}", {})
                ini = limits.get("ini", 2048)
                packet_handler.write4ByteTxRx(ph, motor_id, ADDR_GOAL_POSITION, ini)
                packet_handler.write1ByteTxRx(ph, motor_id, ADDR_TORQUE_ENABLE, 1)
                packet_handler.write1ByteTxRx(ph, motor_id, ADDR_LED, 1)
                self.get_logger().info(f"Motor {motor_id} re-initialized to pos={ini}.")
            else:
                self.get_logger().error(
                    f"Reboot failed for {motor_id}: {packet_handler.getTxRxResult(comm_result)}")

    def set_torque(self, request, response):
        """Service handler to enable/disable torque for the specified motor IDs"""
        try:
            # In simulation mode, accept and return success without hardware access
            if self.simulation:
                response.success = True
                response.message = 'Simulation mode: torque change accepted'
                return response

            enable_val = 1 if request.enable else 0

            for motor_id in request.ids:
                if motor_id in PORT0:
                    selected_port_handler = port_handler0
                elif motor_id in PORT1:
                    selected_port_handler = port_handler1
                elif motor_id in PORT2:
                    selected_port_handler = port_handler2
                else:
                    # Unknown ID; skip but keep going
                    self.get_logger().warn(f"SetTorque: Unknown motor ID {motor_id}")
                    continue

                dxl_comm_result, _ = packet_handler.write1ByteTxRx(
                    selected_port_handler, motor_id, ADDR_TORQUE_ENABLE, enable_val)
                if dxl_comm_result != COMM_SUCCESS:
                    self.get_logger().error(
                        f"SetTorque failed for {motor_id}: {packet_handler.getTxRxResult(dxl_comm_result)}")
                else:
                    self.get_logger().info(
                        f"SetTorque {'ENABLED' if request.enable else 'DISABLED'} for ID {motor_id}")

                    # When torque is enabled, drive motor back to its ini position so it holds safely
                    if request.enable:
                        limits = self.motor_limits.get(f"{motor_id}")
                        ini = limits.get("ini") if limits else None
                        if ini is not None:
                            write_result, _ = packet_handler.write4ByteTxRx(
                                selected_port_handler, motor_id, ADDR_GOAL_POSITION, int(ini))
                            if write_result != COMM_SUCCESS:
                                self.get_logger().warn(
                                    f"SetTorque: failed to reset ID {motor_id} to ini ({packet_handler.getTxRxResult(write_result)})")
                        else:
                            self.get_logger().warn(
                                f"SetTorque: ini position unknown for ID {motor_id}; skipping reset")

            response.success = True
            response.message = 'Torque updated'
            return response
        except Exception as e:
            self.get_logger().error(f"SetTorque service error: {e}")
            response.success = False
            response.message = str(e)
            return response

    def reconnect_ports_callback(self, request, response):
        self.get_logger().info("Reconnecting ports...")
        global DEVICE_NAME0, DEVICE_NAME1, DEVICE_NAME2
        global PORT0, PORT1, PORT2
        global port_handler0, port_handler1, port_handler2
        global groupSyncWrite0, groupSyncWrite1, groupSyncWrite2
        global groupSyncRead0_pos, groupSyncRead1_pos, groupSyncRead2_pos
        global groupSyncRead0_temp, groupSyncRead1_temp, groupSyncRead2_temp
        global groupSyncRead0_current, groupSyncRead1_current, groupSyncRead2_current
        global groupSyncRead0_load, groupSyncRead1_load, groupSyncRead2_load
        global groupSyncRead0_error, groupSyncRead1_error, groupSyncRead2_error

        if self.port0_open:
            port_handler0.closePort()
        if self.port1_open:
            port_handler1.closePort()
        if getattr(self, "port2_open", False):
            port_handler2.closePort()
            
        import glob
        available_ports = sorted(glob.glob('/dev/ttyUSB*') + glob.glob('/dev/ttyACM*'))
        DEVICE_NAME0 = available_ports[0] if len(available_ports) > 0 else "/dev/ttyUSB0"
        DEVICE_NAME1 = available_ports[1] if len(available_ports) > 1 else "/dev/ttyUSB1"
        DEVICE_NAME2 = available_ports[2] if len(available_ports) > 2 else "/dev/ttyUSB2"
        
        # Recreate port handlers so the Dynamixel SDK picks up the new device names
        port_handler0 = PortHandler(DEVICE_NAME0)
        port_handler1 = PortHandler(DEVICE_NAME1)
        port_handler2 = PortHandler(DEVICE_NAME2)
        groupSyncWrite0 = GroupSyncWrite(port_handler0, packet_handler, ADDR_GOAL_POSITION, LEN_GOAL_POSITION)
        groupSyncWrite1 = GroupSyncWrite(port_handler1, packet_handler, ADDR_GOAL_POSITION, LEN_GOAL_POSITION)
        groupSyncWrite2 = GroupSyncWrite(port_handler2, packet_handler, ADDR_GOAL_POSITION, LEN_GOAL_POSITION)
        groupSyncRead0_pos = GroupSyncRead(port_handler0, packet_handler, ADDR_PRESENT_POSITION, LEN_PRESENT_POSITION)
        groupSyncRead1_pos = GroupSyncRead(port_handler1, packet_handler, ADDR_PRESENT_POSITION, LEN_PRESENT_POSITION)
        groupSyncRead2_pos = GroupSyncRead(port_handler2, packet_handler, ADDR_PRESENT_POSITION, LEN_PRESENT_POSITION)
        groupSyncRead0_temp = GroupSyncRead(port_handler0, packet_handler, ADDR_PRESENT_TEMPERATURE, LEN_PRESENT_TEMPERATURE)
        groupSyncRead1_temp = GroupSyncRead(port_handler1, packet_handler, ADDR_PRESENT_TEMPERATURE, LEN_PRESENT_TEMPERATURE)
        groupSyncRead2_temp = GroupSyncRead(port_handler2, packet_handler, ADDR_PRESENT_TEMPERATURE, LEN_PRESENT_TEMPERATURE)
        groupSyncRead0_current = GroupSyncRead(port_handler0, packet_handler, ADDR_PRESENT_CURRENT, LEN_PRESENT_CURRENT)
        groupSyncRead1_current = GroupSyncRead(port_handler1, packet_handler, ADDR_PRESENT_CURRENT, LEN_PRESENT_CURRENT)
        groupSyncRead2_current = GroupSyncRead(port_handler2, packet_handler, ADDR_PRESENT_CURRENT, LEN_PRESENT_CURRENT)
        groupSyncRead0_load = GroupSyncRead(port_handler0, packet_handler, ADDR_PRESENT_LOAD, LEN_PRESENT_LOAD)
        groupSyncRead1_load = GroupSyncRead(port_handler1, packet_handler, ADDR_PRESENT_LOAD, LEN_PRESENT_LOAD)
        groupSyncRead2_load = GroupSyncRead(port_handler2, packet_handler, ADDR_PRESENT_LOAD, LEN_PRESENT_LOAD)
        groupSyncRead0_error = GroupSyncRead(port_handler0, packet_handler, ADDR_HARDWARE_ERROR_STATUS, LEN_HARDWARE_ERROR)
        groupSyncRead1_error = GroupSyncRead(port_handler1, packet_handler, ADDR_HARDWARE_ERROR_STATUS, LEN_HARDWARE_ERROR)
        groupSyncRead2_error = GroupSyncRead(port_handler2, packet_handler, ADDR_HARDWARE_ERROR_STATUS, LEN_HARDWARE_ERROR)
        
        try:
            self.port0_open = port_handler0.openPort()
            if self.port0_open: port_handler0.setBaudRate(BAUDRATE)
        except Exception as e:
            self.get_logger().error(f"Error opening port0: {e}")
            self.port0_open = False
            
        try:
            self.port1_open = port_handler1.openPort()
            if self.port1_open: port_handler1.setBaudRate(BAUDRATE)
        except Exception as e:
            self.get_logger().error(f"Error opening port1: {e}")
            self.port1_open = False
            
        try:
            self.port2_open = port_handler2.openPort()
            if self.port2_open: port_handler2.setBaudRate(BAUDRATE)
        except Exception as e:
            self.get_logger().error(f"Error opening port2: {e}")
            self.port2_open = False
            
        PORT0.clear()
        PORT1.clear()
        PORT2.clear()
        
        self.simulation = not (self.port0_open or self.port1_open or self.port2_open)
        
        if self.port0_open or self.port1_open or self.port2_open:
            scan_motors(self.port0_open, self.port1_open, self.port2_open)
            try:
                initialize_motor()
            except Exception as e:
                self.get_logger().error(f"Initialize failed: {e}")
            response.success = True
            response.message = (
                f"Connected P0: {DEVICE_NAME0} ({self.port0_open}), "
                f"P1: {DEVICE_NAME1} ({self.port1_open}), "
                f"P2: {DEVICE_NAME2} ({self.port2_open})"
            )
        else:
            response.success = False
            response.message = "Failed to connect to any port. Running in simulation mode."
            
        return response
    
    def _bulk_read_motor_states(self, requested_ids):
        """Optimized bulk reading using GroupSyncRead (Interleaved)"""
        ids, positions, temperatures, torques, error_statuses = [], [], [], [], []
        
        # Separate motors by port
        port0_motors = [mid for mid in requested_ids if mid in PORT0]
        port1_motors = [mid for mid in requested_ids if mid in PORT1]
        port2_motors = [mid for mid in requested_ids if mid in PORT2]
        
        # Determine what to read in this cycle (Round Robin)
        # Cycle 0: Position + Temperature
        # Cycle 1: Position + Current (Torque)
        # Cycle 2: Position + Hardware Error
        current_phase = self.read_cycle % 3
        self.read_cycle += 1
        
        # Read actual position from hardware using GroupSyncRead
        pos_data = self._bulk_read_parameter(
            port0_motors,
            port1_motors,
            port2_motors,
            groupSyncRead0_pos,
            groupSyncRead1_pos,
            groupSyncRead2_pos,
            ADDR_PRESENT_POSITION,
            LEN_PRESENT_POSITION,
        )

        # --- Interleaved Reads (cycle-based to avoid bus congestion) ---
        temp_data = {}
        torque_data = {}
        error_data = {}
        
        if current_phase == 0:
            # Read Temperature
            temp_data = self._bulk_read_parameter(
                port0_motors,
                port1_motors,
                port2_motors,
                groupSyncRead0_temp,
                groupSyncRead1_temp,
                groupSyncRead2_temp,
                ADDR_PRESENT_TEMPERATURE,
                LEN_PRESENT_TEMPERATURE,
            )
        elif current_phase == 1:
            # Read Torque (Current/Load)
            torque_data = self._bulk_read_parameter(
                port0_motors,
                port1_motors,
                port2_motors,
                groupSyncRead0_current,
                groupSyncRead1_current,
                groupSyncRead2_current,
                ADDR_PRESENT_CURRENT,
                LEN_PRESENT_CURRENT,
            )
            
            if not torque_data and (port0_motors or port1_motors or port2_motors):
                self.get_logger().debug("PRESENT_CURRENT failed, trying PRESENT_LOAD")
                torque_data = self._bulk_read_parameter(
                    port0_motors,
                    port1_motors,
                    port2_motors,
                    groupSyncRead0_load,
                    groupSyncRead1_load,
                    groupSyncRead2_load,
                    ADDR_PRESENT_LOAD,
                    LEN_PRESENT_LOAD,
                )
        elif current_phase == 2:
            # Read Hardware Error
            error_data = self._bulk_read_parameter(
                port0_motors,
                port1_motors,
                port2_motors,
                groupSyncRead0_error,
                groupSyncRead1_error,
                groupSyncRead2_error,
                ADDR_HARDWARE_ERROR_STATUS,
                LEN_HARDWARE_ERROR,
            )
        
        # Combine data (Use read values OR cached values)
        for motor_id in requested_ids:
            if motor_id in pos_data: # If we can't even get position, skip this motor for now
                ids.append(motor_id)
                positions.append(pos_data[motor_id])
                
                # --- Temperature ---
                if motor_id in temp_data:
                    temperatures.append(temp_data[motor_id])
                else:
                    cached = self.motor_states_cache.get(motor_id, {})
                    temperatures.append(cached.get('temperature', 25))
                
                # --- Torque ---
                if motor_id in torque_data:
                    raw_torque = torque_data[motor_id]
                    # Convert 2-byte signed integer to mA (milliamperes)
                    if raw_torque > 32767:  # Handle negative values
                        torque_value = raw_torque - 65536
                    else:
                        torque_value = raw_torque
                    
                    # Convert to milliamperes (mA) and use absolute value
                    torque_mA = abs(torque_value)  # Direct mA value for PRESENT_CURRENT
                    torques.append(torque_mA)
                    self.get_logger().debug(f"Motor {motor_id} torque: raw={raw_torque}, mA={torque_mA}")
                else:
                    cached = self.motor_states_cache.get(motor_id, {})
                    torques.append(cached.get('torque', 0))
                    self.get_logger().debug(f"Motor {motor_id} torque: using cached/default value")
                
                # --- Error ---
                if motor_id in error_data:
                    error_byte = error_data[motor_id]
                    error_list = self._parse_hardware_error(error_byte)
                    error_status = ",".join(error_list)
                    error_statuses.append(error_status)
                    if error_status != "NO_ERROR":
                        self.get_logger().warn(f"Motor {motor_id} error: {error_status}")
                else:
                    cached = self.motor_states_cache.get(motor_id, {})
                    error_statuses.append(cached.get('error_status', 'NO_ERROR'))
                    
            else:
                self.get_logger().warn(f"Failed to read motor {motor_id}")
        
        return ids, positions, temperatures, torques, error_statuses
    
    def _bulk_read_parameter(self, port0_motors, port1_motors, port2_motors,
                             sync_read0, sync_read1, sync_read2, addr, length):
        """Helper method for bulk parameter reading"""
        result_data = {}
        
        # Setup and read from port0
        if port0_motors:
            sync_read0.clearParam()
            for motor_id in port0_motors:
                sync_read0.addParam(motor_id)
            try:
                result = sync_read0.txRxPacket()
            except SerialException as exc:
                self.get_logger().error(f"Port0 sync-read failed: {exc}")
                result = None
            if result == COMM_SUCCESS:
                for motor_id in port0_motors:
                    if sync_read0.isAvailable(motor_id, addr, length):
                        result_data[motor_id] = sync_read0.getData(motor_id, addr, length)
        
        # Setup and read from port1  
        if port1_motors:
            sync_read1.clearParam()
            for motor_id in port1_motors:
                sync_read1.addParam(motor_id)
            try:
                result = sync_read1.txRxPacket()
            except SerialException as exc:
                self.get_logger().error(f"Port1 sync-read failed: {exc}")
                result = None
            if result == COMM_SUCCESS:
                for motor_id in port1_motors:
                    if sync_read1.isAvailable(motor_id, addr, length):
                        result_data[motor_id] = sync_read1.getData(motor_id, addr, length)

        # Setup and read from port2
        if port2_motors:
            sync_read2.clearParam()
            for motor_id in port2_motors:
                sync_read2.addParam(motor_id)
            try:
                result = sync_read2.txRxPacket()
            except SerialException as exc:
                self.get_logger().error(f"Port2 sync-read failed: {exc}")
                result = None
            if result == COMM_SUCCESS:
                for motor_id in port2_motors:
                    if sync_read2.isAvailable(motor_id, addr, length):
                        result_data[motor_id] = sync_read2.getData(motor_id, addr, length)
        
        return result_data
    
    def _individual_read_motor_states(self, requested_ids):
        """Fallback individual reading method"""
        ids, positions, temperatures, torques, error_statuses = [], [], [], [], []
        
        for motor_id in requested_ids:
            selected_port_handler = (
                port_handler0 if motor_id in PORT0
                else port_handler1 if motor_id in PORT1
                else port_handler2 if motor_id in PORT2
                else None
            )
            if selected_port_handler is None:
                continue

            try:
                # Read position
                position, comm_result, _ = packet_handler.read4ByteTxRx(selected_port_handler, motor_id, ADDR_PRESENT_POSITION)
                if comm_result != COMM_SUCCESS:
                    position = self.motor_limits.get(f"{motor_id}", {}).get("ini", 0)

                # Read temperature
                temperature, comm_result, _ = packet_handler.read1ByteTxRx(selected_port_handler, motor_id, ADDR_PRESENT_TEMPERATURE)
                if comm_result != COMM_SUCCESS:
                    cached = self.motor_states_cache.get(motor_id, {})
                    temperature = cached.get('temperature', 25)

                # Read torque - try PRESENT_CURRENT first, then PRESENT_LOAD
                torque, comm_result, _ = packet_handler.read2ByteTxRx(selected_port_handler, motor_id, ADDR_PRESENT_CURRENT)
                if comm_result != COMM_SUCCESS:
                    self.get_logger().debug(f"Motor {motor_id}: PRESENT_CURRENT failed, trying PRESENT_LOAD")
                    torque, comm_result, _ = packet_handler.read2ByteTxRx(selected_port_handler, motor_id, ADDR_PRESENT_LOAD)
                    
                if comm_result != COMM_SUCCESS:
                    cached = self.motor_states_cache.get(motor_id, {})
                    torque = cached.get('torque', 0)
                else:
                    # Convert 2-byte signed integer to mA
                    if torque > 32767:
                        torque = torque - 65536
                    torque_mA = abs(torque)  # Convert to mA and use absolute value
                    torque = torque_mA
                    self.get_logger().debug(f"Motor {motor_id} individual read torque: {torque_mA}mA")
                
                # Read hardware error status
                error_byte, comm_result, _ = packet_handler.read1ByteTxRx(selected_port_handler, motor_id, ADDR_HARDWARE_ERROR_STATUS)
                if comm_result != COMM_SUCCESS:
                    cached = self.motor_states_cache.get(motor_id, {})
                    error_status = cached.get('error_status', 'NO_ERROR')
                else:
                    error_list = self._parse_hardware_error(error_byte)
                    error_status = ",".join(error_list)
                    if error_status != "NO_ERROR":
                        self.get_logger().warn(f"Motor {motor_id} error: {error_status}")

            except SerialException as exc:
                self.get_logger().error(f"Serial read failed for motor {motor_id}: {exc}")
                position = self.motor_limits.get(f"{motor_id}", {}).get("ini", 0)
                temperature = 0
                torque = 0
                error_status = "SERIAL_ERROR"
            
            positions.append(position)
            temperatures.append(temperature)
            torques.append(torque)
            error_statuses.append(error_status)
            ids.append(motor_id)

        return ids, positions, temperatures, torques, error_statuses
    
    def _calculate_total_currents(self, ids, torques):
        """Calculate total currents for each port and system"""
        port0_total = 0
        port1_total = 0
        port2_total = 0
        
        for i, motor_id in enumerate(ids):
            torque_value = torques[i] if i < len(torques) else 0
            
            if motor_id in PORT0:
                port0_total += torque_value
            elif motor_id in PORT1:
                port1_total += torque_value
            elif motor_id in PORT2:
                port2_total += torque_value
        
        system_total = port0_total + port1_total + port2_total
        
        self.get_logger().debug(
            f"Current totals - PORT0: {port0_total}mA, PORT1: {port1_total}mA, "
            f"PORT2: {port2_total}mA, System: {system_total}mA"
        )
        
        return port0_total, port1_total, system_total
    
    def _parse_hardware_error(self, error_status):
        """Parse Dynamixel hardware error status byte"""
        errors = []
        if error_status & 0x01:  # Bit 0
            errors.append("INPUT_VOLTAGE")
        if error_status & 0x04:  # Bit 2  
            errors.append("OVERHEATING")
        if error_status & 0x08:  # Bit 3
            errors.append("MOTOR_ENCODER")
        if error_status & 0x10:  # Bit 4
            errors.append("ELECTRICAL_SHOCK")
        if error_status & 0x20:  # Bit 5
            errors.append("OVERLOAD")
        
        return errors if errors else ["NO_ERROR"]

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
    limits_path = os.path.expanduser("~/CS_Animatronics/Motor_Limits.json")
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
    
    # Create valid list of all detected motors
    all_detected_ids = sorted(list(set(PORT0) | set(PORT1) | set(PORT2)))
    
    for motor_id in all_detected_ids:
        if motor_id in PORT0:
            selected_port_handler = port_handler0
        elif motor_id in PORT1:
            selected_port_handler = port_handler1
        elif motor_id in PORT2:
            selected_port_handler = port_handler2
        else:
            print(f"Motor ID {motor_id} not found on any port.")
            continue

        print(f"\nInitializing motor {motor_id} on")
        
        # Check if motor exists in configuration
        is_configured = f"{motor_id}" in motor_limits
        
        # 1. Disable Torque
        set_motor1(selected_port_handler, motor_id, ADDR_TORQUE_ENABLE, 0)
        sleep(0.1)
        
        # 2. Operating Mode (3: Position Control)
        set_motor1(selected_port_handler, motor_id, ADDR_OPERATING_MODE, 3)
        sleep(0.1)
        
        if is_configured:
            # Full initialization for known motors
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
        else:
            # Minimal initialization for unknown/detected motors
            print(f"[Warn] Motor {motor_id} is not in Motor_Limits.json. Enabling torque with default settings.")
            # LED only (skip profile/limits to avoid errors)
        
        # 3. Enable Torque
        set_motor1(selected_port_handler, motor_id, ADDR_TORQUE_ENABLE, 1)
        sleep(0.1)

        # 4. After torque is back on, command the ini pose again so the joint moves away from its slack position
        if is_configured:
            set_motor4(selected_port_handler, motor_id, ADDR_GOAL_POSITION, motor_limits[f"{motor_id}"]["ini"])
            sleep(0.1)
        
        # 5. LED
        set_motor1(selected_port_handler, motor_id, ADDR_LED, 1)
        sleep(0.1)
        
        print(f"Finished initializing motor {motor_id}")
    print("Finished initializing motors")

def scan_motors(port0_open, port1_open, port2_open):
    """Scan for motors. Phase 1: ping only known MOTOR_IDS (fast, with retry
    for motors still booting). Phase 2: full range for any undocumented IDs."""
    MAX_RETRIES = 2
    RETRY_DELAY = 1.5  # seconds between retries for known IDs

    def _ping_with_retry(port_handler, motor_id):
        for attempt in range(MAX_RETRIES):
            _, comm_result, _ = packet_handler.ping(port_handler, motor_id)
            if comm_result == COMM_SUCCESS:
                return True
            if attempt < MAX_RETRIES - 1:
                sleep(RETRY_DELAY)
        return False

    try:
        # Phase 1: scan known Motor IDs on both ports (with retry)
        print("\n[Scan] Phase 1 – known IDs (with retry for late-booting motors)")
        for motor_id in MOTOR_IDS:
            found = False
            if port0_open and _ping_with_retry(port_handler0, motor_id):
                PORT0.append(motor_id)
                print(f"  ID {motor_id:>3} -> PORT0")
                found = True
            elif port1_open and _ping_with_retry(port_handler1, motor_id):
                PORT1.append(motor_id)
                print(f"  ID {motor_id:>3} -> PORT1")
                found = True
            elif port2_open and _ping_with_retry(port_handler2, motor_id):
                PORT2.append(motor_id)
                print(f"  ID {motor_id:>3} -> PORT2")
                found = True
            if not found:
                print(f"  ID {motor_id:>3} -> NOT FOUND (check hardware)")

        # Phase 2: full range to catch undocumented IDs (no retry, fast)
        print("\n[Scan] Phase 2 – full range for unknown IDs")
        for motor_id in range(1, 254):
            if motor_id in PORT0 or motor_id in PORT1 or motor_id in PORT2 or motor_id in MOTOR_IDS:
                continue
            if port0_open:
                _, r0, _ = packet_handler.ping(port_handler0, motor_id)
                if r0 == COMM_SUCCESS:
                    PORT0.append(motor_id)
                    print(f"  Unknown ID {motor_id} -> PORT0")
                    continue
            if port1_open:
                _, r1, _ = packet_handler.ping(port_handler1, motor_id)
                if r1 == COMM_SUCCESS:
                    PORT1.append(motor_id)
                    print(f"  Unknown ID {motor_id} -> PORT1")
                    continue
            if port2_open:
                _, r2, _ = packet_handler.ping(port_handler2, motor_id)
                if r2 == COMM_SUCCESS:
                    PORT2.append(motor_id)
                    print(f"  Unknown ID {motor_id} -> PORT2")

        print(f"\n[Scan] Final PORT0: {sorted(PORT0)}")
        print(f"[Scan] Final PORT1: {sorted(PORT1)}")
        print(f"[Scan] Final PORT2: {sorted(PORT2)}")
        missing = [m for m in MOTOR_IDS if m not in PORT0 and m not in PORT1 and m not in PORT2]
        if missing:
            print(f"[Scan] WARNING – expected IDs not found: {missing}")

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

    try:
        port2_open = port_handler2.openPort()
    except Exception as e:
        print(f"Exception opening port2: {e}")
        port2_open = False

    if not port2_open:
        print("Failed to open port2. Running in simulation mode.")

    # 各ポートがオープンしている場合のみbaudrate設定
    if port0_open:
        if not port_handler0.setBaudRate(BAUDRATE):
            print(f"Failed to set baudrate {BAUDRATE} on port0")
            port0_open = False
    if port1_open:
        if not port_handler1.setBaudRate(BAUDRATE):
            print(f"Failed to set baudrate {BAUDRATE} on port1")
            port1_open = False
    if port2_open:
        if not port_handler2.setBaudRate(BAUDRATE):
            print(f"Failed to set baudrate {BAUDRATE} on port2")
            port2_open = False

    if port0_open or port1_open or port2_open:
        print(f"Baudrate set to {BAUDRATE} on available ports.")
        scan_motors(port0_open, port1_open, port2_open)
        try:
            initialize_motor()
        except Exception as e:
            print(f"Motor initialization failed: {e}")
    else:
        print("One or more ports not open; operating in simulation mode.")

    rclpy.init(args=args)
    node = MotorController(port0_open, port1_open, port2_open)
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
            elif motor_id in PORT2:
                selected_port_handler = port_handler2
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
        if port2_open:
            port_handler2.closePort()

if __name__ == "__main__":
    main()

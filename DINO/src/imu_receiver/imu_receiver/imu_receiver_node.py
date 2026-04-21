#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2024 Ryo Isogawa
# SPDX-License-Identifier: BSD-3-Clause

import math
import serial
import struct
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu
import glob
import time


class IMUReceiver:
    HEADER = b'\xAA\x55'
    FOOTER = b'\x55\xAA'
    # 2(header) + 1(count) + (1 + 9*4)*3 + 2(footer) = 116 bytes
    PACKET_SIZE = 116

    PACKET_SIZE = 116

    def __init__(self, baudrate=115200):
        self.baudrate = baudrate
        self.ser = None
        self.connected = False
        self.buffer = b''
        # Each element is a dict with keys: euler, accel, gyro
        self.data = [
            {'euler': None, 'accel': None, 'gyro': None} for _ in range(3)
        ]
        
    def find_and_connect(self):
        # Candidate patterns for macOS and Linux
        patterns = ['/dev/ttyACM*', '/dev/ttyUSB*', '/dev/cu.usbmodem*', '/dev/tty.usbmodem*', '/dev/cu.usbserial*']
        candidates = []
        for p in patterns:
            candidates.extend(glob.glob(p))
            
        # Avoid known devices if necessary (e.g. bluetooth)
        candidates = [c for c in candidates if "Bluetooth" not in c and "Bose" not in c and "debug" not in c]
        
        for port in candidates:
            try:
                print(f"Checking port: {port}")
                ser = serial.Serial(port, self.baudrate, timeout=0.1)
                
                # Handshake: Look for header
                # We wait for a bit to receive data
                end_time = time.time() + 1.5
                found_header = False
                temp_buffer = b''
                
                while time.time() < end_time:
                    if ser.in_waiting > 0:
                        temp_buffer += ser.read(ser.in_waiting)
                        if self.HEADER in temp_buffer:
                            found_header = True
                            break
                    time.sleep(0.05)
                
                if found_header:
                    print(f"Connected to IMU on {port}")
                    self.ser = ser
                    self.ser.timeout = 1 # Restore normal timeout
                    self.connected = True
                    self.buffer = b''
                    return True
                else:
                    ser.close()
            except Exception as e:
                pass
                
        return False

    def update(self):
        if not self.connected:
            self.find_and_connect()
            return

        try:
            if self.ser.in_waiting > 0:
                self.buffer += self.ser.read(self.ser.in_waiting)
                
            latest_packet = None
            while len(self.buffer) >= self.PACKET_SIZE:
                start = self.buffer.find(self.HEADER)
                # If header not found or too far, trim
                if start == -1:
                     # Keep last byte just in case it's part of header
                    self.buffer = self.buffer[-1:]
                    break
                
                # If header is found but not at start, discard garbage before it
                if start > 0:
                    self.buffer = self.buffer[start:]
                    start = 0
                    
                # Check for footer
                if len(self.buffer) < self.PACKET_SIZE:
                    break
                    
                end = start + self.PACKET_SIZE - 2
                
                if self.buffer[end:end+2] == self.FOOTER:
                    packet = self.buffer[start:end + 2]
                    self.buffer = self.buffer[end + 2:]
                    latest_packet = packet
                else:
                    # Invalid packet (header found but footer mismatch), move forward
                    self.buffer = self.buffer[2:]
            
            if latest_packet:
                self._parse_packet(latest_packet)
                
        except Exception as e:
            print(f"Connection lost: {e}")
            self.connected = False
            if self.ser:
                try:
                    self.ser.close()
                except:
                    pass
            self.ser = None

    def _parse_packet(self, packet):
        if packet[:2] != self.HEADER or packet[-2:] != self.FOOTER:
            return
        count = packet[2]
        offset = 3
        for _ in range(count):
            unpacked = struct.unpack_from("<Bfffffffff", packet, offset)
            ch = unpacked[0]
            if 0 <= ch < 3:
                self.data[ch] = {
                    'euler': unpacked[1:4],
                    'accel': unpacked[4:7],
                    'gyro': unpacked[7:10],
                }
            offset += 37

    def get_data(self):
        return self.data


def euler_to_quaternion(heading, roll, pitch):
    h = math.radians(heading) * 0.5
    r = math.radians(roll) * 0.5
    p = math.radians(pitch) * 0.5

    cy = math.cos(h)
    sy = math.sin(h)
    cr = math.cos(r)
    sr = math.sin(r)
    cp = math.cos(p)
    sp = math.sin(p)

    qw = cr * cp * cy + sr * sp * sy
    qx = sr * cp * cy - cr * sp * sy
    qy = cr * sp * cy + sr * cp * sy
    qz = cr * cp * sy - sr * sp * cy
    return qx, qy, qz, qw


class IMUPublisher(Node):
    def __init__(self):
        super().__init__('imu_publisher')
        self.receiver = IMUReceiver()
        # Avoid name collision with the Node.publishers property
        self.imu_publishers = [
            self.create_publisher(Imu, f'imu{i}', 10) for i in range(3)
        ]
        self.timer = self.create_timer(0.02, self.timer_callback)
        self.get_logger().info('IMU publisher node started')

    def timer_callback(self):
        self.receiver.update()
        data = self.receiver.get_data()
        for i, sensor in enumerate(data):
            if sensor is None:
                continue
            euler = sensor.get('euler')
            if euler is None or not all(math.isfinite(v) for v in euler):
                continue
            accel = sensor.get('accel')
            gyro = sensor.get('gyro')

            qx, qy, qz, qw = euler_to_quaternion(*euler)
            msg = Imu()
            msg.orientation.x = qx
            msg.orientation.y = qy
            msg.orientation.z = qz
            msg.orientation.w = qw

            if accel and all(math.isfinite(v) for v in accel):
                msg.linear_acceleration.x = accel[0]
                msg.linear_acceleration.y = accel[1]
                msg.linear_acceleration.z = accel[2]
            if gyro and all(math.isfinite(v) for v in gyro):
                msg.angular_velocity.x = gyro[0]
                msg.angular_velocity.y = gyro[1]
                msg.angular_velocity.z = gyro[2]

            self.imu_publishers[i].publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = IMUPublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

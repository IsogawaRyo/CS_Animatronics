#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2024 Ryo Isogawa
# SPDX-License-Identifier: BSD-3-Clause

import math
import serial
import struct
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu


class IMUReceiver:
    HEADER = b'\xAA\x55'
    FOOTER = b'\x55\xAA'
    PACKET_SIZE = 44  # 2(header) + 1 + (13*3) + 2(footer)

    def __init__(self, port='/dev/ttyACM1', baudrate=115200):
        self.ser = serial.Serial(port, baudrate, timeout=1)
        self.buffer = b''
        self.data = [None, None, None]

    def update(self):
        self.buffer += self.ser.read(128)
        latest_packet = None
        while len(self.buffer) >= self.PACKET_SIZE:
            start = self.buffer.find(self.HEADER)
            end = self.buffer.find(self.FOOTER, start + 1)
            if start != -1 and end != -1 and (end + 2 - start) == self.PACKET_SIZE:
                packet = self.buffer[start:end + 2]
                self.buffer = self.buffer[end + 2:]
                latest_packet = packet
            else:
                self.buffer = self.buffer[1:]
        if latest_packet:
            self._parse_packet(latest_packet)

    def _parse_packet(self, packet):
        if packet[:2] != self.HEADER or packet[-2:] != self.FOOTER:
            return
        count = packet[2]
        offset = 3
        for _ in range(count):
            ch, heading, roll, pitch = struct.unpack_from("<Bfff", packet, offset)
            if 0 <= ch < 3:
                self.data[ch] = (heading, roll, pitch)
            offset += 13

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
        for i, euler in enumerate(data):
            if euler is None:
                continue
            heading, roll, pitch = euler
            if not all(math.isfinite(v) for v in (heading, roll, pitch)):
                continue
            qx, qy, qz, qw = euler_to_quaternion(heading, roll, pitch)
            msg = Imu()
            msg.orientation.x = qx
            msg.orientation.y = qy
            msg.orientation.z = qz
            msg.orientation.w = qw
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

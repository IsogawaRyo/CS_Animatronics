import serial

import struct

import numpy as np

import matplotlib.pyplot as plt

from mpl_toolkits.mplot3d import Axes3D
 
class IMUReceiver:

    HEADER = b'\xAA\x55'

    FOOTER = b'\x55\xAA'

    PACKET_SIZE = 44  # 2(header) + 1 + (13*3) + 2(footer)
 
    def __init__(self, port='/dev/ttyACM1', baudrate=115200):

        self.ser = serial.Serial(port, baudrate, timeout=1)

        self.buffer = b''

        self.data = [None, None, None]
 
    def update(self):

        self.buffer += self.ser.read(128)  # read a chunk

        latest_packet = None
 
        while len(self.buffer) >= self.PACKET_SIZE:

            start = self.buffer.find(self.HEADER)

            end = self.buffer.find(self.FOOTER, start + 1)
 
            if start != -1 and end != -1 and (end + 2 - start) == self.PACKET_SIZE:

                packet = self.buffer[start:end + 2]

                self.buffer = self.buffer[end + 2:]

                latest_packet = packet  # ← 上書きして最新だけ残す

            else:

                self.buffer = self.buffer[1:]  # shift buffer if unsynced
 
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
 
class IMUVisualizer:

    def __init__(self):

        plt.ion()

        self.fig = plt.figure()

        self.ax = self.fig.add_subplot(111, projection='3d')

        self.positions = [(-2, 0, 0), (0, 0, 0), (2, 0, 0)]
 
    def euler_to_matrix(self, heading, roll, pitch):

        if not all(np.isfinite([heading, roll, pitch])):

            return np.identity(3)

        h, r, p = np.radians([heading, roll, pitch])

        Rz = np.array([

            [np.cos(h), -np.sin(h), 0],

            [np.sin(h),  np.cos(h), 0],

            [0, 0, 1]

        ])

        Ry = np.array([

            [np.cos(p), 0, np.sin(p)],

            [0, 1, 0],

            [-np.sin(p), 0, np.cos(p)]

        ])

        Rx = np.array([

            [1, 0, 0],

            [0, np.cos(r), -np.sin(r)],

            [0, np.sin(r),  np.cos(r)]

        ])

        return Rz @ Ry @ Rx
 
    def draw_cube(self, center, rotation, size=0.5):

        r = size / 2

        corners = np.array([

            [-r, -r, -r], [ r, -r, -r], [ r,  r, -r], [-r,  r, -r],

            [-r, -r,  r], [ r, -r,  r], [ r,  r,  r], [-r,  r,  r],

        ])

        rotated = (rotation @ corners.T).T + center

        edges = [

            [0,1], [1,2], [2,3], [3,0],

            [4,5], [5,6], [6,7], [7,4],

            [0,4], [1,5], [2,6], [3,7],

        ]

        for edge in edges:

            self.ax.plot(*zip(rotated[edge[0]], rotated[edge[1]]), color='blue')
 
    def update(self, all_data):

        self.ax.cla()

        self.ax.set_xlim([-3, 3])

        self.ax.set_ylim([-3, 3])

        self.ax.set_zlim([-3, 3])

        self.ax.set_title("BNO055 Orientation (Latest Only)")
 
        for i, euler in enumerate(all_data):

            if euler:

                h, r, p = euler

                matrix = self.euler_to_matrix(h, r, p)

                center = np.array(self.positions[i])

                self.draw_cube(center, matrix)

                label = f"CH{i}\nH:{h:.1f}\nR:{r:.1f}\nP:{p:.1f}"

                self.ax.text(center[0], center[1], center[2] + 1.0, label, fontsize=9, color='black')
 
        plt.draw()

        plt.pause(0.01)
 
if __name__ == '__main__':

    receiver = IMUReceiver()

    visualizer = IMUVisualizer()

    print("🛰️  Receiving latest BNO055 data from Pico...")
 
    try:

        while True:

            receiver.update()

            visualizer.update(receiver.get_data())

    except KeyboardInterrupt:

        print("終了")

 

import time
import board
import busio
import adafruit_bno055
import adafruit_tca9548a
import usb_cdc
import struct

# I2C初期化（GP1=SCL, GP0=SDA）
i2c = busio.I2C(board.GP1, board.GP0)

# TCA9548A初期化（I2Cマルチプレクサ）
tca = adafruit_tca9548a.TCA9548A(i2c)

# BNO055を3チャンネルから取得
sensors = []
for i in range(3):
    try:
        sensors.append(adafruit_bno055.BNO055_I2C(tca[i]))
    except ValueError:
        sensors.append(None)

# データ送信ループ
while True:
    for ch, sensor in enumerate(sensors):
        if sensor is None:
            continue
        euler = sensor.euler
        if euler is not None:
            heading, roll, pitch = euler
            packet = struct.pack("<Bfff", ch, heading, roll, pitch)
            usb_cdc.data.write(packet)
    time.sleep(0.05)


import time
import board
import busio
import struct
import usb_cdc
import adafruit_bno055
import adafruit_tca9548a

# I2C 初期化
i2c = busio.I2C(board.GP1, board.GP0)
tca = adafruit_tca9548a.TCA9548A(i2c)

# BNO055 センサー初期化（CH0〜CH2）
sensors = []
for i in range(3):
    try:
        sensor = adafruit_bno055.BNO055_I2C(tca[i])
        time.sleep(0.2)
        sensors.append(sensor)
    except ValueError:
        sensors.append(None)

# データ送信ループ
while True:
    packet = bytearray()
    packet += b'\xAA\x55'  # ヘッダー
    packet += struct.pack("<B", 3)  # センサ数

    for ch, sensor in enumerate(sensors):
        def safe_tuple(value, length):
            return tuple(v if v is not None else float('nan') for v in (value or (float('nan'),)*length))

        if sensor is None:
            data = [float('nan')] * 9
        else:
            euler = safe_tuple(sensor.euler, 3)
            accel = safe_tuple(sensor.acceleration, 3)
            gyro  = safe_tuple(sensor.gyro, 3)
            data = list(euler) + list(accel) + list(gyro)

        # ch + 9 float = 1 + 36 byte
        packet += struct.pack("<B" + "f"*9, ch, *data)

    packet += b'\x55\xAA'  # フッター
    usb_cdc.data.write(packet)
    time.sleep(0.02)  # 約50Hz

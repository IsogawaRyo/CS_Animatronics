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
        sensor  = adafruit_bno055.BNO055_I2C(tca[i])
        time.sleep(0.2)  # 各センサごとに待機（安定化）
        sensors.append(sensor)
    except ValueError:
        sensors.append(None)

# データ送信ループ
while True:
    packet = bytearray()

    # ヘッダー
    packet += b'\xAA\x55'
    packet += struct.pack("<B", 3)  # センサ数

    # 各センサデータ
    for ch, sensor in enumerate(sensors):
        if sensor is None:
            # センサがない場合は NaN を送る
            packet += struct.pack("<Bfff", ch, float('nan'), float('nan'), float('nan'))
        else:
            euler = sensor.euler
            if euler is not None:
                heading, roll, pitch = euler
                packet += struct.pack("<Bfff", ch, heading, roll, pitch)
            else:
                packet += struct.pack("<Bfff", ch, float('nan'), float('nan'), float('nan'))

    # フッター
    packet += b'\x55\xAA'

    # USBに送信
    usb_cdc.data.write(packet)

    # 少し待機（調整可）
    time.sleep(0.02)


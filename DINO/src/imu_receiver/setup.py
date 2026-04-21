from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'imu_receiver'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools', 'rclpy', 'sensor_msgs', 'pyserial'],
    zip_safe=True,
    maintainer='Ryo Isogawa',
    maintainer_email='2023m002@kuas.ac.jp',
    description='ROS2 node for publishing BNO055 IMU data',
    license='BSD-3-Clause',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'imu_receiver = imu_receiver.imu_receiver_node:main',
        ],
    },
)

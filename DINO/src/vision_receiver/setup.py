from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'vision_receiver'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools', 'opencv-python', 'cv-bridge'],
    zip_safe=True,
    maintainer='isogawaryo',
    maintainer_email='isogawaryo@todo.todo',
    description='Receives stereo video streams from Raspberry Pi Zero cameras',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'vision_receiver_node = vision_receiver.vision_receiver_node:main',
        ],
    },
)

# CS_Animatronics
Practice for ROS2. 

Raspberry Pi 5 8GB with Ubuntu is used.
We use DualeSence for controlling a robot.
XL430 and XL330 are used.

# Description of nodes
## 👨‍💻system_controller
A system_controller is ROS2 node that subscribes Joy message and publishes IdAngle.

## 👨‍🔧motor_controller
A motor_controller is ROS2 node that subscribes IdAngle message and Angle and operate motors safely.
As a initialization, this node searches motors on /dev/ttyUSB0 and /dev/ttyUSB1 and creates list of IDs for each port.

## 🎮controller_publisher
A controller_publisher is ROS2 node that receives signals from DualScence and publish Joy message.

# Descriptions of messages
## IdAngle
id: uint8[10], angle: int32[10]

## SetPositions
id: uint8, position: int32

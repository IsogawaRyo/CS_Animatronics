# CS_Animatronics
Practice for ROS2. 

# Description of nodes
## system_controller
A system_controller is ROS2 node that subscribes Joy message and publishes IdAngle.

## motor_controller
A motor_controller is ROS2 node that subscribes IdAngle message and Angle and operate motors safely.

## controller_publisher
A controller_publisher is ROS2 node that receives signals from DualScence and publish Joy message.

# Descriptions of messages
## IdAngle
id: uint8[10], angle: int32[10]

## SetPositions
id: uint8, position: int32

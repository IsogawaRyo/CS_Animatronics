# CS_Animatronics
Practice for ROS2. 

# Description of nodes
## system_controller
A system_controller is node that subscribes states of controller and publishes list of ID and Angle.

## motor_controller
A motor_controller is node that subscribes list of ID and Angle and operate motors safely.

## controller_publisher
A controller_publisher is node that receives signals from DualScence and publish state of buttons and angles of axes.

# Descriptions of messages
## IdAngle
id: uint8[10], angle: int32[10]

## SetPositions
id: uint8, position: int32

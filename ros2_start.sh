#!/bin/bash

source /opt/ros/jazzy/setup.bash

gnome-terminal -- bash -c "cd CS_Animatronics && rm -rf build log install && colcon build"

sleep 50

sudo -S usermod -aG dialout csanimatronics <<< "KUASECSA"

gnome-terminal -- bash -c "source ~/CS_Animatronics/install/setup.bash && source ~/CS_Animatronics/install/local_setup.bash && source ~/CS_Animatronics/install/setup.bash && ros2 run system_controller system_controller"

gnome-terminal -- bash -c "source ~/CS_Animatronics/install/setup.bash && source ~/CS_Animatronics/install/local_setup.bash && source ~/CS_Animatronics/install/setup.bash  && ros2 run controller_publisher controller_publisher"

gnome-terminal -- bash -c "source ~/CS_Animatronics/install/setup.bash && source ~/CS_Animatronics/install/local_setup.bash && source ~/CS_Animatronics/install/setup.bash  && sudo -S usermod -aG dialout csanimatronics <<< "KUASECSA" && ros2 run motor_controller motor_controller"

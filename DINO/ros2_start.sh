#!/bin/bash
DIR=$(cd $(dirname $0); pwd)

# Ensure fallback script is executable
chmod +x $DIR/sudo_fallback.sh

source /opt/ros/jazzy/setup.bash

gnome-terminal -- bash -c "cd $DIR && rm -rf build log install && export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin && colcon build --cmake-args -DPYTHON_EXECUTABLE=/usr/bin/python3 -DPython3_EXECUTABLE=/usr/bin/python3; read"

$DIR/sudo_fallback.sh "usermod -aG dialout cvl"

sleep 50

gnome-terminal -- bash -c "export DINO_ROOT_DIR=$DIR && source $DIR/install/setup.bash && source $DIR/install/local_setup.bash && source $DIR/install/setup.bash && ros2 run system_controller system_controller; read"

gnome-terminal -- bash -c "export DINO_ROOT_DIR=$DIR && source $DIR/install/setup.bash && source $DIR/install/local_setup.bash && source $DIR/install/setup.bash  && ros2 run controller_publisher controller_publisher; read"

gnome-terminal -- bash -c "export DINO_ROOT_DIR=$DIR && source $DIR/install/setup.bash && source $DIR/install/local_setup.bash && source $DIR/install/setup.bash && ros2 run system_controller trajectory_interpolator; read"

gnome-terminal -- bash -c "export DINO_ROOT_DIR=$DIR && source $DIR/install/setup.bash && source $DIR/install/local_setup.bash && source $DIR/install/setup.bash  && $DIR/sudo_fallback.sh \"usermod -aG dialout cvl\" && ros2 run motor_controller motor_controller; read"

gnome-terminal -- bash -c "export DINO_ROOT_DIR=$DIR && source $DIR/install/setup.bash && source $DIR/install/local_setup.bash && source $DIR/install/setup.bash && ros2 run system_monitor system_monitor; read"

gnome-terminal -- bash -c "export DINO_ROOT_DIR=$DIR && source $DIR/install/setup.bash && source $DIR/install/local_setup.bash && source $DIR/install/setup.bash  && ros2 run audio_player audio_player; read"

gnome-terminal -- bash -c "export DINO_ROOT_DIR=$DIR && source $DIR/install/setup.bash && source $DIR/install/local_setup.bash && source $DIR/install/setup.bash  && ros2 run imu_receiver imu_receiver; read"

gnome-terminal -- bash -c "export DINO_ROOT_DIR=$DIR && source $DIR/install/setup.bash && source $DIR/install/local_setup.bash && source $DIR/install/setup.bash  && ros2 run vision_receiver vision_receiver_node; read"

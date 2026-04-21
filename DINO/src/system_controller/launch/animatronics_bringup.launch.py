from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    start_controller = LaunchConfiguration('start_controller_publisher')
    start_motor_controller = LaunchConfiguration('start_motor_controller')
    start_system_controller = LaunchConfiguration('start_system_controller')
    start_audio_player = LaunchConfiguration('start_audio_player')
    start_motion_editor = LaunchConfiguration('start_motion_editor')
    start_imu_receiver = LaunchConfiguration('start_imu_receiver')

    return LaunchDescription([
        DeclareLaunchArgument(
            'start_controller_publisher',
            default_value='true',
            description='Launch controller_publisher node (DualSense input).'
        ),
        DeclareLaunchArgument(
            'start_motor_controller',
            default_value='true',
            description='Launch motor_controller node to drive Dynamixels.'
        ),
        DeclareLaunchArgument(
            'start_system_controller',
            default_value='true',
            description='Launch system_controller node (command routing, recording, audio triggers).'
        ),
        DeclareLaunchArgument(
            'start_audio_player',
            default_value='true',
            description='Launch audio_player node for dinosaur sounds.'
        ),
        DeclareLaunchArgument(
            'start_motion_editor',
            default_value='false',
            description='Launch Tk-based motion_editor GUI (set true when a display is available).'
        ),
        DeclareLaunchArgument(
            'start_imu_receiver',
            default_value='false',
            description='Launch imu_receiver node for Pico/BNO055 telemetry.'
        ),
        Node(
            package='controller_publisher',
            executable='controller_publisher',
            name='controller_publisher',
            output='screen',
            emulate_tty=True,
            condition=IfCondition(start_controller)
        ),
        Node(
            package='motor_controller',
            executable='motor_controller',
            name='motor_controller',
            output='screen',
            emulate_tty=True,
            condition=IfCondition(start_motor_controller)
        ),
        Node(
            package='system_controller',
            executable='system_controller',
            name='system_controller',
            output='screen',
            emulate_tty=True,
            condition=IfCondition(start_system_controller)
        ),
        Node(
            package='audio_player',
            executable='audio_player',
            name='audio_player',
            output='screen',
            emulate_tty=True,
            condition=IfCondition(start_audio_player)
        ),
        Node(
            package='motion_editor',
            executable='motion_editor',
            name='motion_editor',
            output='screen',
            emulate_tty=True,
            condition=IfCondition(start_motion_editor)
        ),
        Node(
            package='imu_receiver',
            executable='imu_receiver_node',
            name='imu_receiver',
            output='screen',
            emulate_tty=True,
            condition=IfCondition(start_imu_receiver)
        ),
    ])

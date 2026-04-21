#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2024
# SPDX-License-Identifier: BSD-3-Clause

import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory
from motor_commands.msg import IdAngle
from builtin_interfaces.msg import Duration

class TrajectoryInterpolator(Node):
    def __init__(self):
        super().__init__('trajectory_interpolator')

        # Publisher to motor_controller
        self.cmd_pub = self.create_publisher(IdAngle, 'IdAngle', 10)

        # Subscriber to trajectory commands
        self.traj_sub = self.create_subscription(
            JointTrajectory,
            'animatronics_trajectory',
            self.trajectory_callback,
            10
        )

        # Timer for 30Hz control loop to avoid RS485 bus congestion at 115200 bps
        self.timer_period = 0.033  # ~30 Hz
        self.timer = self.create_timer(self.timer_period, self.control_loop)

        self.current_trajectory = None
        self.start_time = None

        # Optionally load motor roles if we want to map string names to IDs later
        self.role_map = {
            "jaw": 11, "eye_r": 12, "eye_l": 13,
            "lid_ru": 21, "lid_rl": 22, "lid_lu": 23, "lid_ll": 24,
            "neck_yaw": 31, "neck_p1": 32, "neck_r": 33, "neck_p2": 34,
            "shld_r": 41, "elbw_r": 42, "shld_l": 43, "elbw_l": 44,
        }

        # Updated tail + leg naming that Motion Editor now emits
        self.role_map.update({
            "tail_r": 51,
            "tail_l": 52,
            "hip_a_l": 60,
            "hip_b_l": 61,
            "hip_c_l": 62,
            "knee_l": 63,
            "ankle_l": 64,
            "hip_a_r": 65,
            "hip_b_r": 66,
            "hip_c_r": 67,
            "knee_r": 68,
            "ankle_r": 69,
        })
        
        # Reverse map to support uppercase/spaced names
        # Also map integer strings like "11" -> 11
        for i in range(11, 70):
            self.role_map[str(i)] = i
            
        self.get_logger().info('Trajectory Interpolator initialized at 50Hz.')

    def duration_to_sec(self, d: Duration):
        return d.sec + (d.nanosec * 1e-9)

    def trajectory_callback(self, msg: JointTrajectory):
        if not msg.points:
            # Empty trajectory = STOP signal
            self.get_logger().info("Received STOP signal (empty trajectory). Halting playback.")
            self.current_trajectory = None
            self.start_time = None
            return
            
        self.get_logger().info(f"Received new trajectory with {len(msg.points)} points. Joint count: {len(msg.joint_names)}")
        self.current_trajectory = msg
        self.start_time = self.get_clock().now()

    def control_loop(self):
        if self.current_trajectory is None or self.start_time is None:
            return

        now = self.get_clock().now()
        elapsed = (now - self.start_time).nanoseconds * 1e-9

        points = self.current_trajectory.points
        
        # If elapsed time is before the first point, use first point
        # Though valid time_from_start should start at 0
        if elapsed < self.duration_to_sec(points[0].time_from_start):
            self.publish_point(points[0])
            return
            
        # If elapsed time is past the last point, hold the last point
        last_point_time = self.duration_to_sec(points[-1].time_from_start)
        if elapsed >= last_point_time:
            self.publish_point(points[-1])
            # We can choose to keep holding or clear the trajectory
            # Let's keep holding it so motors stay in active torque holding the last pose
            return

        # Find the two points to interpolate between
        for i in range(len(points) - 1):
            t1 = self.duration_to_sec(points[i].time_from_start)
            t2 = self.duration_to_sec(points[i+1].time_from_start)
            
            if t1 <= elapsed <= t2:
                # Interpolate
                ratio = (elapsed - t1) / (t2 - t1) if t2 > t1 else 0.0
                interpolated_positions = []
                
                for j in range(len(self.current_trajectory.joint_names)):
                    p1 = points[i].positions[j]
                    p2 = points[i+1].positions[j]
                    p_interp = p1 + ratio * (p2 - p1)
                    interpolated_positions.append(p_interp)
                
                self.publish_interpolated(interpolated_positions)
                break

    def publish_point(self, point):
        self.publish_interpolated(point.positions)

    def publish_interpolated(self, positions):
        msg = IdAngle()
        for i, name in enumerate(self.current_trajectory.joint_names):
            name_lower = name.lower()
            motor_id = None
            if name_lower in self.role_map:
                motor_id = self.role_map[name_lower]
            elif name in self.role_map:
                motor_id = self.role_map[name]
                
            if motor_id is not None:
                msg.ids.append(motor_id)
                msg.angles.append(int(positions[i]))
            else:
                self.get_logger().warn(f"Unknown joint name: {name}", throttle_duration_sec=2.0)
                
        if msg.ids:
            self.cmd_pub.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = TrajectoryInterpolator()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()

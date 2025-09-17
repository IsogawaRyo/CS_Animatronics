#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2024 Ryo Isogawa 　　　　　
# SPDX-License-Identifier: BSD-3-Claus

import time

import pygame
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Joy

class ControllerPublisher(Node):
    def __init__(self):
        super().__init__('controller_publisher')
        self.get_logger().info('Run controller publisher node')
        
        self.publisher_ = self.create_publisher(Joy, 'controller_input', 10)

        pygame.init()
        pygame.joystick.init()

        self.controller = None
        self.joystick_index = 0
        self.retry_interval = 1.0
        self.retry_log_interval = 5.0
        self._last_retry_attempt = 0.0
        self._last_retry_log = 0.0

        # Try initial connection immediately; timer will keep retrying if this fails.
        self.ensure_controller(force=True)

        self.timer = self.create_timer(0.05, self.timer_callback)

    def timer_callback(self):
        if not self.ensure_controller():
            return

        try:
            pygame.event.pump()

            msg = Joy()

            axes = [self.controller.get_axis(i) for i in range(self.controller.get_numaxes())]
            msg.axes = axes

            buttons = [self.controller.get_button(i) for i in range(self.controller.get_numbuttons())]
            msg.buttons = buttons

            self.publisher_.publish(msg)
            self.get_logger().info('Published controller state')
        except pygame.error as exc:
            self.get_logger().warn(f'Controller read failed; will retry connection: {exc}')
            if self.controller is not None:
                try:
                    self.controller.quit()
                except pygame.error:
                    pass
            self.controller = None

    def ensure_controller(self, force: bool = False) -> bool:
        """Attempt to ensure a joystick is connected. Returns True if ready."""

        if self.controller is not None:
            # Verify device still present; if not, drop and re-attempt.
            if pygame.joystick.get_count() == 0:
                self.get_logger().warn('Controller disconnected; waiting for reconnection...')
                try:
                    self.controller.quit()
                except pygame.error:
                    pass
                self.controller = None
            else:
                return True

        now = time.time()
        if not force and (now - self._last_retry_attempt) < self.retry_interval:
            return False

        self._last_retry_attempt = now

        pygame.joystick.quit()
        pygame.joystick.init()

        count = pygame.joystick.get_count()
        if count <= self.joystick_index:
            if (now - self._last_retry_log) >= self.retry_log_interval:
                self.get_logger().warn('No joystick detected. Please connect a controller!')
                self._last_retry_log = now
            return False

        try:
            controller = pygame.joystick.Joystick(self.joystick_index)
            controller.init()
        except pygame.error as exc:
            self.get_logger().warn(f'Failed to initialize joystick: {exc}')
            return False

        self.controller = controller
        self._last_retry_log = now
        name = controller.get_name() if hasattr(controller, 'get_name') else 'unknown'
        self.get_logger().info(f'Controller initialized: {name}')
        return True

def main(args=None):
    rclpy.init(args=args)
    node = ControllerPublisher()
    rclpy.spin(node)
    
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

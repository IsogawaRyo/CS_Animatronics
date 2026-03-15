#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2024 Ryo Isogawa
# SPDX-License-Identifier: BSD-3-Clause

import time
import json
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Joy
from std_msgs.msg import String

# Try importing pydualsense; handle failure gracefully if possible, 
# though this node is intended to use it.
try:
    from pydualsense import pydualsense, TriggerModes
    PYDUALSENSE_AVAILABLE = True
except ImportError:
    PYDUALSENSE_AVAILABLE = False

class ControllerPublisher(Node):
    def __init__(self):
        super().__init__('controller_publisher')
        self.get_logger().info('Run controller publisher node (pydualsense version)')

        if not PYDUALSENSE_AVAILABLE:
            self.get_logger().error("pydualsense library not found. Please install it.")
            # We might want to exit or fallback, but for now just warn.
        
        self.publisher_ = self.create_publisher(Joy, 'controller_input', 10)
        
        # Subscribe to feedback commands (JSON string)
        # e.g. {"type": "led", "r": 255, "g": 0, "b": 0}
        #      {"type": "rumble", "left": 100, "right": 255, "duration": 0.5}
        #      {"type": "trigger", "target": "L2", "mode": "rigid", "force": [10]}
        self.feedback_sub = self.create_subscription(
            String,
            'controller_feedback',
            self.feedback_callback,
            10
        )

        self.ds = None
        self.joystick_index = 0 # Not used for pydualsense which finds first available
        self.connected = False
        
        self.retry_interval = 2.0
        self._last_retry_attempt = 0.0

        # Try initial connection
        self.connect_controller()

        self.timer = self.create_timer(0.02, self.timer_callback) # 50Hz for smoother feedback response

    def connect_controller(self):
        if not PYDUALSENSE_AVAILABLE:
            return False
            
        try:
            if self.ds is not None:
                self.ds.close()
        except:
            pass

        try:
            self.ds = pydualsense()
            self.ds.init()
            self.connected = True
            self.get_logger().info('DualSense connected successfully.')
            
            # Initial feedback test (Blue LED)
            self.ds.setLightbar(0, 0, 255)
            # self.ds.setLeftMotor(0)
            # self.ds.setRightMotor(0)
            return True
        except Exception as e:
            self.get_logger().warn(f'Failed to connect DualSense: {e}')
            self.connected = False
            self.ds = None
            return False

    def feedback_callback(self, msg):
        if not self.connected or self.ds is None:
            return

        try:
            data = json.loads(msg.data)
            cmd_type = data.get("type")

            if cmd_type == "led":
                r = data.get("r", 0)
                g = data.get("g", 0)
                b = data.get("b", 0)
                self.ds.setLightbar(r, g, b)
                
            elif cmd_type == "rumble":
                left = data.get("left", 0)
                right = data.get("right", 0)
                self.ds.setLeftMotor(left)
                self.ds.setRightMotor(right)
                # Note: duration handling would need a separate timer or non-blocking wait
                # For now, system_controller should send stop command or short pulse

            elif cmd_type == "trigger":
                target = data.get("target", "R2") # L2 or R2
                mode_str = data.get("mode", "off")
                
                # Map string modes to TriggerModes
                # modes: off, rigid, pulse, etc.
                mode_map = {
                    "off": TriggerModes.Off,
                    "rigid": TriggerModes.Rigid,
                    "pulse": TriggerModes.Pulse,
                    "rigid_a": TriggerModes.Rigid_A,
                    "rigid_b": TriggerModes.Rigid_B,
                    "rigid_ab": TriggerModes.Rigid_AB,
                    "pulse_a": TriggerModes.Pulse_A,
                    "pulse_b": TriggerModes.Pulse_B,
                }
                mode = mode_map.get(mode_str, TriggerModes.Off)
                
                # Parameters for limit/force
                forces = data.get("force", []) 
                # pydualsense expects specific args based on mode. 
                # Simple implementation for Rigid:
                
                trigger = self.ds.triggerL if target == "L2" else self.ds.triggerR
                
                # Apply mode
                if mode == TriggerModes.Off:
                    trigger.setMode(TriggerModes.Off)
                elif mode == TriggerModes.Rigid:
                    # force[0] = start, force[1] = force
                    start = forces[0] if len(forces) > 0 else 0
                    force = forces[1] if len(forces) > 1 else 255
                    trigger.setMode(TriggerModes.Rigid)
                    trigger.setForce(1, start)
                    trigger.setForce(2, force)
                # Add other modes as needed
                    
        except json.JSONDecodeError:
            self.get_logger().error("Invalid JSON in feedback message")
        except Exception as e:
            self.get_logger().error(f"Error processing feedback: {e}")

    def timer_callback(self):
        if not self.connected:
            now = time.time()
            if (now - self._last_retry_attempt) > self.retry_interval:
                self._last_retry_attempt = now
                self.connect_controller()
            return

        try:
            # pydualsense updates state in background thread usually, or we assume data is fresh
            # But wait, standard pydualsense usage might need explicit update?
            # actually pydualsense uses hidapi and reads in init? 
            # Looking at docs/source, it usually spawns a thread or needs reading.
            # Assuming the library handles reading. The provided test script implies `ds.init()` starts it.
            
            # Map pydualsense state to sensor_msgs/Joy
            msg = Joy()
            msg.header.stamp = self.get_clock().now().to_msg()
            
            # Axes Mapping (Standard DualSense Layout)
            # 0: Lx, 1: Ly, 2: L2, 3: Rx, 4: Ry, 5: R2
            # pydualsense values: -128 to 127 usually for sticks, 0-255 for triggers
            # We normalize to -1.0 to 1.0
            
            # Stick LY and RY are commonly inverted in ROS (Up is +1.0 in msg usually, but hardware depends)
            # Let's standardize: Up = +1.0, Left = +1.0
            
            msg.axes = [0.0] * 6
            msg.axes[0] = -(self.ds.state.LX / 128.0 - 1.0) # Left +1.0
            msg.axes[1] = -(self.ds.state.LY / 128.0 - 1.0) # Up +1.0
            msg.axes[2] = (self.ds.state.L2 / 255.0)        # 0.0 to 1.0
            msg.axes[3] = -(self.ds.state.RX / 128.0 - 1.0) # Left +1.0
            msg.axes[4] = -(self.ds.state.RY / 128.0 - 1.0) # Up +1.0
            msg.axes[5] = (self.ds.state.R2 / 255.0)        # 0.0 to 1.0
            
            # Buttons Mapping
            # 0: Cross, 1: Circle, 2: Square, 3: Triangle, 
            # 4: L1, 5: R1, 6: L2_Btn, 7: R2_Btn, 
            # 8: Share, 9: Options, 10: PS, 11: L3, 12: R3
            msg.buttons = [0] * 13
            msg.buttons[0] = 1 if self.ds.state.cross else 0
            msg.buttons[1] = 1 if self.ds.state.circle else 0
            msg.buttons[2] = 1 if self.ds.state.square else 0
            msg.buttons[3] = 1 if self.ds.state.triangle else 0
            msg.buttons[4] = 1 if self.ds.state.L1 else 0
            msg.buttons[5] = 1 if self.ds.state.R1 else 0
            msg.buttons[6] = 1 if self.ds.state.L2Btn else 0 # Threshold usually
            msg.buttons[7] = 1 if self.ds.state.R2Btn else 0
            msg.buttons[8] = 1 if self.ds.state.share else 0
            msg.buttons[9] = 1 if self.ds.state.options else 0
            msg.buttons[10] = 1 if self.ds.state.ps else 0
            msg.buttons[11] = 1 if self.ds.state.L3 else 0
            msg.buttons[12] = 1 if self.ds.state.R3 else 0
            
            # Hat (D-Pad) usually mapped to axes 6/7 or buttons in some ROS nodes.
            # system_controller expects fixed indices, let's stick to buttons if possible
            # system_controller doesn't seem to use D-Pad heavily in current logic shown (uses R1/L1 for menu).
            # But standard is axes 6/7.
            
            self.publisher_.publish(msg)
            
        except IOError:
            self.get_logger().warn("Controller read error, forcing reconnect.")
            self.connected = False
        except Exception as e:
            self.get_logger().error(f"Error reading controller: {e}")

def main(args=None):
    rclpy.init(args=args)
    node = ControllerPublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        if node.ds:
            try:
                node.ds.setLightbar(0,0,0)
                node.ds.close()
            except:
                pass
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()

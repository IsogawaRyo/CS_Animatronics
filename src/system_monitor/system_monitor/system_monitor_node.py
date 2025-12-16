#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2024 Ryo Isogawa
# SPDX-License-Identifier: BSD-3-Clause

import rclpy
from rclpy.node import Node
from motor_command_msg.msg import IdAngle
from sensor_msgs.msg import Joy
from dynamixel_sdk_custom_interfaces.srv import GetPosition  # Assuming this exists based on imports in other files
# Note: In dev branch logic, motor_controller uses GetMotorStates custom service. 
# Checking imports in motor_controller.py: from motor_commands.srv import GetMotorStates
from motor_commands.srv import GetMotorStates

import tkinter as tk
from tkinter import ttk
import threading
import time

class SystemMonitor(Node):
    def __init__(self):
        super().__init__('system_monitor')
        self.get_logger().info('System Monitor GUI starting...')

        # Data storage
        self.motor_targets = {}  # {id: angle}
        self.motor_states = {}   # {id: {pos, temp, load, error}}
        self.controller_connected = False
        self.last_controller_msg = 0.0
        
        # Subscribe to IdAngle (Targets)
        self.create_subscription(IdAngle, 'IdAngle', self.target_callback, 10)
        
        # Subscribe to Controller Input
        self.create_subscription(Joy, 'controller_input', self.joy_callback, 10)
        
        # Service Client for Motor States
        self.get_states_client = self.create_client(GetMotorStates, 'get_motor_states')
        
        # Tkinter Setup
        self.root = tk.Tk()
        self.root.title("CS_Animatronics System Monitor")
        self.root.geometry("800x600")
        
        self.setup_ui()
        
        # Start state polling timer
        self.create_timer(0.5, self.poll_motor_states)
        
        # Start GUI update loop (separate from ROS loop)
        self.update_gui()

    def setup_ui(self):
        # Top Frame: System Status
        status_frame = ttk.LabelFrame(self.root, text="System Status", padding=10)
        status_frame.pack(fill="x", padx=5, pady=5)
        
        self.lbl_controller = ttk.Label(status_frame, text="Controller: Disconnected", foreground="red")
        self.lbl_controller.pack(side="left", padx=10)
        
        self.lbl_ros_time = ttk.Label(status_frame, text="ROS Time: 0.0")
        self.lbl_ros_time.pack(side="right", padx=10)

        # Main Frame: Motor Table
        table_frame = ttk.LabelFrame(self.root, text="Motor Status", padding=10)
        table_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        columns = ("ID", "Role", "Target", "Actual", "Diff", "Temp", "Load", "Error")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=80, anchor="center")
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)
        
        # Populate initial rows
        self.motor_ids = [
            11, 12, 13, 
            21, 22, 23, 24, 
            31, 32, 33, 34,
            41, 42, 43, 44,
            51, 52,
            61, 62, 63, 64, 65, 66, 67, 68
        ]
        
        self.role_map = {
            11: "Jaw", 12: "Eye R", 13: "Eye L",
            21: "Lid RU", 22: "Lid RL", 23: "Lid LU", 24: "Lid LL",
            31: "Neck Yaw", 32: "Neck P1", 33: "Neck R", 34: "Neck P2",
            41: "Shld R", 42: "Elbw R", 43: "Shld L", 44: "Elbw L",
            51: "Tail Yaw", 52: "Tail Pit",
            61: "Leg R1", 62: "Leg R2", 63: "Leg R3", 64: "Leg R4",
            65: "Leg L1", 66: "Leg L2", 67: "Leg L3", 68: "Leg L4"
        }

        for mid in self.motor_ids:
            self.tree.insert("", "end", iid=str(mid), values=(
                mid, self.role_map.get(mid, "Unknown"), 
                "-", "-", "-", "-", "-", "-"
            ))

    def target_callback(self, msg):
        for i, mid in enumerate(msg.ids):
            if i < len(msg.angles):
                self.motor_targets[mid] = msg.angles[i]

    def joy_callback(self, msg):
        self.controller_connected = True
        self.last_controller_msg = time.time()

    def poll_motor_states(self):
        if not self.get_states_client.service_is_ready():
            return
            
        req = GetMotorStates.Request()
        req.ids = self.motor_ids
        future = self.get_states_client.call_async(req)
        future.add_done_callback(self.on_states_received)

    def on_states_received(self, future):
        try:
            resp = future.result()
            for i, mid in enumerate(resp.ids):
                self.motor_states[mid] = {
                    "pos": resp.positions[i],
                    "temp": resp.temperatures[i],
                    "load": resp.torques[i], # Note: message field is 'torques' but logically load/current
                    "error": resp.error_status[i]
                }
        except Exception as e:
            self.get_logger().error(f"Failed to get motor states: {e}")

    def update_gui(self):
        # Update Controller Status
        if time.time() - self.last_controller_msg > 2.0:
            self.lbl_controller.config(text="Controller: Disconnected", foreground="red")
        else:
            self.lbl_controller.config(text="Controller: Connected", foreground="green")
            
        self.lbl_ros_time.config(text=f"Time: {time.time():.1f}")

        # Update Treeview only if data changed (optimization)
        for mid in self.motor_ids:
            target = self.motor_targets.get(mid, "-")
            
            state = self.motor_states.get(mid, {})
            actual = state.get("pos", "-")
            temp = state.get("temp", "-")
            load = state.get("load", "-")
            error = state.get("error", "-")
            
            diff = "-"
            if isinstance(target, int) and isinstance(actual, int):
                diff = actual - target
            
            # Update row
            # Color coding logic
            tags = ()
            if error != "NO_ERROR" and error != "-":
                tags = ("error",)
            elif isinstance(temp, int) and temp > 50:
                 tags = ("warn",)

            self.tree.item(str(mid), values=(
                mid, self.role_map.get(mid, "Unknown"),
                target, actual, diff, temp, load, error
            ), tags=tags)
        
        self.tree.tag_configure("error", background="#ffcccc")
        self.tree.tag_configure("warn", background="#ffffcc")

        self.root.update_idletasks()
        self.root.update()
        
        # Schedule next update (approx 10Hz)
        self.root.after(100, self.update_gui)

def main(args=None):
    rclpy.init(args=args)
    node = SystemMonitor()
    
    try:
        # Tkinter mainloop takes control, so we need to pump ROS callbacks manually or use thread
        # Simple approach: rclpy.spin in a separate thread
        spin_thread = threading.Thread(target=rclpy.spin, args=(node,), daemon=True)
        spin_thread.start()
        
        node.root.mainloop()
        
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()

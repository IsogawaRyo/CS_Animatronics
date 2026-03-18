#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2024 Ryo Isogawa
# SPDX-License-Identifier: BSD-3-Clause

import rclpy
from rclpy.node import Node
from motor_commands.msg import IdAngle
from sensor_msgs.msg import Joy, Imu
from dynamixel_sdk_custom_interfaces.srv import GetPosition  # Assuming this exists based on imports in other files
# Note: In dev branch logic, motor_controller uses GetMotorStates custom service. 
# Checking imports in motor_controller.py: from motor_commands.srv import GetMotorStates
from motor_commands.srv import GetMotorStates

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import subprocess
import os
import math
from std_msgs.msg import String, Int32
from std_srvs.srv import Trigger
from rclpy.executors import MultiThreadedExecutor

from motion_editor.motion_editor import MotionEditor, ROSManager as MotionROSManager

STATE_POLL_PERIOD = 5.0  # seconds between motor state refreshes

class SystemMonitor(Node):
    def __init__(self, motion_ros_manager):
        super().__init__('system_monitor')
        self.motion_ros_manager = motion_ros_manager
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
        
        # Subscribe to IMU topics
        self.imu_data = {0: {}, 1: {}, 2: {}}
        for i in range(3):
            self.create_subscription(Imu, f'imu{i}', lambda msg, idx=i: self.imu_callback(msg, idx), 10)
            
        # Audio Player Publishers
        self.play_audio_id_pub = self.create_publisher(Int32, 'play_audio_id', 10)
        self.play_audio_name_pub = self.create_publisher(String, 'play_audio_name', 10)
        self.stop_audio_pub = self.create_publisher(String, 'stop_audio', 10)
        
        # Subscribe to audio_status
        self.create_subscription(String, 'audio_status', self.audio_status_callback, 10)
        
        # Service Client for Motor States
        self.get_states_client = self.create_client(GetMotorStates, 'get_motor_states')
        
        # Service Client for Reconnection
        self.reconnect_client = self.create_client(Trigger, 'reconnect_ports')
        
        # Tkinter Setup
        self.root = tk.Tk()
        self.root.title("CS_Animatronics System Monitor")
        self.root.geometry("800x600")
        
        self.setup_ui()
        
        # Start state polling timer (Slower to reduce bus contention)
        self.create_timer(STATE_POLL_PERIOD, self.poll_motor_states)
        
        # Start GUI update loop (separate from ROS loop)
        self.update_gui()

    def setup_ui(self):
        # Notebook (Tabs)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Tab 1: Motor Monitor
        self.motor_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.motor_tab, text="Motor Monitor")
        self.setup_motor_tab(self.motor_tab)
        
        # Tab 2: Node Manager
        self.node_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.node_tab, text="Node Manager")
        self.setup_node_manager_tab(self.node_tab)
        
        # Tab 3: IMU Monitor
        self.imu_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.imu_tab, text="IMU Monitor")
        self.setup_imu_tab(self.imu_tab)
        
        # Tab 4: Motion Editor
        self.motion_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.motion_tab, text="Motion Editor")
        self.motion_editor_app = MotionEditor(self.motion_ros_manager, self.motion_tab)

        # Tab 5: Audio Player
        self.audio_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.audio_tab, text="Audio Player")
        self.setup_audio_tab(self.audio_tab)

    def setup_motor_tab(self, parent):
        # Top Frame: System Status
        status_frame = ttk.LabelFrame(parent, text="System Status", padding=10)
        status_frame.pack(fill="x", padx=5, pady=5)
        
        self.lbl_controller = ttk.Label(status_frame, text="Controller: Disconnected", foreground="red")
        self.lbl_controller.pack(side="left", padx=10)
        
        self.lbl_ros_time = ttk.Label(status_frame, text="ROS Time: 0.0")
        self.lbl_ros_time.pack(side="right", padx=10)

        # Main Frame: Motor Table
        table_frame = ttk.LabelFrame(parent, text="Motor Status", padding=10)
        table_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        columns = ("ID", "Role", "Target", "Actual", "Diff", "Temp", "Load", "Error")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=70, anchor="center")
        
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
            60, 61, 62, 63, 64,
            65, 66, 67, 68, 69
        ]
        
        self.role_map = {
            11: "Jaw", 12: "Eye R", 13: "Eye L",
            21: "Lid RU", 22: "Lid RL", 23: "Lid LU", 24: "Lid LL",
            31: "Neck Yaw", 32: "Neck P1", 33: "Neck R", 34: "Neck P2",
            41: "Shld R", 42: "Elbw R", 43: "Shld L", 44: "Elbw L",
            51: "Tail R", 52: "Tail L",
            60: "HipA L", 61: "HipB L", 62: "HipC L", 63: "Knee L", 64: "Ankle L",
            65: "HipA R", 66: "HipB R", 67: "HipC R", 68: "Knee R", 69: "Ankle R"
        }

        for mid in self.motor_ids:
            self.tree.insert("", "end", iid=str(mid), values=(
                mid, self.role_map.get(mid, "Unknown"), 
                "-", "-", "-", "-", "-", "-"
            ))

        # --- Reboot button row ---
        btn_frame = ttk.Frame(table_frame)
        btn_frame.pack(fill="x", pady=(4, 0))
        ttk.Button(btn_frame, text="🔄 Reboot Selected Motor",
                   command=self._reboot_selected_motor).pack(side="left", padx=4)
        ttk.Label(btn_frame,
                  text="(Select a row then click, or right-click a row)",
                  foreground="gray").pack(side="left")

        # --- Reconnect button ---
        ttk.Button(btn_frame, text="🔌 接続切れポートを再接続",
                   command=self._reconnect_ports).pack(side="right", padx=10)

        # Right-click context menu
        self._ctx_menu = tk.Menu(self.root, tearoff=0)
        self._ctx_menu.add_command(label="🔄 Reboot this motor",
                                   command=self._reboot_selected_motor)
        self.tree.bind("<Button-3>", self._show_ctx_menu)

    def _show_ctx_menu(self, event):
        """Select the row under cursor and show context menu."""
        row = self.tree.identify_row(event.y)
        if row:
            self.tree.selection_set(row)
            self._ctx_menu.tk_popup(event.x_root, event.y_root)

    def _reboot_selected_motor(self):
        """Reboot the motor currently selected in the treeview."""
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("No Selection", "Motor Monitor: モーター行を選択してください。")
            return
        motor_id = int(sel[0])
        if not messagebox.askyesno("Reboot Motor",
                                   f"Motor ID {motor_id} ({self.role_map.get(motor_id, '?')}) を再起動しますか？\n"
                                   "トルク OFF 後に自動再初期化されます。"):
            return
        self.motion_ros_manager.reboot_motor(motor_id)
        self.get_logger().info(f"Reboot sent to motor {motor_id}.")

    def _reconnect_ports(self):
        if not self.reconnect_client.service_is_ready():
            messagebox.showerror("Error", "Motor Controller is not ready or service is unavailable!")
            return
            
        if not messagebox.askyesno("Confirm Reconnect", "USBポートの再スキャンと再接続を実行しますか？\n(実行中、モーターが一時的に初期状態に戻る可能性があります)"):
            return
            
        req = Trigger.Request()
        future = self.reconnect_client.call_async(req)
        future.add_done_callback(self._on_reconnect_done)
        
    def _on_reconnect_done(self, future):
        try:
            resp = future.result()
            if resp.success:
                messagebox.showinfo("Success", f"再接続に成功しました:\n{resp.message}")
            else:
                messagebox.showwarning("Failed", f"再接続に失敗しました:\n{resp.message}")
        except Exception as e:
            messagebox.showerror("Error", f"Reconnection request failed: {e}")

    def setup_node_manager_tab(self, parent):
        # Manager Settings
        self.targets = [
            {"name": "motor_controller", "pkg": "motor_controller", "exec": "motor_controller", "cmd": "sudo -S usermod -aG dialout csanimatronics <<< 'KUASECSA' && ros2 run motor_controller motor_controller"},
            {"name": "system_controller", "pkg": "system_controller", "exec": "system_controller", "cmd": "ros2 run system_controller system_controller"},
            {"name": "controller_publisher", "pkg": "controller_publisher", "exec": "controller_publisher", "cmd": "ros2 run controller_publisher controller_publisher"},
            {"name": "audio_player", "pkg": "audio_player", "exec": "audio_player", "cmd": "ros2 run audio_player audio_player"},
            {"name": "motion_editor", "pkg": "motion_editor", "exec": "motion_editor", "cmd": "ros2 run motion_editor motion_editor"},
            {"name": "imu_receiver", "pkg": "imu_receiver", "exec": "imu_receiver", "cmd": "ros2 run imu_receiver imu_receiver"},
        ]
        
        # UI
        frame = ttk.LabelFrame(parent, text="Nodes", padding=10)
        frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.node_widgets = {} # {name: {lbl_status, btn_start, btn_stop}}
        
        for i, target in enumerate(self.targets):
            row_frame = ttk.Frame(frame)
            row_frame.pack(fill="x", pady=5)
            
            lbl_name = ttk.Label(row_frame, text=target["name"], width=20, font=("Arial", 12, "bold"))
            lbl_name.pack(side="left")
            
            lbl_status = ttk.Label(row_frame, text="Unknown", width=15)
            lbl_status.pack(side="left", padx=10)
            
            btn_restart = ttk.Button(row_frame, text="Restart", command=lambda t=target: self.restart_node(t))
            btn_restart.pack(side="right", padx=5)
            
            btn_stop = ttk.Button(row_frame, text="Stop", command=lambda t=target: self.stop_node(t))
            btn_stop.pack(side="right", padx=5)
            
            btn_start = ttk.Button(row_frame, text="Start", command=lambda t=target: self.start_node(t))
            btn_start.pack(side="right", padx=5)
            
            self.node_widgets[target["name"]] = {
                "status": lbl_status,
                "start": btn_start,
                "stop": btn_stop
            }
            
        # Refresh Button
        btn_refresh = ttk.Button(frame, text="Refresh Status", command=self.check_node_status)
        btn_refresh.pack(pady=10)
        
        # Start status checker timer (every 2s)
        self.create_timer(2.0, self.check_node_status)

    def check_node_status(self):
        # Get active nodes from ROS
        try:
            active_nodes = self.get_node_names_and_namespaces()
            # Result is list of (name, namespace). Flatten to list of names.
            # Node names often start with /
            active_names = [n[0].lstrip('/') for n in active_nodes]
        except Exception as e:
            self.get_logger().error(f"Failed to get node list: {e}")
            return

        for target in self.targets:
            name = target["name"]
            widgets = self.node_widgets[name]
            
            if name in active_names:
                widgets["status"].config(text="Running", foreground="green")
                widgets["start"].state(["disabled"])
                widgets["stop"].state(["!disabled"])
            else:
                widgets["status"].config(text="Stopped", foreground="red")
                widgets["start"].state(["!disabled"])
                widgets["stop"].state(["disabled"])

    def start_node(self, target):
        self.get_logger().info(f"Starting {target['name']}...")
        try:
            # Emulate ros2_start.sh behavior: Open new terminal and source setup then run
            cmd = f"source ~/CS_Animatronics/install/setup.bash && {target['cmd']}; read"
            subprocess.Popen(["gnome-terminal", "--", "bash", "-c", cmd])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start {target['name']}: {e}")

    def stop_node(self, target):
        self.get_logger().info(f"Stopping {target['name']}...")
        try:
            # Pkill based on the executable name
            # Note: This is aggressive but simple.
            subprocess.run(["pkill", "-f", f"ros2 run {target['pkg']} {target['exec']}"], check=False)
            subprocess.run(["pkill", "-f", target["exec"]], check=False) # Fallback
            
            # Update UI immediately (optimistic)
            self.node_widgets[target["name"]]["status"].config(text="Stopping...", foreground="orange")
        except Exception as e:
             messagebox.showerror("Error", f"Failed to stop {target['name']}: {e}")

    def restart_node(self, target):
        self.stop_node(target)
        # Wait a bit before starting
        self.root.after(1000, lambda: self.start_node(target))

    def setup_imu_tab(self, parent):
        frame = ttk.LabelFrame(parent, text="IMU Sensors", padding=10)
        frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        columns = ("Sensor", "Roll (deg)", "Pitch (deg)", "Yaw (deg)", "Acc X", "Acc Y", "Acc Z")
        self.tree_imu = ttk.Treeview(frame, columns=columns, show="headings", height=5)
        
        for col in columns:
            self.tree_imu.heading(col, text=col)
            self.tree_imu.column(col, width=100, anchor="center")
        
        self.tree_imu.pack(fill="both", expand=True)
        
        # Init rows
        for i in range(3):
            self.tree_imu.insert("", "end", iid=f"imu_{i}", values=(f"IMU {i}", "-", "-", "-", "-", "-", "-"))

    def imu_callback(self, msg, idx):
        # Convert Quat to Euler
        q = msg.orientation
        
        # Roll (x-axis rotation)
        sinr_cosp = 2 * (q.w * q.x + q.y * q.z)
        cosr_cosp = 1 - 2 * (q.x * q.x + q.y * q.y)
        roll = math.atan2(sinr_cosp, cosr_cosp)

        # Pitch (y-axis rotation)
        sinp = 2 * (q.w * q.y - q.z * q.x)
        if abs(sinp) >= 1:
            pitch = math.copysign(math.pi / 2, sinp) # use 90 degrees if out of range
        else:
            pitch = math.asin(sinp)

        # Yaw (z-axis rotation)
        siny_cosp = 2 * (q.w * q.z + q.x * q.y)
        cosy_cosp = 1 - 2 * (q.y * q.y + q.z * q.z)
        yaw = math.atan2(siny_cosp, cosy_cosp)
        
        self.imu_data[idx] = {
            "roll": math.degrees(roll),
            "pitch": math.degrees(pitch),
            "yaw": math.degrees(yaw),
            "acc_x": msg.linear_acceleration.x,
            "acc_y": msg.linear_acceleration.y,
            "acc_z": msg.linear_acceleration.z
        }

    def setup_audio_tab(self, parent):
        self.lbl_audio_status = ttk.Label(parent, text="Status: Unknown", font=("Arial", 14), foreground="blue")
        self.lbl_audio_status.pack(pady=10)
        
        btn_frame = ttk.Frame(parent)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="Stop Audio", command=self.stop_audio).pack(side="left", padx=5)
        
        audio_frame = ttk.LabelFrame(parent, text="Play Dinosaur Sounds", padding=10)
        audio_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        sounds = {
            1: "Roar 1", 2: "Roar 2", 3: "Growl", 4: "Hiss", 5: "Chomp",
            6: "Footstep 1", 7: "Footstep 2", 8: "Breath 1", 9: "Warning",
            10: "Hunt", 11: "Pain", 12: "Victory"
        }
        
        row, col = 0, 0
        for sound_id, name in sounds.items():
            ttk.Button(audio_frame, text=name, command=lambda i=sound_id: self.play_audio_id(i)).grid(row=row, column=col, padx=10, pady=10, sticky="ew")
            col += 1
            if col > 3:
                col = 0
                row += 1

    def play_audio_id(self, audio_id):
        msg = Int32()
        msg.data = audio_id
        self.play_audio_id_pub.publish(msg)
        
    def stop_audio(self):
        msg = String()
        msg.data = ""
        self.stop_audio_pub.publish(msg)
        
    def audio_status_callback(self, msg):
        if hasattr(self, 'lbl_audio_status'):
            self.lbl_audio_status.config(text=f"Status: {msg.data}")



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

        # Update IMU Treeview
        if hasattr(self, 'tree_imu'):
            for i in range(3):
                data = self.imu_data.get(i, {})
                if not data:
                    continue
                    
                self.tree_imu.item(f"imu_{i}", values=(
                    f"IMU {i}",
                    f"{data.get('roll', 0):.1f}",
                    f"{data.get('pitch', 0):.1f}",
                    f"{data.get('yaw', 0):.1f}",
                    f"{data.get('acc_x', 0):.2f}",
                    f"{data.get('acc_y', 0):.2f}",
                    f"{data.get('acc_z', 0):.2f}"
                ))

        self.root.update_idletasks()
        self.root.update()
        
        # Schedule next update (approx 10Hz)
        self.root.after(100, self.update_gui)

def main(args=None):
    rclpy.init(args=args)
    motion_ros_manager = MotionROSManager()
    node = SystemMonitor(motion_ros_manager)
    
    executor = MultiThreadedExecutor()
    executor.add_node(node)
    executor.add_node(motion_ros_manager)
    
    try:
        spin_thread = threading.Thread(target=executor.spin, daemon=True)
        spin_thread.start()
        
        node.root.mainloop()
        
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        motion_ros_manager.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()

import sys
import os
import tkinter as tk
import tkinter.filedialog
import tkinter.ttk as ttk
import tkinter.messagebox as messagebox
import json
import time
import threading

import rclpy
from rclpy.node import Node
from motor_commands.msg import IdAngle
from motor_commands.srv import GetMotorStates
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from builtin_interfaces.msg import Duration

class ROSManager(Node):
    def __init__(self):
        super().__init__('motion_editor_ros_client')
        
        self.publisher = self.create_publisher(
            IdAngle,
            'IdAngle',
            12
        )

        self.traj_publisher = self.create_publisher(
            JointTrajectory,
            'animatronics_trajectory',
            10
        )

        self.reboot_publisher = self.create_publisher(
            IdAngle,
            'motor_reboot',
            10
        )

        self.get_motor_states_client = self.create_client(
            GetMotorStates,
            "get_motor_states"
        )
    
        # We won't block main thread indefinitely
        self.request = GetMotorStates.Request()

    def call_get_motor_states(self, ids, callback):
        """Returns True if the async call was made, False if service unavailable."""
        if not self.get_motor_states_client.wait_for_service(timeout_sec=0.1):
            return False
        self.request.ids = ids
        self.future = self.get_motor_states_client.call_async(self.request)
        self.future.add_done_callback(callback)
        return True

    def set_positions(self, ids, angles):
        new_msg = IdAngle()
        new_msg.ids = ids
        new_msg.angles = angles
        self.publisher.publish(new_msg)

    def publish_trajectory(self, trajectory_msg):
        self.traj_publisher.publish(trajectory_msg)

    def stop_trajectory(self):
        """Publish an empty JointTrajectory to signal the interpolator to stop."""
        self.traj_publisher.publish(JointTrajectory())

    def reboot_motor(self, motor_id: int):
        """Publish a reboot request for a single motor via /motor_reboot topic."""
        msg = IdAngle()
        msg.ids = [motor_id]
        msg.angles = [0]  # placeholder; ignored by reboot_callback
        self.reboot_publisher.publish(msg)


class MotionEditor:
    def __init__(self, ros_manager, parent_frame):
        self.ros_manager = ros_manager
        self.root = parent_frame

        self.motionFile = []
        self.is_playing = False
        
        # Time variables (in seconds)
        self.timestamp = tk.DoubleVar(self.root, value=0.0)
        self.last_timestamp = tk.DoubleVar(self.root, value=-1.0)
        
        self.timeMin = tk.DoubleVar(self.root, value=0.0)
        self.timeMax = tk.DoubleVar(self.root, value=10.0)
        
        # Observe mode flag - enabled by default
        self.observe_mode = tk.BooleanVar(self.root, value=True)
        self.is_service_calling = False   # guard for observe_hardware
        self._syncing = False              # guard for sync_sliders_from_hardware (独立)
        self.last_observe_time = 0.0
        
        # Edit mode: when True, timeline does NOT overwrite sliders/include state
        self.edit_mode = False
        
        # Playback tracking: wall-clock time when PLAY was pressed
        self._play_start_wall = None    # float or None
        self._play_total_duration = 0.0  # seconds (last keypose timestamp)
        
        # Track which slider the user is currently dragging (None = not dragging)
        self._editing_id = None
        # Track when timeline was last updated to temporarily block observe overwrites
        self._timeline_updated_at = 0.0
        
        # Keep track of actual hardware positions (for display only, won't override user edits)
        self.hardware_positions = {}  # {id_str: int}
        
        # Current displays
        self.port0_current = tk.IntVar(self.root)
        self.port1_current = tk.IntVar(self.root)
        self.system_current = tk.IntVar(self.root)
        
        # Load Motor Limits
        self.motorLimits = {}
        self.loadMotorLimits()

        self.selectedFile = tk.StringVar(value="Not Selected")

        self.setup_ui()
        
        # Start main loop at 50Hz for smooth playback UI
        self.root.after(20, self.main_loop)

    def loadMotorLimits(self):
        try:
            with open(os.path.expanduser("~/CS_Animatronics/Motor_Limits.json"), "r", encoding="utf-8") as file:
                data = json.load(file)
            for key, subdict in data.items():
                subdict["ini"] = int(subdict["ini"])
                subdict["min"] = int(subdict["min"])
                subdict["max"] = int(subdict["max"])
            self.motorLimits = data
        except Exception as e:
            print(f"Failed to load Motor_Limits.json: {e}")

    def setup_ui(self):
        # Settings Frame
        self.frame_settings = tk.LabelFrame(self.root, text="File Settings", foreground="green")
        self.frame_settings.grid(sticky="W", row=0, column=0, columnspan=2, padx=5, pady=5)
        
        tk.Label(self.frame_settings, textvariable=self.selectedFile, width=40).grid(row=0, column=0, columnspan=2)
        tk.Button(self.frame_settings, text="Open JSON", command=self.fileDialog).grid(row=1, column=0, pady=5)
        tk.Button(self.frame_settings, text="Save JSON", command=self.saveMotionFile).grid(row=1, column=1, pady=5)
        
        # Operations Frame
        self.frame_operations = tk.LabelFrame(self.root, text="Timeline & Keyposes", foreground="green")
        self.frame_operations.grid(sticky="W", row=1, column=0, columnspan=2, padx=5, pady=5)
        
        tk.Button(self.frame_operations, text="< -1s", command=self.moveBackward).grid(row=0, column=0)
        tk.Label(self.frame_operations, text="0.0s").grid(row=0, column=1)
        
        self.scale_time = tk.Scale(self.frame_operations, from_=self.timeMin.get(), to_=self.timeMax.get(), 
                                   variable=self.timestamp, orient=tk.HORIZONTAL, resolution=0.1, length=400)
        self.scale_time.grid(row=0, column=2, padx=10)
        
        self.lbl_max_time = tk.Label(self.frame_operations, text=f"{self.timeMax.get()}s")
        self.lbl_max_time.grid(row=0, column=3)
        tk.Button(self.frame_operations, text="+1s >", command=self.moveForward).grid(row=0, column=4)
        
        tk.Button(self.frame_operations, text="Add/Update Keypose (At Current Time)", bg="lightblue", command=self.add_keypose).grid(row=1, column=1, columnspan=2, pady=10)
        tk.Button(self.frame_operations, text="Delete Keypose", bg="#ff9999", command=self.delete_keypose).grid(row=1, column=3, pady=10)
        
        # Edit / Preview toggle button
        self.btn_edit = tk.Button(self.frame_operations, text="✏️ EDIT MODE: OFF",
                                  bg="#d0d0d0", width=18, command=self.toggle_edit_mode)
        self.btn_edit.grid(row=2, column=0, columnspan=1, pady=5, padx=4)
        
        tk.Button(self.frame_operations, text="▶ PLAY Trajectory", bg="lightgreen", command=self.playMotion).grid(row=2, column=1, pady=5)
        tk.Button(self.frame_operations, text="⏹ STOP", bg="#ff6666", fg="white", font=("TkDefaultFont", 10, "bold"),
                  command=self.stopMotion).grid(row=2, column=2, pady=5)
        
        # Monitor Frame (Sliders)
        self.frame_monitor = tk.LabelFrame(self.root, text="Motor Control (Edit Position)", foreground="green")
        self.frame_monitor.grid(sticky="NSEW", row=2, column=0, padx=5, pady=5)
        self.frame_monitor.grid_rowconfigure(0, weight=1)
        self.frame_monitor.grid_columnconfigure(0, weight=1)
        
        # Add Canvas + Scrollbar for motors (vertical + horizontal)
        self.motor_canvas = tk.Canvas(self.frame_monitor)
        vbar = tk.Scrollbar(self.frame_monitor, orient=tk.VERTICAL, command=self.motor_canvas.yview)
        hbar = tk.Scrollbar(self.frame_monitor, orient=tk.HORIZONTAL, command=self.motor_canvas.xview)
        self.motor_canvas.configure(yscrollcommand=vbar.set, xscrollcommand=hbar.set)
        
        self.inner_monitor = tk.Frame(self.motor_canvas)
        self.inner_monitor.bind("<Configure>", lambda e: self.motor_canvas.configure(
            scrollregion=self.motor_canvas.bbox("all")))
        self.motor_canvas.create_window((0, 0), window=self.inner_monitor, anchor="nw")
        
        self.motor_canvas.grid(row=0, column=0, sticky="NSEW")
        vbar.grid(row=0, column=1, sticky="NS")
        hbar.grid(row=1, column=0, sticky="EW")
        
        # Current Frame
        self.frame_current = tk.LabelFrame(self.root, text="System Status", foreground="blue")
        self.frame_current.grid(sticky="NEW", row=2, column=1, padx=5, pady=5)
        
        tk.Checkbutton(self.frame_current, text="Enable Hardware Observe Mode", variable=self.observe_mode).grid(row=0, column=0, columnspan=3, pady=5)
        
        tk.Button(self.frame_current, text="📥 Sync from Hardware", bg="#ffe0a0",
                  command=self.sync_sliders_from_hardware).grid(row=1, column=0, columnspan=3, pady=4, sticky="EW")
        
        tk.Label(self.frame_current, text="PORT0:").grid(row=2, column=0)
        self.label_port0 = tk.Label(self.frame_current, textvariable=self.port0_current, width=6, relief="sunken")
        self.label_port0.grid(row=2, column=1)
        tk.Label(self.frame_current, text="mA").grid(row=2, column=2)
        
        tk.Label(self.frame_current, text="PORT1:").grid(row=3, column=0)
        self.label_port1 = tk.Label(self.frame_current, textvariable=self.port1_current, width=6, relief="sunken")
        self.label_port1.grid(row=3, column=1)
        tk.Label(self.frame_current, text="mA").grid(row=3, column=2)

        tk.Label(self.frame_current, text="Total:").grid(row=4, column=0)
        self.label_total = tk.Label(self.frame_current, textvariable=self.system_current, width=6, relief="sunken")
        self.label_total.grid(row=4, column=1)
        tk.Label(self.frame_current, text="mA").grid(row=4, column=2)

        # Build Motor Sliders
        self.labels_ID = {}
        self.scales_angle = {}
        self.positions = {}
        self.state_checkBox = {}
        self.checkBox = {}
        self.labels_error = {}
        self.error_status = {}

        for i, id_str in enumerate(self.motorLimits):
            # Fixed-width label so slider column never shifts when value digits change
            self.labels_ID[id_str] = tk.Label(self.inner_monitor, text=f"ID:{id_str:>3}",
                                              width=14, anchor="w", font=("Courier", 10))
            self.labels_ID[id_str].grid(row=i, column=0, padx=2, sticky="W")
            
            min_ = self.motorLimits[id_str]["min"]
            max_ = self.motorLimits[id_str]["max"]
            ini_ = self.motorLimits[id_str]["ini"]
            
            self.positions[id_str] = tk.IntVar(self.root, value=ini_)
            self.scales_angle[id_str] = tk.Scale(self.inner_monitor, from_=min_, to_=max_, 
                                                 variable=self.positions[id_str], orient=tk.HORIZONTAL,
                                                 length=350)
            # Track which slider is being dragged to block observe_hardware overwrites
            self.scales_angle[id_str].bind("<ButtonPress-1>",
                lambda e, k=id_str: self._on_slider_press(k))
            self.scales_angle[id_str].bind("<ButtonRelease-1>",
                lambda e, k=id_str: self._on_slider_release_for(k))
            self.scales_angle[id_str].grid(row=i, column=1, padx=2, sticky="EW")
            self.inner_monitor.grid_columnconfigure(1, weight=1)
            
            self.state_checkBox[id_str] = tk.BooleanVar(self.root, value=False)
            self.checkBox[id_str] = tk.Checkbutton(self.inner_monitor, text="Include",
                                                   variable=self.state_checkBox[id_str],
                                                   state=tk.DISABLED)  # enabled only on keyposes
            self.checkBox[id_str].grid(row=i, column=2, padx=2)
            
            self.error_status[id_str] = tk.StringVar(self.root, value="OK")
            self.labels_error[id_str] = tk.Label(self.inner_monitor, textvariable=self.error_status[id_str], width=10)
            self.labels_error[id_str].grid(row=i, column=3, padx=2)

            # Per-motor reboot button
            tk.Button(self.inner_monitor, text="🔄", width=3,
                      command=lambda k=id_str: self._reboot_motor(k)
                      ).grid(row=i, column=4, padx=2)

    def _reboot_motor(self, id_str: str):
        """Send a reboot command for a single motor (with confirmation)."""
        if not messagebox.askyesno("Reboot Motor",
                                   f"Motor ID {id_str} を再起動しますか？\n"
                                   "トルクOFFになった後、自動で再初期化されます。"):
            return
        self.ros_manager.reboot_motor(int(id_str))
        print(f"Reboot sent to motor {id_str}.")

    def fileDialog(self):
        fTyp = [("JSON Motion", "*.json")]
        iDir = os.path.expanduser("~/CS_Animatronics/MotionFiles")
        if not os.path.exists(iDir):
            os.makedirs(iDir)
        file_name = tk.filedialog.askopenfilename(filetypes=fTyp, initialdir=iDir)
        if file_name:
            self.selectedFile.set(file_name)
            self.loadMotionFile()

    def loadMotionFile(self):
        try:
            with open(self.selectedFile.get(), "r") as f:
                self.motionFile = json.load(f)
            
            if self.motionFile:
                # Ensure timestamps are floats
                for entry in self.motionFile:
                    entry["timestamp"] = float(entry["timestamp"])
                
                self.motionFile.sort(key=lambda x: x["timestamp"])
                max_t = self.motionFile[-1]["timestamp"]
                # Auto adjust timeline
                if max_t > self.timeMax.get():
                    self.timeMax.set(max_t + 2.0)
                    self.scale_time.config(to_=self.timeMax.get())
                    self.lbl_max_time.config(text=f"{self.timeMax.get()}s")
                    
                self.update_sliders_from_timeline()
                messagebox.showinfo("Loaded", f"Loaded {len(self.motionFile)} keyposes.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load JSON: {e}")

    def saveMotionFile(self):
        if not self.motionFile:
            messagebox.showwarning("Warning", "No motion data to save.")
            return

        fTyp = [("JSON Motion", "*.json")]
        iDir = os.path.expanduser("~/CS_Animatronics/MotionFiles")
        if not os.path.exists(iDir):
            os.makedirs(iDir)
        file_name = tk.filedialog.asksaveasfilename(defaultextension=".json", filetypes=fTyp, initialdir=iDir)
        if file_name:
            self.motionFile.sort(key=lambda x: x["timestamp"])
            try:
                with open(file_name, "w", encoding="utf-8") as f:
                    json.dump(self.motionFile, f, indent=2)
                self.selectedFile.set(file_name)
                messagebox.showinfo("Saved", "Motion file saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save JSON: {e}")

    def moveForward(self):
        self.timeMax.set(self.timeMax.get() + 1.0)
        self.scale_time.config(to_=self.timeMax.get())
        self.lbl_max_time.config(text=f"{self.timeMax.get()}s")

    def moveBackward(self):
        if self.timeMax.get() > 1.0:
            self.timeMax.set(self.timeMax.get() - 1.0)
            self.scale_time.config(to_=self.timeMax.get())
            self.lbl_max_time.config(text=f"{self.timeMax.get()}s")

    def add_keypose(self):
        t = round(self.timestamp.get(), 1)
        angles = {}
        for id_str in self.motorLimits:
            if self.state_checkBox[id_str].get():
                angles[id_str] = self.positions[id_str].get()
                
        if not angles:
            messagebox.showwarning("Warning", "No motors selected (Include checkbox) for this keypose.")
            return

        # Check if exists
        updated = False
        for entry in self.motionFile:
            if abs(entry["timestamp"] - t) < 0.05:
                entry["angles"] = angles
                updated = True
                break
                
        if not updated:
            self.motionFile.append({"timestamp": t, "angles": angles})
            self.motionFile.sort(key=lambda x: x["timestamp"])
            
        print(f"Keypose set at {t}s")

    def delete_keypose(self):
        t = round(self.timestamp.get(), 1)
        new_file = [e for e in self.motionFile if abs(e["timestamp"] - t) >= 0.05]
        if len(new_file) < len(self.motionFile):
            self.motionFile = new_file
            print(f"Keypose at {t}s deleted.")
        else:
            print(f"No keypose found at {t}s.")

    def _on_slider_press(self, id_str):
        """Called when user starts dragging a slider — blocks observe_hardware overwrites."""
        self._editing_id = id_str

    def _on_slider_release_for(self, id_str):
        """Send just this motor's current position immediately on release."""
        angle = self.positions[id_str].get()
        self.ros_manager.set_positions([int(id_str)], [angle])
        self._editing_id = None

    def on_slider_release(self, event):
        # Legacy: send all Include-checked motors (called from update_sliders_from_timeline)
        ids = []
        angles = []
        for id_str in self.motorLimits:
            if self.state_checkBox[id_str].get():
                ids.append(int(id_str))
                angles.append(self.positions[id_str].get())
        if ids:
            self.ros_manager.set_positions(ids, angles)

    def val_to_color(self, val, min_val=0, max_val=100):
        norm = (val - min_val) / (max_val - min_val)
        norm = max(0.0, min(1.0, norm))
        r = int(255 * norm)
        g = 0
        b = int(255 * (1 - norm))
        return f"#{r:02x}{g:02x}{b:02x}"

    def toggle_edit_mode(self):
        """Switch between EDIT mode (free slider editing) and PREVIEW mode (timeline-driven)."""
        self.edit_mode = not self.edit_mode
        if self.edit_mode:
            # Switch to EDIT: enable all checkboxes, update button style
            self.btn_edit.config(text="✏️ EDIT MODE: ON", bg="#ffa500", fg="white")
            self.frame_monitor.config(text="Motor Control [✂ EDIT MODE - Free Edit]")
            for id_str in self.motorLimits:
                self.checkBox[id_str].config(state=tk.NORMAL)
        else:
            # Switch to PREVIEW: restore timeline-driven behaviour
            self.btn_edit.config(text="✏️ EDIT MODE: OFF", bg="#d0d0d0", fg="black")
            self.frame_monitor.config(text="Motor Control (Edit Position)")
            # Force a timeline refresh so sliders/checkboxes re-sync
            self.last_timestamp.set(-1.0)

    def update_sliders_from_timeline(self):
        t = round(self.timestamp.get(), 1)
        
        # --- EDIT mode: do not overwrite anything the user has set ---
        if self.edit_mode:
            return
        
        # Check if exactly on a keypose
        exact_entry = next((e for e in self.motionFile if abs(e["timestamp"] - t) < 0.05), None)
        
        if exact_entry:
            # ON a keypose: update sliders and Include checkboxes from keypose data
            angles = exact_entry["angles"]
            for id_str in self.motorLimits:
                if id_str in angles:
                    self.positions[id_str].set(angles[id_str])
                    self.state_checkBox[id_str].set(True)
                else:
                    self.state_checkBox[id_str].set(False)
                # Enable the checkbox so user can edit which motors are included
                self.checkBox[id_str].config(state=tk.NORMAL)
        else:
            # NOT on a keypose: disable and uncheck all Include boxes
            for id_str in self.motorLimits:
                self.state_checkBox[id_str].set(False)
                self.checkBox[id_str].config(state=tk.DISABLED)
            # Interpolate slider positions for preview only (don't change Include)
            self.interpolate_and_preview(t)
            
        # Send to ROS ONLY if we are NOT playing back automatically
        # (trajectory_interpolator handles automatic playback)
        if self._play_start_wall is None:
            self.on_slider_release(None)
        
    def interpolate_and_preview(self, t):
        """Update slider positions by interpolating between keyposes. Does NOT touch Include state."""
        if len(self.motionFile) < 2:
            return
            
        before = None
        after = None
        for e in self.motionFile:
            if e["timestamp"] <= t:
                before = e
            elif e["timestamp"] > t and after is None:
                after = e
                
        if before and after:
            ratio = (t - before["timestamp"]) / (after["timestamp"] - before["timestamp"])
            for id_str in self.motorLimits:
                if id_str in before["angles"] and id_str in after["angles"]:
                    val1 = before["angles"][id_str]
                    val2 = after["angles"][id_str]
                    val_int = int(val1 + ratio * (val2 - val1))
                    self.positions[id_str].set(val_int)
                    # NOTE: Include state is NOT changed here

    def playMotion(self):
        if not self.motionFile:
            messagebox.showwarning("Warning", "No motion data to play.")
            return
            
        self.motionFile.sort(key=lambda x: x["timestamp"])
        
        msg = JointTrajectory()
        # Collect all unique joint names used across the whole motion
        all_joints = set()
        for e in self.motionFile:
            for k in e["angles"].keys():
                all_joints.add(str(k))
        
        msg.joint_names = list(all_joints)
        
        for entry in self.motionFile:
            point = JointTrajectoryPoint()
            # Convert float timestamp to builtin_interfaces Duration
            sec = int(entry["timestamp"])
            nanosec = int((entry["timestamp"] - sec) * 1e9)
            point.time_from_start = Duration(sec=sec, nanosec=nanosec)
            
            point.positions = []
            for j in msg.joint_names:
                # If a keypose is missing a joint, ideally it should hold or interpolate, 
                # but for simplicity, we use the initial limit value or current slider value
                val = entry["angles"].get(j, float(self.positions[j].get()))
                point.positions.append(float(val))
                
            msg.points.append(point)
            
        self.ros_manager.publish_trajectory(msg)
        
        # Start playback timer so the time slider tracks progress
        self._play_start_wall = time.time()
        self._play_total_duration = self.motionFile[-1]["timestamp"]  # already sorted
        # Rewind the time slider to 0 before starting
        self.timestamp.set(0.0)
        self.last_timestamp.set(-1.0)
        print(f"Trajectory published! Duration: {self._play_total_duration:.1f}s")

    def stopMotion(self):
        """Stop ongoing trajectory playback by sending an empty JointTrajectory."""
        self.ros_manager.stop_trajectory()
        self._play_start_wall = None  # stop the UI timer too
        print("Trajectory STOP sent.")

    def sync_sliders_from_hardware(self):
        """Button handler: one-shot sync of all sliders from current hardware positions."""
        if self._syncing:
            print("Sync already in progress, please wait...")
            return
        self._syncing = True
        ids_ = [int(x) for x in self.motorLimits.keys()]

        def on_response(future):
            try:
                response = future.result()
                for i, id_val in enumerate(response.ids):
                    id_str = str(id_val)
                    if i < len(response.positions) and id_str in self.positions:
                        hw_pos = int(response.positions[i])
                        self.positions[id_str].set(hw_pos)
                        self.hardware_positions[id_str] = hw_pos
                        if id_str in self.labels_ID:
                            self.labels_ID[id_str].config(text=f"ID:{id_str:>3} [{hw_pos:>4}]")
                self.port0_current.set(response.port0_total_current)
                self.port1_current.set(response.port1_total_current)
                self.system_current.set(response.system_total_current)
                print("Sliders synced from hardware.")
            except Exception as e:
                print(f"Sync from hardware failed: {e}")
            finally:
                self._syncing = False

        called = self.ros_manager.call_get_motor_states(
            ids_, lambda fut: self.root.after(0, lambda: on_response(fut)))
        if not called:
            print("get_motor_states service not available.")
            self._syncing = False

    def observe_hardware(self):
        if not self.observe_mode.get():
            return
            
        current_time = time.time()
        if self.is_service_calling or (current_time - self.last_observe_time < 0.2):
            return
            
        self.is_service_calling = True
        self.last_observe_time = current_time
        ids_ = [int(x) for x in self.motorLimits.keys()]
        
        def on_response(future):
            try:
                response = future.result()
                for i, id_val in enumerate(response.ids):
                    id_str = str(id_val)
                    
                    # --- Update error status label ---
                    if id_str in self.error_status:
                        err = response.error_status[i] if i < len(response.error_status) else "NO_ERROR"
                        self.error_status[id_str].set("OK" if err == "NO_ERROR" else "ERR")
                        bg_col = "lightgreen" if err == "NO_ERROR" else "red"
                        self.labels_error[id_str].configure(bg=bg_col)
                    
                    # --- Sync slider to actual motor position ---
                    if i < len(response.positions) and id_str in self.positions:
                        hw_pos = int(response.positions[i])
                        self.hardware_positions[id_str] = hw_pos
                        
                        # Do NOT overwrite the slider if:
                        #   1. The user is actively dragging this slider, OR
                        #   2. The timeline was recently moved (within 0.5 s)
                        timeline_busy = (time.time() - self._timeline_updated_at) < 0.5
                        if self._editing_id == id_str or timeline_busy:
                            # Just update the label without touching the slider value
                            if id_str in self.labels_ID:
                                self.labels_ID[id_str].config(
                                    text=f"ID:{id_str:>3} [~{hw_pos:>4}]")
                            continue
                        
                        # Safe to sync slider to hardware position
                        self.positions[id_str].set(hw_pos)
                        
                        # Update the ID label to show current position (fixed width)
                        if id_str in self.labels_ID:
                            self.labels_ID[id_str].config(
                                text=f"ID:{id_str:>3} [{hw_pos:>4}]")
                        
                self.port0_current.set(response.port0_total_current)
                self.port1_current.set(response.port1_total_current)
                self.system_current.set(response.system_total_current)
            except Exception as e:
                pass
            finally:
                self.is_service_calling = False
                
        called = self.ros_manager.call_get_motor_states(ids_, lambda fut: self.root.after(0, lambda: on_response(fut)))
        if not called:
            self.is_service_calling = False  # サービス未応答時にフラグをリセット

    def main_loop(self):
        # --- Playback timer: advance time slider to match trajectory progress ---
        if self._play_start_wall is not None:
            elapsed = time.time() - self._play_start_wall
            if elapsed <= self._play_total_duration:
                # Quantise to 0.1 s resolution to match slider
                new_t = round(min(elapsed, self._play_total_duration), 1)
                self.timestamp.set(new_t)
            else:
                # Reached end: hold the last pose, stop the timer
                self.timestamp.set(self._play_total_duration)
                self._play_start_wall = None
                print("Playback finished.")

        t = self.timestamp.get()
        if t != self.last_timestamp.get():
            self._timeline_updated_at = time.time()  # mark timeline as recently moved
            self.update_sliders_from_timeline()
            self.last_timestamp.set(t)
            
        self.observe_hardware()
        self.root.after(20, self.main_loop)

def main():
    rclpy.init()
    ros_manager = ROSManager()
    ros_thread = threading.Thread(target=rclpy.spin, args=(ros_manager,), daemon=True)
    ros_thread.start()

    app = MotionEditor(ros_manager, tk.Tk())
    app.root.title("Keypose Motion Editor")
    app.root.geometry("1200x800")
    app.root.minsize(900, 600)
    # Allow the motor slider column to grow with window resize
    app.root.grid_rowconfigure(2, weight=1)
    app.root.grid_columnconfigure(0, weight=1)
    app.root.mainloop()

    ros_manager.destroy_node()
    rclpy.shutdown()
    ros_thread.join()
    
if __name__ == "__main__":
    main()

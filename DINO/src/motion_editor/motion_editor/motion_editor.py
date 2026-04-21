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
from std_msgs.msg import Int32, String

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
        self.audio_id_pub = self.create_publisher(Int32, 'play_audio_id', 10)
        self.audio_name_pub = self.create_publisher(String, 'play_audio_name', 10)

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

    def play_audio(self, audio_id=None, audio_name=None):
        if audio_id is not None:
            msg = Int32()
            msg.data = int(audio_id)
            self.audio_id_pub.publish(msg)
        if audio_name:
            filename = audio_name if audio_name.endswith(".wav") else f"{audio_name}.wav"
            msg = String()
            msg.data = filename
            self.audio_name_pub.publish(msg)

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
        
        # Audio cue controls
        self.audio_id_var = tk.StringVar(self.root, value="")
        initial_audio_names = ["(none)"] + self._load_audio_file_names()
        self.audio_name_options = initial_audio_names
        self.audio_name_var = tk.StringVar(self.root, value=initial_audio_names[0] if initial_audio_names else "(none)")
        self.audio_event_entries = []
        self.audio_timers = []
        
        # Track which slider the user is currently dragging (None = not dragging)
        self._editing_id = None
        # Track when timeline was last updated to temporarily block observe overwrites
        self._timeline_updated_at = 0.0
        
        # Keep track of actual hardware positions (for display only, won't override user edits)
        self.hardware_positions = {}  # {id_str: int}
        
        # Current displays
        self.port0_current = tk.IntVar(self.root)
        self.port1_current = tk.IntVar(self.root)
        self.port2_current = tk.IntVar(self.root)
        self.system_current = tk.IntVar(self.root)
        
        # Load Motor Limits
        self.motorLimits = {}
        self.loadMotorLimits()

        self.selectedFile = tk.StringVar(value="Not Selected")

        # Controller button assignment support
        dino_root = os.environ.get("DINO_ROOT_DIR", os.path.expanduser("~/CS_Animatronics/DINO"))
        self.controller_map_path = os.path.join(dino_root, "ControllerMap.json")
        self.controller_button_labels = {
            "0": "Cross",
            "1": "Circle",
            "2": "Square",
            "3": "Triangle",
            "4": "L1",
            "5": "R1",
            "6": "L2",
            "7": "R2",
            "8": "Share",
            "9": "Options",
            "11": "L3",
            "12": "R3",
        }
        self.controller_map = self.load_controller_map()
        self.controller_button_choices = [
            f"{bid}: {label}" for bid, label in self.controller_button_labels.items()
        ]
        default_choice = self.controller_button_choices[0]
        self.selected_button_display = tk.StringVar(self.root, value=default_choice)
        self.current_assignment = tk.StringVar(self.root, value="(none)")

        self.setup_ui()
        
        # Start main loop at 50Hz for smooth playback UI
        self.root.after(20, self.main_loop)

    def loadMotorLimits(self):
        try:
            dino_root = os.environ.get("DINO_ROOT_DIR", os.path.expanduser("~/CS_Animatronics/DINO"))
            with open(os.path.join(dino_root, "Motor_Limits.json"), "r", encoding="utf-8") as file:
                data = json.load(file)
            for key, subdict in data.items():
                subdict["ini"] = int(subdict["ini"])
                subdict["min"] = int(subdict["min"])
                subdict["max"] = int(subdict["max"])
            self.motorLimits = data
        except Exception as e:
            print(f"Failed to load Motor_Limits.json: {e}")

    def _load_audio_file_names(self):
        dino_root = os.environ.get("DINO_ROOT_DIR", os.path.expanduser("~/CS_Animatronics/DINO"))
        audio_dir = os.path.join(dino_root, "AudioFiles")
        names = []
        try:
            if os.path.isdir(audio_dir):
                for fname in sorted(os.listdir(audio_dir)):
                    if fname.lower().endswith(".wav"):
                        names.append(os.path.splitext(fname)[0])
        except Exception as e:
            print(f"Failed to list AudioFiles: {e}")
        return names

    def load_controller_map(self):
        try:
            if os.path.exists(self.controller_map_path):
                with open(self.controller_map_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, dict):
                        return data
        except Exception as e:
            print(f"Failed to load ControllerMap.json: {e}")
        return {}

    def save_controller_map(self):
        try:
            directory = os.path.dirname(self.controller_map_path)
            if directory and not os.path.exists(directory):
                os.makedirs(directory, exist_ok=True)
            with open(self.controller_map_path, "w", encoding="utf-8") as f:
                json.dump(self.controller_map, f, indent=2)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update ControllerMap.json: {e}")
            raise

    def _get_selected_button_id(self):
        value = self.selected_button_display.get()
        if not value:
            return None
        return value.split(":", 1)[0].strip()

    def _on_button_selection_change(self, *_):
        self.update_assignment_label()

    def update_assignment_label(self):
        btn_id = self._get_selected_button_id()
        path = self.controller_map.get(btn_id)
        if path:
            display = os.path.basename(path)
        else:
            display = "(none)"
        self.current_assignment.set(display)

    def assign_motion_to_button(self):
        btn_id = self._get_selected_button_id()
        if not btn_id:
            messagebox.showwarning("Warning", "No controller button selected.")
            return

        current_file = self.selectedFile.get()
        if not current_file or current_file == "Not Selected":
            messagebox.showwarning("Warning", "Please open or save a motion file first.")
            return
        if not os.path.exists(current_file):
            messagebox.showwarning("Warning", "Selected motion file does not exist. Please save it before assigning.")
            return

        self.controller_map[btn_id] = current_file
        try:
            self.save_controller_map()
        except Exception:
            return

        self.update_assignment_label()
        messagebox.showinfo("Assigned", f"Assigned {os.path.basename(current_file)} to button {btn_id}.")

    def refresh_audio_list(self):
        names = self._load_audio_file_names()
        options = ["(none)"] + names
        self.audio_name_options = options
        if hasattr(self, "combo_audio"):
            self.combo_audio["values"] = options
        if self.audio_name_var.get() not in options:
            self.audio_name_var.set(options[0])

    def clear_audio_selection(self):
        self.audio_id_var.set("")
        if self.audio_name_options:
            self.audio_name_var.set(self.audio_name_options[0])
        else:
            self.audio_name_var.set("(none)")

    def _build_audio_payload(self):
        payload = {}
        audio_id_text = self.audio_id_var.get().strip()
        if audio_id_text:
            try:
                payload["audio_id"] = int(audio_id_text)
            except ValueError:
                messagebox.showerror("Invalid Audio ID", "Audio ID must be an integer.")
                return None, False
        audio_name = self.audio_name_var.get()
        if audio_name and audio_name != "(none)":
            payload["audio_name"] = audio_name
        if payload:
            return payload, True
        return None, True

    def _apply_audio_from_entry(self, entry):
        audio = entry.get("audio")
        if isinstance(audio, dict):
            audio_id = audio.get("audio_id")
            audio_name = audio.get("audio_name")
            self.audio_id_var.set(str(audio_id) if audio_id is not None else "")
            if audio_name:
                if audio_name not in self.audio_name_options:
                    self.audio_name_options.append(audio_name)
                    if hasattr(self, "combo_audio"):
                        self.combo_audio["values"] = self.audio_name_options
                self.audio_name_var.set(audio_name)
            else:
                if self.audio_name_options:
                    self.audio_name_var.set(self.audio_name_options[0])
        else:
            self.clear_audio_selection()

    def refresh_audio_event_list(self):
        events = []
        for entry in sorted(self.motionFile, key=lambda x: x.get("timestamp", 0.0)):
            audio = entry.get("audio")
            if isinstance(audio, dict):
                ts = float(entry.get("timestamp", 0.0))
                parts = []
                if "audio_id" in audio:
                    parts.append(f"ID:{audio['audio_id']}")
                if "audio_name" in audio:
                    parts.append(f"NAME:{audio['audio_name']}")
                if parts:
                    events.append((ts, ", ".join(parts)))
        self.audio_event_entries = events
        if hasattr(self, "audio_event_list"):
            self.audio_event_list.delete(0, tk.END)
            for ts, desc in events:
                self.audio_event_list.insert(tk.END, f"{ts:6.1f}s  {desc}")

    def on_audio_event_select(self, *_):
        if not hasattr(self, "audio_event_list"):
            return
        selection = self.audio_event_list.curselection()
        if not selection:
            return
        idx = selection[0]
        if idx >= len(self.audio_event_entries):
            return
        ts, _ = self.audio_event_entries[idx]
        self.timestamp.set(round(ts, 1))
        self.last_timestamp.set(-1.0)
        self.update_sliders_from_timeline()

    def remove_audio_from_current(self):
        t = round(self.timestamp.get(), 1)
        modified = False
        for entry in self.motionFile:
            if abs(entry.get("timestamp", 0.0) - t) < 0.05 and "audio" in entry:
                entry.pop("audio", None)
                modified = True
        if modified:
            self.clear_audio_selection()
            self.refresh_audio_event_list()
            messagebox.showinfo("Audio", f"Removed audio cue at {t:.1f}s")

    def update_keypose_markers(self):
        if not hasattr(self, "keypose_canvas"):
            return
        canvas = self.keypose_canvas
        canvas.delete("marker")
        width = canvas.winfo_width()
        if width <= 1:
            width = canvas.winfo_reqwidth()
        if width <= 1 or not self.motionFile:
            return
        time_min = self.timeMin.get()
        time_span = max(0.1, self.timeMax.get() - time_min)
        for entry in sorted(self.motionFile, key=lambda e: e.get("timestamp", 0.0)):
            t = float(entry.get("timestamp", 0.0))
            normalized = max(0.0, min(1.0, (t - time_min) / time_span))
            x = normalized * width
            canvas.create_line(x, 0, x, canvas.winfo_height(), fill="#ff6600", tags="marker")

    def _cancel_audio_timers(self):
        for timer in self.audio_timers:
            try:
                timer.cancel()
            except Exception:
                pass
        self.audio_timers = []

    def _schedule_audio_events(self, events):
        self._cancel_audio_timers()
        if not events:
            return
        for event in events:
            delay = max(0.0, float(event.get("timestamp", 0.0)))
            timer = threading.Timer(delay, self._fire_audio_event, args=(event,))
            timer.daemon = True
            timer.start()
            self.audio_timers.append(timer)

    def _fire_audio_event(self, event):
        audio_id = event.get("audio_id")
        audio_name = event.get("audio_name")
        self.ros_manager.play_audio(audio_id=audio_id, audio_name=audio_name)

    def setup_ui(self):
        for child in self.root.winfo_children():
            child.destroy()

        self.main_paned = ttk.Panedwindow(self.root, orient=tk.VERTICAL)
        self.main_paned.pack(fill="both", expand=True)

        self.top_section = ttk.Frame(self.main_paned)
        self.bottom_paned = ttk.Panedwindow(self.main_paned, orient=tk.HORIZONTAL)
        self.main_paned.add(self.top_section, weight=1)
        self.main_paned.add(self.bottom_paned, weight=4)

        self.monitor_container = ttk.Frame(self.bottom_paned)
        self.side_container = ttk.Frame(self.bottom_paned)
        self.bottom_paned.add(self.monitor_container, weight=3)
        self.bottom_paned.add(self.side_container, weight=2)

        # Settings Frame
        self.frame_settings = tk.LabelFrame(self.top_section, text="File Settings", foreground="green")
        self.frame_settings.pack(fill="x", padx=5, pady=5)
        self.frame_settings.grid_columnconfigure(0, weight=1)
        self.frame_settings.grid_columnconfigure(1, weight=1)
        
        tk.Label(self.frame_settings, textvariable=self.selectedFile, width=40).grid(row=0, column=0, columnspan=2, sticky="EW")
        tk.Button(self.frame_settings, text="Open JSON", command=self.fileDialog).grid(row=1, column=0, pady=5, sticky="EW")
        tk.Button(self.frame_settings, text="Save JSON", command=self.saveMotionFile).grid(row=1, column=1, pady=5, sticky="EW")
        
        # Operations Frame
        self.frame_operations = tk.LabelFrame(self.top_section, text="Timeline & Keyposes", foreground="green")
        self.frame_operations.pack(fill="x", padx=5, pady=5)
        self.frame_operations.grid_columnconfigure(2, weight=1)
        self.frame_operations.grid_rowconfigure(0, weight=0)
        
        tk.Button(self.frame_operations, text="< -1s", command=self.moveBackward).grid(row=0, column=0)
        tk.Label(self.frame_operations, text="0.0s").grid(row=0, column=1)
        
        self.scale_time = tk.Scale(self.frame_operations, from_=self.timeMin.get(), to_=self.timeMax.get(), 
                                   variable=self.timestamp, orient=tk.HORIZONTAL, resolution=0.1, length=400)
        self.scale_time.grid(row=0, column=2, padx=10, sticky="EW")
        # Keypose markers along the timeline
        self.keypose_canvas = tk.Canvas(self.frame_operations, height=8, bg="#f0f0f0", highlightthickness=0)
        self.keypose_canvas.grid(row=1, column=0, columnspan=5, sticky="EW", padx=10, pady=(2, 6))
        self.keypose_canvas.bind("<Configure>", lambda e: self.update_keypose_markers())
        
        self.lbl_max_time = tk.Label(self.frame_operations, text=f"{self.timeMax.get()}s")
        self.lbl_max_time.grid(row=0, column=3)
        tk.Button(self.frame_operations, text="+1s >", command=self.moveForward).grid(row=0, column=4)
        
        tk.Button(self.frame_operations, text="Add/Update Keypose (At Current Time)", bg="lightblue", command=self.add_keypose).grid(row=2, column=1, columnspan=2, pady=6)
        tk.Button(self.frame_operations, text="Delete Keypose", bg="#ff9999", command=self.delete_keypose).grid(row=2, column=3, pady=6)
        
        # Edit / Preview toggle button
        self.btn_edit = tk.Button(self.frame_operations, text="✏️ EDIT MODE: OFF",
                                  bg="#d0d0d0", width=18, command=self.toggle_edit_mode)
        self.btn_edit.grid(row=3, column=0, columnspan=1, pady=5, padx=4)
        
        tk.Button(self.frame_operations, text="▶ PLAY Trajectory", bg="lightgreen", command=self.playMotion).grid(row=3, column=1, pady=5)
        tk.Button(self.frame_operations, text="⏹ STOP", bg="#ff6666", fg="white", font=("TkDefaultFont", 10, "bold"),
                  command=self.stopMotion).grid(row=3, column=2, pady=5)
        
        # Monitor Frame (Sliders)
        self.frame_monitor = tk.LabelFrame(self.monitor_container, text="Motor Control (Edit Position)", foreground="green")
        self.frame_monitor.pack(fill="both", expand=True, padx=5, pady=5)
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
        self.frame_current = tk.LabelFrame(self.side_container, text="System Status", foreground="blue")
        self.frame_current.pack(fill="x", padx=5, pady=5)
        for col in range(3):
            self.frame_current.grid_columnconfigure(col, weight=1 if col == 1 else 0)
        self.frame_current.grid_rowconfigure(5, weight=1)
        
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

        tk.Label(self.frame_current, text="PORT2:").grid(row=4, column=0)
        self.label_port2 = tk.Label(self.frame_current, textvariable=self.port2_current, width=6, relief="sunken")
        self.label_port2.grid(row=4, column=1)
        tk.Label(self.frame_current, text="mA").grid(row=4, column=2)

        tk.Label(self.frame_current, text="Total:").grid(row=5, column=0)
        self.label_total = tk.Label(self.frame_current, textvariable=self.system_current, width=6, relief="sunken")
        self.label_total.grid(row=5, column=1)
        tk.Label(self.frame_current, text="mA").grid(row=5, column=2)

        # Controller assignment frame
        self.frame_assignment = tk.LabelFrame(self.side_container, text="Controller Button Assignment", foreground="purple")
        self.frame_assignment.pack(fill="x", padx=5, pady=5)
        self.frame_assignment.grid_columnconfigure(1, weight=1)

        tk.Label(self.frame_assignment, text="Button:").grid(row=0, column=0, padx=4, pady=4, sticky="W")
        self.combo_buttons = ttk.Combobox(
            self.frame_assignment,
            state="readonly",
            values=self.controller_button_choices,
            textvariable=self.selected_button_display,
            width=18,
        )
        self.combo_buttons.grid(row=0, column=1, padx=4, pady=4, sticky="EW")
        self.combo_buttons.bind("<<ComboboxSelected>>", self._on_button_selection_change)

        tk.Label(self.frame_assignment, text="Currently Assigned:").grid(row=1, column=0, padx=4, pady=4, sticky="W")
        tk.Label(self.frame_assignment, textvariable=self.current_assignment, width=30, relief="sunken").grid(
            row=1, column=1, padx=4, pady=4, sticky="W"
        )
        tk.Button(
            self.frame_assignment,
            text="Assign current motion file",
            bg="#d4ffd4",
            command=self.assign_motion_to_button,
        ).grid(row=2, column=0, columnspan=2, pady=6, sticky="EW")

        self.update_assignment_label()
        # Audio cue frame
        self.frame_audio = tk.LabelFrame(self.side_container, text="Audio Cue (per keypose)", foreground="purple")
        self.frame_audio.pack(fill="both", expand=True, padx=5, pady=5)
        self.frame_audio.grid_columnconfigure(1, weight=1)
        self.frame_audio.grid_rowconfigure(5, weight=1)
        tk.Label(self.frame_audio, text="Audio ID:").grid(row=0, column=0, padx=4, pady=4, sticky="W")
        tk.Entry(self.frame_audio, textvariable=self.audio_id_var, width=10).grid(row=0, column=1, padx=4, pady=4, sticky="EW")
        tk.Button(self.frame_audio, text="Clear ID", command=lambda: self.audio_id_var.set("")).grid(row=0, column=2, padx=4, pady=4, sticky="EW")

        tk.Label(self.frame_audio, text="Audio File:").grid(row=1, column=0, padx=4, pady=4, sticky="W")
        self.combo_audio = ttk.Combobox(
            self.frame_audio,
            state="readonly",
            values=self.audio_name_options,
            textvariable=self.audio_name_var,
            width=25,
        )
        self.combo_audio.grid(row=1, column=1, padx=4, pady=4, sticky="EW")
        tk.Button(self.frame_audio, text="Refresh list", command=self.refresh_audio_list).grid(row=1, column=2, padx=4, pady=4, sticky="EW")
        tk.Button(self.frame_audio, text="Clear audio fields", command=self.clear_audio_selection).grid(row=2, column=0, columnspan=3, pady=4, sticky="EW")
        tk.Button(self.frame_audio, text="Remove cue at current time", command=self.remove_audio_from_current).grid(row=3, column=0, columnspan=3, pady=4, sticky="EW")

        tk.Label(self.frame_audio, text="Timeline Cues:").grid(row=4, column=0, padx=4, pady=(8, 2), sticky="W")
        self.audio_event_list = tk.Listbox(self.frame_audio, height=6, width=45)
        self.audio_event_list.grid(row=5, column=0, columnspan=3, padx=4, pady=4, sticky="NSEW")
        self.audio_event_list.bind("<<ListboxSelect>>", self.on_audio_event_select)

        self.refresh_audio_list()
        self.refresh_audio_event_list()

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
        dino_root = os.environ.get("DINO_ROOT_DIR", os.path.expanduser("~/CS_Animatronics/DINO"))
        iDir = os.path.join(dino_root, "MotionFiles")
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
                self.update_keypose_markers()
                self.refresh_audio_event_list()
                messagebox.showinfo("Loaded", f"Loaded {len(self.motionFile)} keyposes.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load JSON: {e}")

    def saveMotionFile(self):
        if not self.motionFile:
            messagebox.showwarning("Warning", "No motion data to save.")
            return

        fTyp = [("JSON Motion", "*.json")]
        dino_root = os.environ.get("DINO_ROOT_DIR", os.path.expanduser("~/CS_Animatronics/DINO"))
        iDir = os.path.join(dino_root, "MotionFiles")
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
        self.update_keypose_markers()

    def moveBackward(self):
        if self.timeMax.get() > 1.0:
            self.timeMax.set(self.timeMax.get() - 1.0)
            self.scale_time.config(to_=self.timeMax.get())
            self.lbl_max_time.config(text=f"{self.timeMax.get()}s")
            self.update_keypose_markers()

    def add_keypose(self):
        t = round(self.timestamp.get(), 1)
        angles = {}
        for id_str in self.motorLimits:
            if self.state_checkBox[id_str].get():
                angles[id_str] = self.positions[id_str].get()
                
        if not angles:
            messagebox.showwarning("Warning", "No motors selected (Include checkbox) for this keypose.")
            return

        audio_payload, ok = self._build_audio_payload()
        if not ok:
            return

        # Check if exists
        updated = False
        for entry in self.motionFile:
            if abs(entry["timestamp"] - t) < 0.05:
                entry["angles"] = angles
                if audio_payload:
                    entry["audio"] = audio_payload
                else:
                    entry.pop("audio", None)
                updated = True
                break
                
        if not updated:
            new_entry = {"timestamp": t, "angles": angles}
            if audio_payload:
                new_entry["audio"] = audio_payload
            self.motionFile.append(new_entry)
            self.motionFile.sort(key=lambda x: x["timestamp"])
            
        print(f"Keypose set at {t}s")
        self.refresh_audio_event_list()
        self.update_keypose_markers()

    def delete_keypose(self):
        t = round(self.timestamp.get(), 1)
        new_file = [e for e in self.motionFile if abs(e["timestamp"] - t) >= 0.05]
        if len(new_file) < len(self.motionFile):
            self.motionFile = new_file
            print(f"Keypose at {t}s deleted.")
            self.update_keypose_markers()
            self.refresh_audio_event_list()
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
            self._apply_audio_from_entry(exact_entry)
        else:
            # NOT on a keypose: disable and uncheck all Include boxes
            for id_str in self.motorLimits:
                self.state_checkBox[id_str].set(False)
                self.checkBox[id_str].config(state=tk.DISABLED)
            # Interpolate slider positions for preview only (don't change Include)
            self.interpolate_and_preview(t)
            self.clear_audio_selection()
            
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
        audio_events = []
        
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

            audio_info = entry.get("audio")
            if isinstance(audio_info, dict):
                event = {"timestamp": float(entry["timestamp"])}
                if "audio_id" in audio_info:
                    try:
                        event["audio_id"] = int(audio_info["audio_id"])
                    except (ValueError, TypeError):
                        pass
                if "audio_name" in audio_info:
                    name = str(audio_info["audio_name"]).strip()
                    if name.endswith(".wav"):
                        name = name[:-4]
                    if name:
                        event["audio_name"] = name
                if any(key in event for key in ("audio_id", "audio_name")):
                    audio_events.append(event)
            
        self.ros_manager.publish_trajectory(msg)
        self._schedule_audio_events(audio_events)
        
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
        self._cancel_audio_timers()
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
                p0 = getattr(response, "port0_total_current", 0)
                p1 = getattr(response, "port1_total_current", 0)
                total = getattr(response, "system_total_current", 0)
                p2 = total - p0 - p1
                self.port0_current.set(p0)
                self.port1_current.set(p1)
                self.port2_current.set(p2)
                self.system_current.set(total)
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
                        
                p0 = getattr(response, "port0_total_current", 0)
                p1 = getattr(response, "port1_total_current", 0)
                total = getattr(response, "system_total_current", 0)
                p2 = total - p0 - p1
                self.port0_current.set(p0)
                self.port1_current.set(p1)
                self.port2_current.set(p2)
                self.system_current.set(total)
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
    app.root.mainloop()

    ros_manager.destroy_node()
    rclpy.shutdown()
    ros_thread.join()
    
if __name__ == "__main__":
    main()

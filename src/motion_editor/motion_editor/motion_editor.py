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
from motor_command_msg.msg import IdAngle

class ROSManager(Node):
    def __init__(self):
        super().__init__('motion_editor_ros_client')
        
        self.publisher = self.create_publisher(
            IdAngle,
            'IdAngle',
            12
        )
        
        #self.get_position_client = self.create_client(GetPosition, 'get_position')
        #while not self.get_position_client.wait_for_service(timeout_sec=1.0):
            #self.get_logger().info('Waiting for get_position service...')
    
    def call_get_position(self):
        req = GetPosition.Request()
        future = self.get_position_client.call_async(req)
        rclpy.spin_until_future_complete(self, future)
        if future.result() is not None:
            return future.result()
        else:
            self.get_logger().error('Service call failed')
            return None

class MotionEditor:
    def __init__(self):
        ##################
        #### ROS init ####
        ##################
        rclpy.init(args=None)
        self.ros_manager = ROSManager()
        
        self.ros_thread = threading.Thread(target=rclpy.spin, args=(self.ros_manager,), daemon=True)
        self.ros_thread.start()

        # Main Loop
        self.root = tk.Tk()
        self.root.title("Motion Editor")
        self.root.geometry("1000x700")

        ########################
        ### Define Variables ###
        ########################
        # Motion JSON
        self.motionFile = None

        # Play Flag
        self.is_playing = False

        # Last updated time
        self.last_updated_time = time.time()

        # Start Time of Motion
        self.timeStartMotion = tk.IntVar(self.root)

        # End Time of Motion
        self.timeEndMotion = tk.IntVar(self.root)

        # Time at Edit Point
        self.timestamp = tk.IntVar(self.root)
        self.last_timestamp = tk.IntVar(self.root)     
  
        # Time Min
        self.timeMin = tk.IntVar(self.root)
        self.timeMin.set(0)

        # Scale span
        self.timeSpan = 100

        # Time Max
        self.timeMax = tk.IntVar(self.root)
        self.timeMax.set(self.timeMin.get() + self.timeSpan)
 
        # Mode
        # 0: Read
        # 1: Read & Write
        # 2: Edit
        self.mode = tk.IntVar(self.root)
        self.mode.set(0)
        
        # Load Motor Limits
        self.motorLimits = {}
        self.loadMotorLimits()

        # Selected File to Edit
        self.selectedFile = tk.StringVar()
        self.selectedFile.set("Selected File")


        ########################
        #### Prepare Frames ####
        ########################
        # Settings Frame
        self.frame_settings = tk.LabelFrame(self.root, text="Settings", foreground="green")
        self.frame_settings.grid(sticky="W", row=0, column=0, columnspan=2)
 
        # Monitor Frame 
        self.frame_monitor = tk.LabelFrame(self.root, text="Monitor", foreground="green")
        self.frame_monitor.grid(sticky="W", row=1, column=0)        

        # Operations Frame
        self.frame_operations = tk.LabelFrame(self.root, text="Operations", foreground="green")
        self.frame_operations.grid(sticky="W", row=1, column=1)
   

        ####################### 
        #### Setting Frame ####
        #######################
        # Seleced File Label
        self.label_selectedFile = tk.Label(self.frame_settings, textvariable=self.selectedFile)
        self.label_selectedFile.grid(row=0, column=2, columnspan=2)
        
        # Selected File Button
        self.button_selectedFile = tk.Button(self.frame_settings, text="Open filedialog", command=self.fileDialog)
        self.button_selectedFile.grid(row=1, column=2)
       
        # Load Selected File Button
        self.button_load = tk.Button(self.frame_settings, text="Load", command=self.loadMotionFile)
        self.button_load.grid(row=1, column=3) 
 
        # Mode Label
        self.label_mode = tk.Label(self.frame_settings, text="Current Mode")
        self.label_mode.grid(row=0, column=0)
        
        # Mode Dropbox
        self.combobox_mode = ttk.Combobox(self.frame_settings, state="readonly", values=("Send", "Write", "Edit"))
        self.combobox_mode.grid(row=0, column=1)
        
        # Mode Chose Button
        self.button_mode = tk.Button(self.frame_settings, text="Change Mode", command=self.changeMode)
        self.button_mode.grid(row=1, column=0, columnspan=2)

        # Start Time Entry
        self.entry_time_start_motion = tk.Entry(self.frame_settings, textvariable=self.timeStartMotion)
        self.entry_time_start_motion.grid(row=0, column=4)

        # End Time Entry
        self.entry_time_end_motion = tk.Entry(self.frame_settings, textvariable=self.timeEndMotion)
        self.entry_time_end_motion.grid(row=1, column=4)


        #######################
        #### Monitor Frame ####
        #######################
        # loop to make elements for each ID
        self.labels_ID = {}  # contains labels of ID
        self.scales_angle = {}  # contains scales of angles
        self.positions = {}  # contains position values from scale_angle
        self.state_checkBox = {}  # contains state of checkBox
        self.checkBox = {}  # contains checkBox
        for i, id in enumerate(self.motorLimits):
            # ID Label
            self.labels_ID[id] = tk.Label(self.frame_monitor, text="ID: " + id)
            self.labels_ID[id].grid(row=2*i, column=0)
        
            # Angle Slider
            min = self.motorLimits[id]["min"]
            max = self.motorLimits[id]["max"]
            self.positions[id] = tk.IntVar(self.root)
            self.scales_angle[id] = tk.Scale(self.frame_monitor, from_=min, to_=max, variable=self.positions[id], orient=tk.HORIZONTAL)
            self.scales_angle[id].grid(row=2*i, column=1, rowspan=2)

            # Check box
            self.state_checkBox[id] = tk.BooleanVar(self.root)
            self.checkBox[id] = tk.Checkbutton(self.frame_monitor, text="target", variable=self.state_checkBox[id])
            self.checkBox[id].grid(row=2*i+1, column=0)


        ##########################
        #### Operations Frame ####
        ##########################
        # Go Back Button
        self.button_goBack = tk.Button(self.frame_operations, text="<", command=self.moveBackward)
        self.button_goBack.grid(row=0, column=0)

        # Go Forward Button
        self.button_goForward = tk.Button(self.frame_operations, text=">", command=self.moveForward)
        self.button_goForward.grid(row=0, column=2)

        # Play Button
        self.button_play = tk.Button(self.frame_operations, text="play", command=self.playMotion)
        self.button_play.grid(row=1, column=1)

        # Stop Button
        self.button_stop = tk.Button(self.frame_operations, text="stop", command=self.stopMotion)
        self.button_stop.grid(row=1, column=0)

        # Minimum Time
        self.label_minimumTime = tk.Label(self.frame_operations, textvariable=self.timeMin)
        self.label_minimumTime.grid(row=0, column=1)

        # Time seacker
        self.scale_time = tk.Scale(self.frame_operations, from_=self.timeMin.get(), to_=self.timeMax.get(), variable=self.timestamp, orient=tk.HORIZONTAL, label="time(s)", length=200)
        self.scale_time.grid(row=0, column=3, rowspan=2)


        self.root.after(100, self.main)
        self.root.mainloop()
        
    def loadMotorLimits(self):
        # load motor limits
        with open("../../../Motor_Limits.json", "r", encoding="utf-8") as file:
            data = json.load(file)
            
        for key, subdict in data.items():
            subdict["ini"] = int(subdict["ini"])
            subdict["min"] = int(subdict["min"])
            subdict["max"] = int(subdict["max"])
            subdict["acc"] = int(subdict["acc"])
            subdict["vel"] = int(subdict["vel"])

        self.motorLimits = data

    def fileDialog(self):
        # Open filedialog
        fTyp = [("", "*.json")]
        iDir = os.path.abspath(os.path.dirname(__file__))
        file_name = tk.filedialog.askopenfilename(filetypes=fTyp, initialdir=iDir)
        if len(file_name) == 0:
            self.selectedFile.set("Not selected")
        else:
            self.selectedFile.set(file_name)

    def changeMode(self):
        # change mode and show it
        self.mode.set(self.combobox_mode.current())
        self.label_mode["text"] = "Mode: " + str(self.mode.get())

    def moveForward(self):
        # Move Forward
        self.timeMin.set(self.timeMin.get() + self.timeSpan)
        self.timeMax.set(self.timeMax.get() + self.timeSpan)
        self.scale_time["from_"] = self.timeMin.get()
        self.scale_time["to_"] = self.timeMax.get()

    def moveBackward(self):
        # Move Backward
        self.timeMin.set(self.timeMin.get() - self.timeSpan)
        self.timeMax.set(self.timeMax.get() - self.timeSpan)
        self.scale_time["from_"] = self.timeMin.get()
        self.scale_time["to_"] = self.timeMax.get()

    def loadMotionFile(self):
        # Load Selected File
        file = open(self.selectedFile.get(), "r")
        data = json.load(file)
        
        # load Timestamps
        timestamps = [entry["timestamp"] for entry in data]
        len_timestamps = len(timestamps)
        self.timeEndMotion.set(int(timestamps[len_timestamps-1]))

        #load ID&Angles
        self.motionFile = data

    def saveMotionFile(self, timestamp, angles):
        # save motion file
        # overwrite data
        is_updated = False
        for entry in self.motionFile:
            if entry["timestamp"] == timestamp:
                entry["angles"] = angles
                is_updated = True
                break

        if not is_updated:
            new_entry = {
                "timestamp": timestamp,
                "angles": angles
            }
            self.motionFile.append(new_entry)

        with open(self.selectedFile.get(), "w", encoding="utf-8") as f:
            json.dump(self.motionFile, f, indent=2)

    def playMotion(self):
        # set Play Flag True
        self.is_playing = True
        #self.updateTimestamp()

    def stopMotion(self):
        # set Play Flag False
        self.is_playing = False

    def operateSend(self):
        # Send Id&Angle as topic
        print("send")
        now = self.timestamp.get()
        found_entry = None

        if self.motionFile is None:
            return
        
        # search entry mach current_time
        for entry in self.motionFile:
            if now == entry["timestamp"]:
                found_entry = entry
                break

        if found_entry:
            angles = found_entry.get("angles", {})
            # set angles if its exist 
            for motor_id in self.motorLimits:
                if motor_id in angles:
                    angle = angles[motor_id]
                    self.positions[motor_id].set(angle)
                    self.state_checkBox[motor_id].set(True)
                else:
                    self.state_checkBox[motor_id].set(False)
        else:
            # set False to others
            for motor_id in self.motorLimits:
                self.state_checkBox[motor_id].set(False)


    def operateWrite(self):
        # Write ID angle to JSON file
        print("Write")
        for now in range(self.timeEndMotion.get()):
            found_entry = None

            if self.motionFile is None:
                return

            # search entry mach current_time
            for entry in self.motionFile:
                if now == entry["timestamp"]:
                    found_entry = entry
                    break

            if found_entry:
                angles = found_entry.get("angles", {})
                # set angles if its exist
                for motor_id in self.motorLimits:
                    if motor_id in angles:
                        angle = angles[motor_id]
                        self.positions[motor_id].set(angle)
                        self.state_checkBox[motor_id].set(True)
                    else:
                        self.state_checkBox[motor_id].set(False)
                self.saveMotionFile(now, angles)

        self.mode.set(0)
        tk.messagebox.showerror("Write Mode", "motion file has benn saved")
        print("Saved")

    def operateEdit(self):
        print("Edit")
        now = self.timestamp.get()

        if self.last_timestamp.get() != now:
            found_entry = None

            if self.motionFile is None:
                return

            # search entry mach current_time
            for entry in self.motionFile:
                if now == entry["timestamp"]:
                    found_entry = entry
                    break

            if found_entry:
                angles = found_entry.get("angles", {})
                # set angles if its exist
                for motor_id in self.motorLimits:
                    if motor_id in angles:
                        angle = angles[motor_id]
                        self.positions[motor_id].set(angle)
                        self.state_checkBox[motor_id].set(True)
                    else:
                        self.state_checkBox[motor_id].set(False)
            else:
                # set False to others
                for motor_id in self.motorLimits:
                    self.state_checkBox[motor_id].set(False)
            
        found_entry = None
        # break if motionFile is NOT selected
        if self.motionFile is None:
            return
    
        # search tiestamp
        for entry in self.motionFile:
            if now == entry["timestamp"]:
                found_entry = entry
                break

        # create time stamp
        if found_entry is None:
            found_entry = {
                "timestamp": now,
                "angles": {}
            }    
            self.motionFile.append(found_entry)

        # GUI
        angles = found_entry.get("angles", {})

        for motor_id in self.motorLimits:
            if self.state_checkBox[motor_id].get():
                # update checked ID
                angles[motor_id] = self.positions[motor_id].get()
            else:
                # delete unchecked ID
                if motor_id in angles:
                    del angles[motor_id]

    def main(self):
        print("main")
        if self.is_playing:
            now = time.time()
            print(now)
            print(self.last_updated_time)
            if now - self.last_updated_time >= 1:
                new_time = self.timestamp.get() + 1
                self.last_timestamp.set(self.timestamp.get())
                self.timestamp.set(new_time)
                self.last_updated_time = now

                if new_time > self.timeMax.get() and new_time < self.timeEndMotion.get():
                    self.moveForward()

        for id in self.positions:
            print(id)
            print(self.positions[id].get())

        if self.mode.get() == 0:
            self.operateSend()
        elif self.mode.get() == 1:
            self.operateWrite()
        elif self.mode.get() == 2:
            self.operateEdit()


        self.root.after(100, self.main)

    def start(self):
        print("start")
    
if __name__ == "__main__":
    editor = MotionEditor()
    editor.start()

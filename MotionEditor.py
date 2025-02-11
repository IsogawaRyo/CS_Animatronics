import sys
import os
import tkinter as tk
import tkinter.filedialog
import tkinter.ttk as ttk
import json

class MotionEditor:
    def __init__(self):
        # Main Loop
        self.root = tk.Tk()
        self.root.title("Motion Editor")
        self.root.geometry("1000x600")

        # Start Time of Motion
        self.timeStartMotion = tk.IntVar(self.root)

        # End Time of Motion
        self.timeEndMotion = tk.IntVar(self.root)

        # Time at Edit Point
        self.timestamp = tk.IntVar(self.root)
       
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


        #### Prepare Frames ####
        # Settings Frame
        self.frame_settings = tk.LabelFrame(self.root, text="Settings", foreground="green")
        self.frame_settings.grid(sticky="W", row=0, column=0)
 
        # Monitor Frame 
        self.frame_monitor = tk.LabelFrame(self.root, text="Monitor", foreground="green")
        self.frame_monitor.grid(sticky="W", row=1, column=0)        

        # Operations Frame
        self.frame_operations = tk.LabelFrame(self.root, text="Operations", foreground="green")
        self.frame_operations.grid(sticky="W", row=3, column=0)
   
 
        #### Setting Frame ####
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
        self.combobox_mode = ttk.Combobox(self.frame_settings, state="readonly", values=("Read", "Read & Write", "Edit"))
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


        #### Monitor Frame ####
        # loop to make elements for each ID
        self.labels_ID = {}
        self.scales_angle = {}
        self.positions = {}
        for i, id in enumerate(self.motorLimits):
            # ID Label
            self.labels_ID[id] = tk.Label(self.frame_monitor, text="ID: " + id)
            self.labels_ID[id].grid(row=i, column=0)
        
            # Angle Slider
            min = self.motorLimits[id]["min"]
            max = self.motorLimits[id]["max"]
            self.positions[id] = tk.IntVar(self.root)
            self.scales_angle[id] = tk.Scale(self.frame_monitor, from_=min, to_=max, variable=self.positions[id], orient=tk.HORIZONTAL)
            self.scales_angle[id].grid(row=i, column=1)


        #### Operations Frame ####
        # Go Back Button
        self.button_goBack = tk.Button(self.frame_operations, text="<", command=self.moveBackward)
        self.button_goBack.grid(row=0, column=0)

        # Go Forward Button
        self.button_goForward = tk.Button(self.frame_operations, text=">", command=self.moveForward)
        self.button_goForward.grid(row=0, column=2)

        # Play Button
        self.button_play = tk.Button(self.frame_operations, text="play")
        self.button_play.grid(row=1, column=1)

        # Stop Button
        self.button_stop = tk.Button(self.frame_operations, text="stop")
        self.button_stop.grid(row=1, column=0)

        # Minimum Time
        self.label_minimumTime = tk.Label(self.frame_operations, textvariable=self.timeMin)
        self.label_minimumTime.grid(row=0, column=1)

        # Time seacker
        self.scale_time = tk.Scale(self.frame_operations, from_=self.timeMin.get(), to_=self.timeMax.get(), variable=self.timestamp, orient=tk.HORIZONTAL, label="time(s)", length=800)
        self.scale_time.grid(row=0, column=3, rowspan=2)


        self.root.after(10, self.main)
        self.root.mainloop()
        
    def loadMotorLimits(self):
        # load motor limits
        with open("./Motor_Limits.json", "r", encoding="utf-8") as file:
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
            self.selectedFile = "Not selected"
        else:
            self.selectedFile.set(file_name)
        self.label_selectedFile["text"] = self.selectedFile

    def changeMode(self):
        # change mode and show it
        self.mode = self.combobox_mode.current()
        self.label_mode["text"] = "Mode: " + str(self.mode)

    def moveForward(self):
        self.timeMin.set(self.timeMin.get() + self.timeSpan)
        self.timeMax.set(self.timeMax.get() + self.timeSpan)
        self.scale_time["from_"] = self.timeMin.get()
        self.scale_time["to_"] = self.timeMax.get()

    def moveBackward(self):
        self.timeMin.set(self.timeMin.get() - self.timeSpan)
        self.timeMax.set(self.timeMax.get() - self.timeSpan)
        self.scale_time["from_"] = self.timeMin.get()
        self.scale_time["to_"] = self.timeMax.get()

    def loadMotionFile(self):
        # Load Selected File
        file = open(self.selectedFile.get(), "r")
        data = json.load(file)
        
        # load Timestamops
        timestamps = [entry["timestamp"] for entry in data]
        len_timestamps = len(timestamps)
        self.timeEndMotion.set(int(timestamps[len_timestamps-1]))

        #load ID&Angles
        

    def operateRead(self):
        print("read")

    def operateReadandWrite(self):
        print("Read&Write")

    def operateEdit(self):
        print("Edit")

    def main(self):
        print("main")

        for id in self.positions:
            print(id)
            print(self.positions[id].get())

        if self.mode == 0:
            self.operateRead()
        elif self.mode == 1:
            self.operateReadandWrite()
        elif self.mode == 2:
            self.operateEdit()


        self.root.after(10, self.main)

    def start(self):
        print("start")
    
if __name__ == "__main__":
    editor = MotionEditor()
    editor.start()

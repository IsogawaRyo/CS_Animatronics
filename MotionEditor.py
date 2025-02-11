import sys
import os
import tkinter as tk
import tkinter.filedialog
import tkinter.ttk
import json

class MotionEditor:
    def __init__(self):
        # Time at Edit Point
        self.timestamp = 0
        
        # Mode
        # 0: Read
        # 1: Read & Write
        # 2: Edit
        self.mode = 0
        
        # Load Motor Limits
        self.motorLimits = {}
        self.loadMotorLimits()
        for id in self.motorLimits:
            print(id)

        # Selected File to Edit
        self.selectedFile = "Not Selected"


        # Main Loop
        root = tk.Tk()
        root.title("Motion Editor")
        root.geometry("1000x1600")
       
        # Settings Frame
        self.frame_settings = tk.Frame(root)
        
        # Monitor Frame 
        self.frame_monitor = tk.Frame(root)
        
        # Operations Frame
        self.frame_operations = tk.Frame(root)
    
        ## Setting Frame
        # Seleced File Label
        self.label_selectedFile = tk.Label(self.frame_settings, text=self.selectedFile)
        self.label_selectedFile.grid(row=0, column=0)
        
        # Selected File Button
        self.button_selectedFile = tk.Button(self.frame_settings, text="Open filedialog", command=self.fileDialog, width=24, height=1)
        self.button_selectedFile.grid(row=0, column=1)
        
        # Mode Label
        self.label_mode = tk.Label(self.frame_settings, text="Current Mode")
        self.label_mode.grid(row=0, column=2)
        
        # Mode Dropbox
        self.combobox_mode = ttk.Combobox(self.frame_settings, state="readonly", values=("Read", "Read & Write", "Mode"))
        self.combobox_mode.grid(row=0, column=3)
        
        # Mode Chose Button
        self.button_mode = tk.Button(self.frame_settings, text="Change Mode", command=self.changeMode)
        self.button_mode.grid(row=0, column=4)

        ## Monitor Frame
        # loop to make elements for each ID
        self.labels_ID = {}
        self.scales_angle = {}
        for i, id in enumerate(self.motorLimits):
            # ID Label
            self.label_ID[id] = tk.Label(self.frame_monitor, text={id})
            self.label_ID[id].grid(row=i, colmun=0)
        
            # Angle Slider
            min = self.motorLimits[id]["min"]
            max = self.motorLimits[id]["max"]
            self.scale_angle[id] = tk.Scale(self.frame_monitor, from_=min, to_=max, orient=tk.HORIZONTAL, label='Angle')
            self.scale_angle[id].grid(row=i, colmun=1)

        ## Operations Frame


        self.frame_settings.grid(row=0, column=0)
        self.frame_monitor.grid(row=1, column=0)
        self.frame_operations.grid(row=3, column=0)
        root.mainloop()
        
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
            self.selectedFile = file_name
        self.label_selectedFile["text"] = self.selectedFile

    def changeMode(self):
        # change mode and show it
        self.mode = self.combobox_mode.current()
        self.label_mode["text"] = "Mode: " + self.mode

    def main(self):
        print("main")
        while True:
            if self.mode == 0:
                print(mode)
            elif self.mode == 1:
                print(mode)
            elif self.mode == 2:
                print(mode)
    
if __name__ == "__main__":
    editor = MotionEditor()
    editor.main()

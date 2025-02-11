import sys
import os
import tkinter as tk
import tkinter.filedialog
import json

class MotionEditor:
    def __init__(self):
        # Time at Edit Point
        self.timestamp = 0
        
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
    
    
        # Seleced File Label
        self.label_selectedFile = tk.Label(self.frame_settings, text=self.selectedFile)
        self.label_selectedFile.grid(row=0, column=0)
        
        # Selected File Button
        self.button_selectedFile = tk.Button(self.frame_settings, text="Open filedialog", command=self.fileDialog, width=24, height=1)
        self.button_selectedFile.grid(row=0, colmun=0)

        # loop to make elements for each ID
        for id in self.motorLimits:
            # ID Label
            command = f"self.label_ID_{id} = tk.Label(root, text={id})"
            exec(command)
            command = f"self.label_ID_{id}.pack(pady=0)"
            exec(command)
            
            # Angle Slider
            min = self.motorLimits[id]["min"]
            max = self.motorLimits[id]["max"]
            command = f"self.scale_angle_{id} = tk.Scale(root, from_=min, to_=max, orient=tk.HORIZONTAL, label='Angle')"
            exec(command)
            command = f"self.scale_angle_{id}.pack(pady=0)"
            exec(command)


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

    def main(self):
        print("main")

if __name__ == "__main__":
    editor = MotionEditor()
    editor.main()

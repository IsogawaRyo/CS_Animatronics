import sys
import os
import tkinter as tk
import tkinter.filedialog
import json

class MotionEditor:
    def __init__(self):
        # time at edit point
        self.timestamp = 0
        
        # load motor limits
        self.motorLimits = {}
        self.loadMotorLimits()
        for id in self.motorLimits:
            print(id)

        # selected file to edit
        self.selectedFile = "Not Selected"


        # main loop
        root = tk.Tk()
        root.title("Motion Editor")
        root.geometry("800x400")
       
        # seleced file label
        self.label_selectedFile = tk.Label(root, text=self.selectedFile)
        self.label_selectedFile.pack(pady=10)
        
        # selected file button
        self.button_selectedFile = tk.Button(root, text="Open filedialog", command=self.fileDialog, width=24, height=1)
        self.button_selectedFile.pack(pady=0)

        # ID labels
        self.labels_ID = {}
        for id in self.motorLimits:
            dict = {}
            dict["label"] = tk.Label(root, text=f"{id}")
            

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

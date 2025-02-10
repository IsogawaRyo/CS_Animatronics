import sys
import os
import tkinter as tk
import tkinter.filedialog
import json

class MotionEditor:
    def __init__(self):
        # time at edit point
        self.timestamp = 0
        
        # selected file to edit
        self.selectedFile = "Not Selected"


        # main loop
        root = tk.Tk()
        root.title("Motion Editor")
        root.geometry("800x400")

        label_selectedFile = tk.Label(self.selectedFile)
        label_selectedFile.pack(pady=10)
        
        button_selectedFile = tk.Button(root, text="Open filedialog", width=24, height=1)
        button_selectedFile.bind("<ButtonPress>", self.fileDialog())
        button_selectedFile.pack(pady=0)

        root.mainloop()
        
    def loadMotorLimits(self):
        # load motor limits
        with open("/home/csanimatronics/CS_Animatronics/Motor_Limits.json", "r", encoding="utf-8") as file:
            data = json.load(file)
            
        for key, subdict in data.items():
            subdict["ini"] = int(subdict["ini"])
            subdict["min"] = int(subdict["min"])
            subdict["max"] = int(subdict["max"])
            subdict["acc"] = int(subdict["acc"])
            subdict["vel"] = int(subdict["vel"])

        motorLimits = data

    def fileDialog(self):
        # Open filedialog
        fTyp = [("", "*.json")]
        iDir = os.path.abspath(os.path.dirname(__file__))
        file_name = tk.filedialog.askopenfilename(filetypes=fTyp, initialdir=iDir)
        if len(file_name) == 0:
            self.selectedFile = "Not selected"
        else:
            self.selectedFilee = file_name

    def main(self):
        print("main")

if __name__ == "__main__":
    editor = MotionEditor()
    editor.main()x

import sys
import Tkinter
import json

class MotionEditor:
    def __init__(self):
        # time at edit point
        self.timestamp = 0
        
        root = Tkinter.Tk()
        root.title("Motion Editor")
        root.geometry("1200x400")
        
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
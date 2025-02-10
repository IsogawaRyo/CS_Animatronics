import sys
import Tkinter
import json

# time at edit point
timeStamp = 0

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

# main loop
root = Tkinter.Tk()



root.mainloop()
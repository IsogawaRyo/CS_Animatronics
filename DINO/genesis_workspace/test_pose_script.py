import genesis as gs
import torch
import math

def test():
    gs.init(backend=gs.cpu)
    scene = gs.Scene(show_viewer=False)
    # The user says it starts tilted 90 deg left. If so, a rotation around X or Y is needed.
    
    q1 = gs.utils.geom.xyz_to_quat(torch.tensor([math.pi/2, 0, 0])) # 90 deg around X
    q2 = gs.utils.geom.xyz_to_quat(torch.tensor([0, math.pi/2, 0])) # 90 deg around Y
    print("90 deg around X:", q1)
    print("90 deg around Y:", q2)

test()

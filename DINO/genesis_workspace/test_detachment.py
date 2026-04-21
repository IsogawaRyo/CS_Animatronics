import genesis as gs
import torch
import numpy as np
import os

def test():
    gs.init(backend=gs.cpu)
    scene = gs.Scene(
        show_viewer=False,
        rigid_options=gs.options.RigidOptions(enable_self_collision=False)
    )
    scene.add_entity(gs.morphs.Plane())

    urdf_path = "../animatronics_urdf_description/animatronics_urdf_description_standalone.urdf"

    robot = scene.add_entity(
        gs.morphs.URDF(
            file=urdf_path,
            pos=(0, 0, 0.35),
            quat=(0.7071, 0.7071, 0.0, 0.0),
            merge_fixed_links=True,
            is_free=True,
        ),
    )
    
    # Try multiple envs
    scene.build(n_envs=5)

    continuous_joints = [
        "Revolute 10", "Revolute 12", "Revolute 13", "Revolute 16", "Revolute 17",
        "Revolute 20", "Revolute 22", "Revolute 23", "Revolute 26", "Revolute 27",
        "Revolute 37", "Revolute 42", "Revolute 43", "Revolute 44"
    ]
    dofs_idx = [robot.get_joint(name).dof_start for name in continuous_joints]
    
    # Apply PD
    robot.set_dofs_kp(np.full(len(dofs_idx), 15.0), dofs_idx)
    robot.set_dofs_kv(np.full(len(dofs_idx), 1.0), dofs_idx)

    # Set pd target
    target_pos = torch.zeros((5, len(dofs_idx)), device=gs.device)
    robot.control_dofs_position(target_pos, dofs_idx)

    print("Running 100 steps...")
    for i in range(100):
        scene.step()
        pos = robot.get_pos()
        if torch.isnan(pos).any() or torch.max(torch.abs(pos)) > 10:
            print(f"Physics exploded at step {i}!")
            return
            
    print("Physics OK. Final Pos:", robot.get_pos())

test()

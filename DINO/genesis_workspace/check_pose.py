import genesis as gs
import torch
import time
import os

def main():
    gs.init(backend=gs.cuda)

    scene = gs.Scene(show_viewer=True)
    scene.add_entity(gs.morphs.Plane())

    script_dir = os.path.dirname(os.path.abspath(__file__))
    urdf_path = os.path.join(script_dir, "../animatronics_urdf_description/animatronics_urdf_description_standalone.urdf")

    robot = scene.add_entity(
        gs.morphs.URDF(
            file=urdf_path,
            pos=(0, 0, 0.42), # Initial height
            merge_fixed_links=True,
        ),
    )

    scene.build()

    # Set all joints to 0
    dofs_idx = [robot.get_joint(name).dof_start for name in [
        "Revolute_3", "Revolute_4", "Revolute_10", "Revolute_11", "Revolute_14", "Revolute_15",
        "Revolute_18", "Revolute_19", "Revolute_22", "Revolute_23", "Revolute_36", "Revolute_37",
        "Revolute_40", "Revolute_42", "Revolute_44", "Revolute_46", "Revolute_47", "Revolute_50"
    ]]
    
    robot.set_dofs_position(torch.zeros(18, device=gs.device), dofs_idx)

    print("Visualizing default pose (all zeros)...")
    while True:
        scene.step()
        time.sleep(0.1)

if __name__ == "__main__":
    main()

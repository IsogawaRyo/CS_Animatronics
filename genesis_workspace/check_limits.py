import genesis as gs
import os

def main():
    gs.init(backend=gs.cpu)

    scene = gs.Scene(show_viewer=False)
    scene.add_entity(gs.morphs.Plane())

    script_dir = os.path.dirname(os.path.abspath(__file__))
    urdf_path = os.path.join(script_dir, "../animatronics_urdf_description/animatronics_urdf_description_standalone.urdf")

    robot = scene.add_entity(
        gs.morphs.URDF(
            file=urdf_path,
            pos=(0, 0, 0.42),
        ),
    )

    scene.build()

    joint_names = [
        "Revolute_3", "Revolute_4", "Revolute_10", "Revolute_11", "Revolute_14", "Revolute_15",
        "Revolute_18", "Revolute_19", "Revolute_22", "Revolute_23", "Revolute_36", "Revolute_37",
        "Revolute_40", "Revolute_42", "Revolute_44", "Revolute_46", "Revolute_47", "Revolute_50"
    ]

    print("Joint Limits:")
    for name in joint_names:
        joint = robot.get_joint(name)
        # Check available attributes
        # Usually limits are in dof_limit or similar
        # Let's try to find it
        if hasattr(joint, 'limit'):
             print(f"{name}: {joint.limit}")
        elif hasattr(joint, 'dof_limit'):
             print(f"{name}: {joint.dof_limit}")
        else:
             print(f"{name}: Could not find limit attribute. Dir: {dir(joint)}")
             
        # Also check if we can get it from the entity
        dof_idx = joint.dof_start
        # Maybe robot.get_dofs_limit(dof_idx)?
        
    # Try getting all limits from robot
    try:
        limits = robot.get_dofs_limit()
        print(f"\nAll DOFs limits shape: {limits[0].shape}, {limits[1].shape}")
        # Print for our joints
        for name in joint_names:
            dof_idx = robot.get_joint(name).dof_start
            lower = limits[0][dof_idx].item()
            upper = limits[1][dof_idx].item()
            print(f"{name}: [{lower:.4f}, {upper:.4f}]")
            
    except Exception as e:
        print(f"Error getting dofs limit: {e}")

if __name__ == "__main__":
    main()

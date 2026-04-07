import genesis as gs
import os

# Path to the URDF file
script_dir = os.path.dirname(os.path.abspath(__file__))
urdf_path = os.path.join(script_dir, "../animatronics_urdf_description/animatronics_urdf_description_standalone.urdf")

# Check if file exists
if not os.path.exists(urdf_path):
    print(f"Error: URDF file not found at {urdf_path}")
    exit(1)

gs.init(backend=gs.cuda)

scene = gs.Scene(show_viewer=True)
plane = scene.add_entity(gs.morphs.Plane())
robot = scene.add_entity(
    gs.morphs.URDF(file=urdf_path),
)

scene.build()

while True:
    scene.step()

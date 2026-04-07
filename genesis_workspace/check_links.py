import genesis as gs
import os

gs.init(backend=gs.cuda)

scene = gs.Scene(show_viewer=False)
plane = scene.add_entity(gs.morphs.Plane())

script_dir = os.path.dirname(os.path.abspath(__file__))
urdf_path = os.path.join(script_dir, "../animatronics_urdf_description/animatronics_urdf_description_standalone.urdf")

robot = scene.add_entity(
    gs.morphs.URDF(file=urdf_path),
)

scene.build()

print("Link names:")
for link in robot.links:
    print(link.name)

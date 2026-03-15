import genesis as gs
import os

def list_links():
    gs.init(backend=gs.cpu)
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    urdf_path = os.path.join(script_dir, "../animatronics_urdf_description/animatronics_urdf_description_standalone.urdf")
    
    scene = gs.Scene(show_viewer=False)
    robot = scene.add_entity(gs.morphs.URDF(file=urdf_path))
    scene.build()
    
    print("--- Available Link Names ---")
    for link in robot.links:
        print(link.name)

if __name__ == "__main__":
    list_links()

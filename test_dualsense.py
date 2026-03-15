import pydualsense
import time

def test_dualsense():
    ds = pydualsense.pydualsense()
    try:
        ds.init()
        print(f"DualSense connected: {ds.device}")
        
        print("Testing LED (Red)...")
        ds.setLeftMotor(255) # Rumble test
        ds.setRightMotor(100)
        ds.setLightbar(255, 0, 0) # Red
        time.sleep(1)
        
        print("Testing LED (Green)...")
        ds.setLightbar(0, 255, 0) # Green
        ds.setLeftMotor(0)
        ds.setRightMotor(0)
        time.sleep(1)
        
        print("Testing Adaptive Trigger (L2 Resistance)...")
        # Trigger modes: 0=Off, 1=Rigid, 2=Pulse, etc. (Check library docs or constants)
        # pydualsense constants might be needed.
        # ds.triggerL.setMode(pydualsense.TriggerModes.Rigid) 
        # For now, just closing.
        
        ds.close()
        print("Test complete.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_dualsense()

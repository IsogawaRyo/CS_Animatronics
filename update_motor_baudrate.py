#!/usr/bin/env python3
import time
import sys
try:
    from dynamixel_sdk import *
except ImportError:
    print("Error: dynamixel_sdk not found. Please install it first.")
    sys.exit(1)

# Protocol version
PROTOCOL_VERSION            = 2.0

# Control table address
ADDR_TORQUE_ENABLE          = 64
ADDR_BAUD_RATE              = 8

# Baud rate values
BAUD_57600                  = 1
BAUD_115200                 = 2

def change_baudrate():
    # Setup ports
    ports = ["/dev/ttyUSB0", "/dev/ttyUSB1"]
    
    print("--- Dynamixel Baud Rate Update Tool (57600 -> 115200) ---")
    
    any_updated = False
    for device_name in ports:
        port_handler = PortHandler(device_name)
        packet_handler = PacketHandler(PROTOCOL_VERSION)
        
        try:
            if not port_handler.openPort():
                print(f"Skipping {device_name}: Could not open port.")
                continue
                
            if not port_handler.setBaudRate(57600):
                print(f"Skipping {device_name}: Could not set baudrate to 57600.")
                port_handler.closePort()
                continue
                
            print(f"\nScanning {device_name} at 57600...")
            found_ids = []
            for dxl_id in range(1, 40): # Scanning a smaller range for speed, adjust if needed
                _, comm_result, _ = packet_handler.ping(port_handler, dxl_id)
                if comm_result == COMM_SUCCESS:
                    found_ids.append(dxl_id)
            
            if not found_ids:
                print(f"No motors found on {device_name} at 57600.")
                # Check 115200 just in case
                port_handler.setBaudRate(115200)
                for dxl_id in range(1, 40):
                    _, comm_result, _ = packet_handler.ping(port_handler, dxl_id)
                    if comm_result == COMM_SUCCESS:
                        found_ids.append(dxl_id)
                if found_ids:
                    print(f"Motors {found_ids} are already at 115200 on {device_name}.")
                port_handler.closePort()
                continue

            print(f"Found motors: {found_ids}")
            
            for dxl_id in found_ids:
                print(f"Attempting to update motor {dxl_id} to 115200...")
                # Disable torque (baud rate cannot be changed while torque is on)
                packet_handler.write1ByteTxRx(port_handler, dxl_id, ADDR_TORQUE_ENABLE, 0)
                time.sleep(0.1)
                
                # Change baud rate
                dxl_comm_result, dxl_error = packet_handler.write1ByteTxRx(port_handler, dxl_id, ADDR_BAUD_RATE, BAUD_115200)
                if dxl_comm_result != COMM_SUCCESS:
                    print(f"  [Error] Failed to change baudrate for {dxl_id}: {packet_handler.getTxRxResult(dxl_comm_result)}")
                elif dxl_error != 0:
                    print(f"  [Error] Motor error for {dxl_id}: {packet_handler.getRxPacketError(dxl_error)}")
                else:
                    print(f"  [Success] Motor {dxl_id} updated.")
                    any_updated = True
            
            port_handler.closePort()
        except Exception as e:
            print(f"An error occurred on {device_name}: {e}")
        
    if any_updated:
        print("\nUpdate process complete.")
        print("IMPORTANT: You may need to power cycle the motors for the changes to take effect.")
    else:
        print("\nNo motors were updated.")

if __name__ == "__main__":
    change_baudrate()

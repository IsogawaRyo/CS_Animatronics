#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from motor_commands.srv import GetMotorStates

class MotorStateTester(Node):
    def __init__(self):
        super().__init__('motor_state_tester')
        
        self.client = self.create_client(GetMotorStates, 'get_motor_states')
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Service not available, waiting...')
    
    def test_motor_states(self):
        request = GetMotorStates.Request()
        request.ids = [11, 12, 13, 21, 22, 23, 24, 31, 32, 33, 34]
        
        self.get_logger().info(f'Requesting states for motors: {request.ids}')
        
        future = self.client.call_async(request)
        rclpy.spin_until_future_complete(self, future)
        
        if future.result() is not None:
            response = future.result()
            self.get_logger().info(f'Response received:')
            self.get_logger().info(f'  IDs: {response.ids}')
            self.get_logger().info(f'  Positions: {response.positions}')
            self.get_logger().info(f'  Temperatures: {response.temperatures}')
            self.get_logger().info(f'  Torques: {response.torques}')
            
            # Check for valid data
            for i, motor_id in enumerate(response.ids):
                pos = response.positions[i]
                temp = response.temperatures[i] 
                torque = response.torques[i]
                
                print(f'Motor {motor_id}:')
                print(f'  Position: {pos} (0-4095 range)')
                print(f'  Temperature: {temp}°C (expected: 20-80°C)')
                print(f'  Torque: {torque} (load value)')
                print()
                
                # Flag potential issues
                if temp == 25 and torque == 0:
                    print(f'  ⚠️  Motor {motor_id}: Using default values (temp=25, torque=0)')
                elif temp < 15 or temp > 100:
                    print(f'  ⚠️  Motor {motor_id}: Temperature out of normal range')
                elif torque == 0:
                    print(f'  ℹ️  Motor {motor_id}: Zero torque (idle or cached value)')
                elif torque > 0:
                    print(f'  ✅ Motor {motor_id}: Active torque detected')
                    
                # Additional validation
                if pos < 0 or pos > 4095:
                    print(f'  ⚠️  Motor {motor_id}: Position out of range (0-4095)')
                if isinstance(torque, (int, float)) and torque > 10000:
                    print(f'  ⚠️  Motor {motor_id}: Suspiciously high torque value')
                    
        else:
            self.get_logger().error('Service call failed')

def main(args=None):
    rclpy.init(args=args)
    
    tester = MotorStateTester()
    
    try:
        tester.test_motor_states()
    except KeyboardInterrupt:
        pass
    
    tester.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Joy
from system_controller.msg import IdAngle

class SystemController(Node):
    def __init__(self):
        super().__init__('system_controller')

        # Setting for subscriber
        self.subscription = self.create_subscription(
            Joy,
            'controller_input',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

        # Setting for publisher
        self.publisher = self.create_publisher(
            IdAngle,
            'output_topic',
            10
        )

    def listener_callback(self, msg):
        # Log the axes and buttons states received from the controller
        self.get_logger().info(f'Axes: {msg.axes}')
        self.get_logger().info(f'Buttons: {msg.buttons}')
       
        ids, angles = self.translate(msg.data)
 
        new_msg = IdAngl()
        new_msg.ids = ids
        new_msg.angles = angles

        self.publisher.publish(new_msg)
        self.get_logger().info(f'Publishing IDs: {new_msg.ids}, Angles: {new_msg.angles}')

    def translete(self, data):
        ids = [11, 21]
        angles = [100, 100]

        return id, angle

def main(args=None):
    rclpy.init(args=args)
    node = SystemController()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()


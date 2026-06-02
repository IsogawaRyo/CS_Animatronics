#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import threading

class VisionReceiverNode(Node):
    def __init__(self):
        super().__init__('vision_receiver_node')
        
        self.bridge = CvBridge()
        
        # Publishers
        self.left_pub = self.create_publisher(Image, '/camera/left/image_raw', 10)
        self.right_pub = self.create_publisher(Image, '/camera/right/image_raw', 10)

        # Connection strings (TCP/MJPEG stream from Pi Zeros)
        # Note: Depending on the libcamera-vid config, it might be TCP or UDP.
        # This setup assumes MJPEG over TCP, which OpenCV handles natively via http/tcp stream.
        # Format: "tcp://<IP>:<PORT>" or "http://<IP>:<PORT>/" if using mjpg-streamer
        self.left_stream_url = "tcp://10.55.0.2:5000"
        self.right_stream_url = "tcp://10.55.1.2:5001"

        # Start reception threads
        self.left_thread = threading.Thread(target=self.receive_stream, args=(self.left_stream_url, self.left_pub, "LEFT"))
        self.right_thread = threading.Thread(target=self.receive_stream, args=(self.right_stream_url, self.right_pub, "RIGHT"))
        
        self.left_thread.daemon = True
        self.right_thread.daemon = True
        
        self.left_thread.start()
        self.right_thread.start()
        
        self.get_logger().info('Vision Receiver Node initialized. Listening for stereo streams.')

    def receive_stream(self, stream_url, publisher, name):
        """Thread function to continuously read from a video stream and publish ROS Image messages"""
        self.get_logger().info(f'Attempting to connect to {name} camera at {stream_url} ...')
        
        # Open video capture
        # Optimization: use cv2.CAP_FFMPEG backend explicitly for tcp/udp streams
        cap = cv2.VideoCapture(stream_url, cv2.CAP_FFMPEG)
        
        # Lower buffer size for lower latency if possible (backend dependent)
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

        if not cap.isOpened():
            self.get_logger().error(f'Failed to open {name} stream at {stream_url}. Retrying later...')
            return

        self.get_logger().info(f'Successfully connected to {name} camera.')

        while rclpy.ok() and cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                self.get_logger().warning(f'{name} camera stream interrupted. Retrying...')
                # Implement basic reconnect logic
                cap.release()
                rclpy.sleep(2)
                cap = cv2.VideoCapture(stream_url, cv2.CAP_FFMPEG)
                continue

            try:
                # Convert OpenCV Image (BGR) to ROS Image message
                msg = self.bridge.cv2_to_imgmsg(frame, encoding="bgr8")
                msg.header.stamp = self.get_clock().now().to_msg()
                msg.header.frame_id = f"camera_{name.lower()}_link"
                publisher.publish(msg)
            except Exception as e:
                self.get_logger().error(f'Error publishing {name} image: {str(e)}')

        cap.release()
        self.get_logger().info(f'{name} camera receiving thread stopped.')


def main(args=None):
    rclpy.init(args=args)
    node = VisionReceiverNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()

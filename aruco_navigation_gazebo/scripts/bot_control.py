#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from custom_message.msg import ArucoVals
from geometry_msgs.msg import Twist

class ArucoNavigator(Node):
    def __init__(self):
        super().__init__('aruco_navigator')
        # Create a subscription to the ArucoVals topic
        self.subscription = self.create_subscription(
            ArucoVals,
            'aruco_data',
            self.aruco_callback,
            10
        )
        self.publisher_ = self.create_publisher(Twist, 'cmd_vel', 10)
        self.current_marker = None

    def aruco_callback(self, msg):
        self.current_marker = msg
        self.navigate_to_marker()

    def navigate_to_marker(self):
        if self.current_marker:
            # Calculate the control commands based on the marker's position
            twist = Twist()

            # Example: Move towards the marker
            if self.current_marker.x < 450:
                twist.linear.x = 0.1
                twist.angular.z = 0.1
            elif self.current_marker.x > 550:
                twist.linear.x = 0.1
                twist.angular.z = -0.1
            else:
                twist.linear.x = 0.2

            # Example: Stop if the marker is close enough
            if self.current_marker.radius > 100:
                twist.linear.x = 0.0
                twist.angular.z = 0.0

            self.publisher_.publish(twist)

def main(args=None):
    rclpy.init(args=args)
    aruco_navigator = ArucoNavigator()
    rclpy.spin(aruco_navigator)
    aruco_navigator.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

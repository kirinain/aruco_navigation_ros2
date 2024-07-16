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
        # Create a publisher for the cmd_vel topic
        self.publisher_ = self.create_publisher(Twist, 'cmd_vel', 10)
        self.current_marker = None
        self.marker_close = False

    def aruco_callback(self, msg):
        # Update current_marker with the received message
        self.current_marker = msg
        # Navigate towards the detected marker
        self.navigate_to_marker()

    def navigate_to_marker(self):
        twist = Twist()
        
        if self.current_marker:
            # Check if the marker is close enough
            if self.current_marker.radius > 152:
                self.marker_close = True
                # Stop the robot
                twist.linear.x = 0.0
                twist.angular.z = 0.0
            else:
                self.marker_close = False
                # Control logic to navigate towards the marker based on its x position
                if self.current_marker.x < 450:
                    twist.linear.x = 0.3
                    twist.angular.z = 0.1
                elif self.current_marker.x > 550:
                    twist.linear.x = 0.3
                    twist.angular.z = -0.1
                else:
                    twist.linear.x = 0.4
            
            self.publisher_.publish(twist)
        
        if self.marker_close:
            # Rotate to look for another marker
            twist.linear.x = 0.0
            twist.angular.z = 0.5
            self.publisher_.publish(twist)

def main(args=None):
    rclpy.init(args=args)
    aruco_navigator = ArucoNavigator()
    rclpy.spin(aruco_navigator)
    aruco_navigator.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
import math

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry


class MR_Robot(Node):
    def __init__(self):
        super().__init__('mr_robot')
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        # self.subscriber_ = self.create_subscription(Odometry, '/odom', self.odom_callback, 10)
        self.vel_msg = Twist()
        # self.odom = Odometry()
        self.timer = self.create_timer(0.1, self.timer_callback)
        self.get_logger().info("MR_Robot has been initialized.")
        
    # def odom_callback(self, msg):
    #     self.odom = msg

    def timer_callback(self):
        self.vel_msg.linear.x = 1.0  # Move forward at 1.0 m/s
        self.publisher_.publish(self.vel_msg)
        print("b")

def main(args=None):#We don't provide any argument to the script
    rclpy.init(args=args)  
    node = MR_Robot()
    rclpy.spin(node)
    rclpy.shutdown() 
    print("c")
    exit()

if __name__ == '__main__':
    main()        

#order of python imports, it should be refined <ros commands together, other commands>.
#Include line spacing, 2 line spacing  before introducing classes.    
#!/usr/bin/env python3
import math

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from aruco_interfaces.msg import Aruco 

class Aruco_Navigation(Node):
    def __init__(self):
        super().__init__('mr_robot')

        self.subscriber_msg = self.create_subscription(Aruco, 'aruco_msg', self.aruco_callback, 10)
        self.publisher_vel = self.create_publisher(Twist, '/cmd_vel', 10)
        self.vel_msg = Twist()
        self.get_logger().info("Centre aligning has been initiated.")   
        
        self.Line_centre = 160
        self.kp = 0.02
        self.radius = 62 
        self.kr = 0.0625
        self.flag = False

    def aruco_callback(self, msg):
        """This funtion ensures that robots navigates smoothly using PID and detect every marker turn by turn."""
        aruco_centre_x = msg.centre_x
        aruco_radius = msg.radius
        aruco_id = msg.id

        if self.flag == False:
            error = self.Line_centre - aruco_centre_x
            self.get_logger().info(f"Error:{error}")

            img_radius = self.radius - aruco_radius
            self.get_logger().info(f"Image_radius:{img_radius}")

        
            self.pub_vel(self.kr*img_radius,self.kp*error)
            self.get_logger().info(f"Velocity:{self.vel_msg}")

        if aruco_id == 0 and aruco_radius == 62:
            self.pub_vel(0.0,1.5)
            self.flag = True
        elif aruco_id == 2:
            self.flag = False

        if aruco_id == 2 and aruco_radius >= 61:     
            self.pub_vel(0.0, 1.5)
            self.flag = True
        elif aruco_id == 1:
            self.flag = False
            
        if aruco_id == 1 and aruco_radius >= 61:
            self.get_logger().info("we have reached destination, have a lovely day!")    
        

    def pub_vel(self, linear, angular):   
        self.vel_msg.linear.x = linear
        self.vel_msg.angular.z = angular

        self.publisher_vel.publish(self.vel_msg)

def main(args=None):#We don't provide any argument to the script
    rclpy.init(args=args)  
    node = Aruco_Navigation()
    rclpy.spin(node)
    rclpy.shutdown() 
    exit()

if __name__ == '__main__':
    main()        

  
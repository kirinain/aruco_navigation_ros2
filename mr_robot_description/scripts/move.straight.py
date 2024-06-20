#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose

while (True):
    print ("yo")

# class MoveNode(Node):
   
#    def __init__(self):
#       super().__init__("turtle_controller")
#       self.cmd_vel_publisher = self.create_publisher(
#          Twist, "/bot/cmd_vel", 10)
#       self.pose_subscriber = self.create_subscription(
#          Pose, "/bot/pose", self.pose_callback, 10)
#       self.get_logger().info("Turtle controller has been started.")
   
#    def pose_callback(self, pose: Pose):
#       cmd = Twist()

#       if pose.x > 9.0:
#          cmd.linear.x = 0.0
#          cmd.angular.z = -5.0
           
#          if pose.theta < -2.3:
#             cmd.linear.x = 9.0
#             cmd.angular.z = 0.0
   
#          else:
#             cmd.linear.x = 0.0
#             cmd.angular.z = -0.9
   
#       else:
#          cmd.linear.x = 5.0
#          cmd.angular.z = 0.0

#       if pose.y < 5 and pose.x < 6:
#          cmd.linear.x = 0.0
#          cmd.angular.z = 0.5

#          if round(pose.theta,2) == 0.0:
#             cmd.linear.x = 9.0
#             cmd.angular.z = 0.0

#       if pose.x > 9.0 and pose.y < 5:
#          print("HOGYA BANCHO")
#          cmd.linear.x = 0.0
#          cmd.angular.z = 0.0
#          self.cmd_vel_publisher.publish(cmd)
#          exit(0)

#       self.cmd_vel_publisher.publish(cmd)
    
# def main(args=None):
#    rclpy.init(args=args)
#    node = MoveNode()
#    rclpy.spin(node)
#    MoveNode.destroy_node()
#    rclpy.shutdown()

# if __name__ == '__main__':
#     main()
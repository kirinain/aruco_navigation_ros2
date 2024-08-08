#!/usr/bin/env python3
import math
import numpy as np

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2
import cv2.aruco as aruco
from aruco_interfaces.msg import Aruco

class Detection(Node):
    def __init__(self):
        super().__init__('Aruco_detection')
        
        self.subscriber_ = self.create_subscription(Image,'/world_image', self.image_callback, 10) #world_image is the topic name I gave in bridge  file
        self.publisher_msg = self.create_publisher(Aruco,'aruco_msg',10)
        self.get_logger().info("Detection has been initialized.")
        
        self.bridge = CvBridge() #created an object self bridge and CvBridge is the class
        self.aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_250) 
        self.parameters = aruco.DetectorParameters_create()

    def image_callback(self, msg):
        self.image = msg
        cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
        i = 0

        gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY) #to convert cv2 image in grayscale for aruco to detect it
        brightness = 15 
        contrast = 2.1  
        gray = cv2.addWeighted(gray, contrast, np.zeros(gray.shape, gray.dtype), 0, brightness)
        corners, ids, RejectedImgPoints = aruco.detectMarkers(gray, self.aruco_dict, parameters=self.parameters)
        print(corners)


        if ids is not None:
            cv_image = aruco.drawDetectedMarkers(cv_image, corners, ids)
            self.get_logger().info(f"Detected Aruco markers with IDs: {ids.flatten()}")
        
    
        for corner in corners:
            # center and radius of the marker
            corner = corner.reshape((4, 2))
            (top_left, top_right, bottom_right, bottom_left) = corner
            center_x = int((top_left[0] + bottom_right[0]) / 2.0)
            center_y = int((top_left[1] + bottom_right[1]) / 2.0)
                
            # radius as half the diagonal of the bounding box
            width = math.sqrt((top_right[0] - top_left[0]) ** 2 + (top_right[1] - top_left[1]) ** 2)
            height = math.sqrt((bottom_left[0] - top_left[0]) ** 2 + (bottom_left[1] - top_left[1]) ** 2)
            radius = int(math.sqrt(width ** 2 + height ** 2) / 2.0)

            aruco_msg = Aruco()
            aruco_msg.radius = float(radius)
            aruco_msg.centre_x = float(center_x)
            aruco_msg.centre_y = float(center_y)
            aruco_msg.id = int(ids[i][0])
            self.publisher_msg.publish(aruco_msg)
            
            # sphere around the marker
            cv2.circle(cv_image, (center_x, center_y), radius, (0, 255, 0), 2)
            self.get_logger().info(f"Marker ID: {ids.flatten()[i]}, Center: ({center_x}, {center_y}), Radius: {radius}")
            i = i+1

        start_point = (160, 0)
        end_point = (160, 300)
        color = (231, 209, 255)
        thickness = 2

       
        cv_image = cv2.line(cv_image, start_point, end_point, color, thickness)
        cv2.imshow("kitty2",gray)
        cv2.imshow("kitty",cv_image) #for showing it on window
        cv2.waitKey(1)   
   
        
def main(args=None):#We don't provide any argument to the script
    rclpy.init(args=args)  
    node = Detection()
    rclpy.spin(node)
    rclpy.shutdown() 
    exit()

if __name__ == '__main__':
    main()   

     



    
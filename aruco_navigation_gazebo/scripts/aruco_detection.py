#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
from cv2 import aruco
import math
import imutils

class ArucoDetector(Node):
    def __init__(self):
        super().__init__('aruco_detector')
        # Create a subscription to the /camera/image_raw topic
        self.subscription = self.create_subscription(
            Image,
            '/camera/image_raw',
            self.image_callback,
            10
        )
        self.bridge = CvBridge()
        self.center = None
        self.markerID1 = None
        self.radius1 = None
        self.T = 0
        # Define the ArUco dictionary
        self.arucoDict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_1000)
        # Create ArUco parameters
        self.arucoParams = cv2.aruco.DetectorParameters()

    def image_callback(self, msg):
        # Convert ROS 2 Image message to OpenCV image
        image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        # Process the image for ArUco marker detection
        det_result = self.aruco_detection(image)
        # Display the image with detected markers
        cv2.imshow("Aruco Detection", det_result[0])
        cv2.waitKey(1)

    def aruco_detection(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        image = imutils.resize(image, width=1000)
        (corners, ids, rejected) = cv2.aruco.detectMarkers(image, self.arucoDict, parameters=self.arucoParams)

        if len(corners) > 0:
            ids = ids.flatten()
            for (markerCorner, markerID) in zip(corners, ids):
                corners = markerCorner.reshape((4, 2))
                (topLeft, topRight, bottomRight, bottomLeft) = corners
                topRight = (int(topRight[0]), int(topRight[1]))
                bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
                bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
                topLeft = (int(topLeft[0]), int(topLeft[1]))

                radius = int(math.sqrt(
                    (int(topRight[0]) - int(bottomLeft[0])) ** 2 + (int(topRight[1]) - int(bottomLeft[1])) ** 2) / 2)
                cX = int((topLeft[0] + bottomRight[0]) / 2.0)
                cY = int((topLeft[1] + bottomRight[1]) / 2.0)
                cv2.circle(image, (cX, cY), radius, (255, 255, 0), 3)

                cv2.putText(image, "Aruco Marker ID = " + str(markerID),
                            (topLeft[0] + 13, topLeft[1] - 5),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.5, (0, 0, 255), 2)

                self.center = (((topLeft[0] + bottomRight[0]) / 2.0), ((topLeft[1] + bottomRight[1]) / 2.0))
                self.markerID1 = markerID
                self.radius1 = radius

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            exit()

        return [image, self.center, self.radius1, self.markerID1, image]

def main(args=None):
    rclpy.init(args=args)
    aruco_detector = ArucoDetector()
    rclpy.spin(aruco_detector)
    aruco_detector.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

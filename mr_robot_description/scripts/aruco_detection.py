#! /usr/bin/env python3

import imutils
import cv2
from cv2 import aruco
import math

class Detection:
    def __init__(self):
        self.center = None
        self.markerID1 = None
        self.radius1 = None
        self.T = 0
        # Define the ArUco dictionary
        self.arucoDict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_1000)
        # Create ArUco parameters
        self.arucoParams = cv2.aruco.DetectorParameters()


    def aruco_detection(self, image):
        self.image = image
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        image = imutils.resize(image, width=1000)
        (corners, ids, rejected) = cv2.aruco.detectMarkers(image, self.arucoDict, parameters=self.arucoParams)
        
        print(corners)

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
                            (topLeft[0] + 13 , topLeft[1] - 5),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.5, (0, 0, 255), 2)

                self.center = (((topLeft[0] + bottomRight[0]) / 2.0), ((topLeft[1] + bottomRight[1]) / 2.0))
                self.markerID1 = markerID
                self.radius1 = radius

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            exit()

        return [image, self.center, self.radius1, self.markerID1, image]

if __name__ == "__main__":
    det = Detection()
    print(det.arucoParams)
    image_path = "/home/ayush/aruco_ws/src/aruco_navigation_ros2/aruco_navigation_gazebo/models/images.png"
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error: Could not load image from {image_path}")
        exit()

    det_result = det.aruco_detection(image)
    
    cv2.imshow("AYK", det_result[0])
    cv2.waitKey(0)
    cv2.destroyAllWindows()

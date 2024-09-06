#!/bin/bash
xhost +local:docker
docker run --rm -it --net=host --name aruco_container --volume /tmp/.X11-unix:/tmp/.X11-unix --volume .:/aruco_ws/src --workdir /aruco_ws --env DISPLAY=$DISPLAY my_ros_image:2.0 /bin/bash
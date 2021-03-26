#!/bin/bash

docker run --rm \
       --network=host \
       --privileged \
       --volume="/dev:/dev" \
       --volume="/mnt/hdd/video/household:/mmaction2/data/household" \
       --runtime=nvidia \
       --device /dev/snd:/dev/snd \
       -e DISPLAY=$DISPLAY \
       -e QT_X11_NO_MITSHM=1 \
       --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
       -it naoki:mmaction2_actionrecognition
xhost +local:docker

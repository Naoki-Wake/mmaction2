#!/bin/bash

docker run --rm \
       --network=host \
       --privileged \
       --volume="/dev:/dev" \
       --volume="/media/ubuntu18/SSD-PHU3-A/custom_dataset/:/dataset" \
       --runtime=nvidia \
       --device /dev/snd:/dev/snd \
       -e DISPLAY=$DISPLAY \
       -e QT_X11_NO_MITSHM=1 \
       --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
       -it naoki:mmaction2-Oct09-20
xhost +local:docker

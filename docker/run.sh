#!/bin/bash

docker run --rm \
       --network=host \
       --privileged \
       --volume="/dev:/dev" \
       --volume="/mnt/hdd/video/household:/mmaction2/data/household" \
       --volume="/home/ubuntu18/Codes/actionrecognition/mmaction2/tools/data:/mmaction2/tools/data" \
       --volume="/home/ubuntu18/Codes/actionrecognition/mmaction2/configs/recognition/arr_tsm:/mmaction2/configs/recognition/arr_tsm" \
       --volume="/home/ubuntu18/Codes/actionrecognition/mmaction2/work_dirs:/mmaction2/work_dirs" \
       --volume="/home/ubuntu18/Codes/actionrecognition/mmaction2/mmaction/datasets:/mmaction2/mmaction/datasets" \
       --runtime=nvidia \
       --device /dev/snd:/dev/snd \
       -e DISPLAY=$DISPLAY \
       -e QT_X11_NO_MITSHM=1 \
       --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
       -it naoki:mmaction2_actionrecognition
xhost +local:docker

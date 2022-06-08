#!/bin/bash
docker run --rm \
       --network=host \
       --privileged \
       --volume="/dev:/dev" \
       --volume="/mnt/ssd_2T/video/sthv2:/mmaction2/data/sthv2" \
       --volume="/mnt/ssd_2T/video/household:/mmaction2/data/household" \
       --volume="/mnt/ssd_2T/video/demo:/mmaction2/data/demo" \
       --volume="/home/ubuntu18/Codes/actionrecognition/mmaction2/tools/data:/mmaction2/tools/data" \
       --volume="/home/ubuntu18/Codes/actionrecognition/mmaction2/configs/recognition/arr_tsm:/mmaction2/configs/recognition/arr_tsm" \
       --volume="/mnt/ssd_2T/work_dirs:/mmaction2/work_dirs" \
       --volume="/home/ubuntu18/Codes/actionrecognition/mmaction2/mmaction/datasets:/mmaction2/mmaction/datasets" \
       --volume="/home/ubuntu18/Codes/actionrecognition/mmaction2/configs/_base_/models:/mmaction2/configs/_base_/models" \
       --volume="/home/ubuntu18/Codes/actionrecognition/mmaction2/mmaction/models/heads:/mmaction2/mmaction/models/heads" \
       --volume="/home/ubuntu18/Codes/actionrecognition/mmaction2/pretrained_models:/mmaction2/pretrained_models" \
       --volume="/home/ubuntu18/Codes/actionrecognition/mmaction2/imagemagick_config:/etc/ImageMagick-6" \
       --volume="/home/ubuntu18/Codes/actionrecognition/mmaction2/demo:/mmaction2/demo" \
       --runtime=nvidia \
       --device /dev/snd:/dev/snd \
       -it naoki:mmaction2_actionrecognition_2206
xhost +local:docker
#--volume="/mnt/hdd/video/household:/mmaction2/data/household" \
#--volume="/home/ubuntu18/Codes/actionrecognition/mmaction2/work_dirs:/mmaction2/work_dirs" \
#       --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
#-it naoki:mmaction2_actionrecognition
#       -e DISPLAY=$DISPLAY \
#       -e QT_X11_NO_MITSHM=1 \
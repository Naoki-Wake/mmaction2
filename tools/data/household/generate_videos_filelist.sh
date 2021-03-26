#!/usr/bin/env bash

cd ../../../
PYTHONPATH=. python tools/data/build_file_list.py household data/household/videos/ --num-split 1 --level 1 --subset train --format videos --shuffle
PYTHONPATH=. python tools/data/build_file_list.py household data/household/videos/ --num-split 1 --level 1 --subset val --format videos --shuffle
echo "Filelist for videos generated."

cd tools/data/household/

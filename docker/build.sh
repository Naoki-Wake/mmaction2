#!/bin/bash

cd ../..
docker build --network=host -t naoki:mmaction2_actionrecognition_2206 -f mmaction2/docker/Dockerfile .

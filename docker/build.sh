#!/bin/bash

cd ../..
docker build --network=host -t naoki:mmaction2_actionrecognition -f mmaction2/docker/Dockerfile .

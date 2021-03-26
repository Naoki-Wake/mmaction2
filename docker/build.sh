#!/bin/bash

cd ../..
docker build --network=host -t naoki:mmaction2-Oct09-20 -f mmaction2/docker/Dockerfile .

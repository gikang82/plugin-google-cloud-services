#!/usr/bin/env bash
# How to upload
./bin/build.sh

docker push pyengine/google-cloud-services:1.0
docker push spaceone/google-cloud-services:1.0
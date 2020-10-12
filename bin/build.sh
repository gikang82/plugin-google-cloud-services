#!/usr/bin/env bash
# Build a docker image
docker build -t pyengine/google-cloud-services . --no-cache

docker tag pyengine/google-cloud-services pyengine/google-cloud-services:1.0
docker tag pyengine/google-cloud-services spaceone/google-cloud-services:1.0
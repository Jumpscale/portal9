#!/bin/bash

# uploads the successfully built js9 portal image to dockr hub for development re-use

image_id=$(sudo docker images -q jumpscale/base3)
sudo docker tag $image_id jumpscale/js9base3:latest
sudo docker login -u ${DOCKERHUB_LOGIN} -p ${DOCKERHUB_PASS}
sudo docker push jumpscale/js9base3

#!/bin/bash

# uploads the successfully built js9 portal image to dockr hub for development re-use

image_id=$(sudo docker images -q jumpscale/base3)
sudo docker tag $image_id ahussein/js9base3:latest
sudo docker login -u ahussein -p rooter
sudo docker push ahussein/js9base3

#!/bin/bash

# generate ssh keys
ssh-keygen -t rsa -N "" -f ~/.ssh/main
export SSHKEYNAME=main

export GIGSAFE=1
# export GIGBRANCH=$(git symbolic-ref --short HEAD)
export GIGBRANCH=travis_ci
export GIGDEVELOPERBRANCH=travis_ci
echo $GIGBRANCH
curl https://raw.githubusercontent.com/Jumpscale/developer/$GIGDEVELOPERBRANCH/jsinit.sh?$RANDOM > /tmp/jsinit.sh; bash /tmp/jsinit.sh

# build image
source ~/.jsenv.sh
js9_build -l

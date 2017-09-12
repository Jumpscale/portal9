#!/bin/bash

# uploads the successfully built js9 ays image to dockr hub for development re-use

sudo docker login -u ${DOCKERHUB_LOGIN} -p ${DOCKERHUB_PASS}
sudo docker push jumpscale/portal9

#!/bin/bash

# uploads the successfully built portal9 image to dockr hub for development re-use

if [ -n $TRAVIS_EVENT_TYPE ] && [ $TRAVIS_EVENT_TYPE == "cron" ]; then
    image_id=$(sudo docker images -q jumpscale/portal9)
    sudo docker tag $image_id jumpscale/portal9nightly:latest
fi

sudo docker login -u ${DOCKERHUB_LOGIN} -p ${DOCKERHUB_PASS}
sudo docker push jumpscale/portal9nightly


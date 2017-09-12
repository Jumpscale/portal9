#!/bin/bash
set -e
set -x

export SSHKEYNAME=id_rsa

if [ -n $TRAVIS_EVENT_TYPE ] && [ $TRAVIS_EVENT_TYPE == "cron" ]; then
    # Start portal9 container
    sudo -HE bash -c "source /opt/code/github/jumpscale/bash/zlibs.sh; ZKeysLoad; ZDockerActive -b jumpscale/portal9 -i portal9"    
else
    # Start portal9 container
    sudo -HE bash -c "source /opt/code/github/jumpscale/bash/zlibs.sh; ZKeysLoad; ZDockerActive -b jumpscale/portal9nightly -i portal9"
    sudo -HE bash -c "source /opt/code/github/jumpscale/bash/zlibs.sh; ZKeysLoad; container 'pip install -e /opt/code/github/jumpscale/core9'"
    sudo -HE bash -c "source /opt/code/github/jumpscale/bash/zlibs.sh; ZKeysLoad; container 'pip install -e /opt/code/github/jumpscale/lib9'"
    sudo -HE bash -c "source /opt/code/github/jumpscale/bash/zlibs.sh; ZKeysLoad; container 'pip install -e /opt/code/github/jumpscale/prefab9'"
    sudo -HE bash -c "source /opt/code/github/jumpscale/bash/zlibs.sh; ZKeysLoad; container 'pip install -e /opt/code/github/jumpscale/ays9'"
    sudo -HE bash -c "source /opt/code/github/jumpscale/bash/zlibs.sh; ZKeysLoad; container 'pip install -e /opt/code/github/jumpscale/portal9'"
fi


# Run tests
sudo -HE bash -c "ssh -tA  root@localhost -p 2222 \"cd /opt/code/github/jumpscale/portal9; /bin/bash test.sh\""

if [ -n $TRAVIS_EVENT_TYPE ] && [ $TRAVIS_EVENT_TYPE == "cron" ]; then
    sudo -HE bash -c "source /opt/code/github/jumpscale/bash/zlibs.sh; ZKeysLoad; ZDockerCommit -b jumpscale/portal9 -i portal9"
else
    sudo -HE bash -c "source /opt/code/github/jumpscale/bash/zlibs.sh; ZKeysLoad; ZDockerCommit -b jumpscale/portal9nightly -i portal9"
fi

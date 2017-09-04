#!/bin/bash
export SSHKEYNAME=main
source ~/.jsenv.sh
js9_start
ssh -A -i ~/.ssh/main root@localhost -p 2222 'cd /root/gig/code/github/jumpscale/portal9; /bin/bash test.sh'


#!/bin/bash
eval $(ssh-agent)
ssh-add

# Start portal9 container
sudo -HE bash -c "source /opt/code/github/jumpscale/bash/zlibs.sh; ZDockerActive -b jumpscale/portal9 -i portal9"


# Run core tests
sudo -HE bash -c "ssh -tA  root@localhost -p 2222 \"cd /opt/code/github/jumpscale/portal9; /bin/bash test.sh\""

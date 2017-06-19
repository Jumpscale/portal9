#!/bin/bash
export SSHKEYNAME=main
source ~/.jsenv.sh
js9_start
ssh -A -i ~/.ssh/main root@localhost -p 2222 'cd /root/gig/code/github/jumpscale/portal9; /bin/bash test.sh'

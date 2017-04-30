User Management
===============

Defining users
--------------

Users can be added via [JSUser](../../MultiNode/AgentController1/ShellCommands/JSUser.md)

Allow guest access
------------------

It is possible to allow guest access to certain spaces. Todo the
following has to be configured:

-   Define a acl for the guest user.

Example content of .space/acl.cfg

```
#rights:
##R: read
##W: write/modify
##S: sync to e.g. local PC
##A: admin rights
##*: means all rights
guest=R
admin=*
```

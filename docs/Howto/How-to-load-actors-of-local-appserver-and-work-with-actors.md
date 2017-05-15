Loading and working with actors
===============================

When calling j.portal.tools.server.loadActorsInProcess(), then by default system
actors will be available under j.apps.system

```python
import JumpScale.portal

#make sure you are in the appropriate appserver dir
j.sal.fs.changeDir("/opt/jumpscale8/apps/portals/main/")

#load the actors
j.portal.tools.server.loadActorsInProcess()
```

If you want your app actors to be loaded under
`j.apps.<your_app_name>.<your_actor_name>`, you will have to
explicitly load them, cause they are lazy-loaded

```python

machines = j.apps.cloud.cloudbroker.machineList()
```

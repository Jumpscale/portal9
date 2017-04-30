## Running JumpScale Portal

**JumpScale Portal** can be run from standard js8 libraries:

- Starting portal from local js8 shell:

```py
    j.tools.cuisine.local.apps.portal.start()
```
  - Starting portal from remote js8 shell:

```py
    executor = j.tools.executor.getSSHBased(addr="<IP address of remote machine>", port="SSH port of remote machine", login="username", passwd= "password")
    cuisine = j.tools.cuisine.get(executor)
    cuisine.apps.portal.start()
```


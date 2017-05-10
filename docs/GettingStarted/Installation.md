## Installing JumpScale Portal

### Requirements

**JumpScale Portal** has two major dependencies:

 - **JumpScale Core**, also referenced to as the JumpScale framework, needs to be installed
  - See the [installation secion in the JumpScale Core documentation](https://gig.gitbooks.io/jumpscale-core8/content/GettingStarted/Installation.html) for detailed instructions
 - A connection to a running MongoDB instance
  - In order to install a MongoDB instance locally:

```py
    j.tools.cuisine.local.apps.mongo.build()
```

  - In order to install a MongoDB instance on a remote node:

```py
    executor = j.tools.executor.getSSHBased(addr="<IP address of remote machine>", port="SSH port of remote machine", login="username", passwd= "password")
    cuisine = j.tools.cuisine.get(executor)
    cuisine.apps.mongo.build()
```


### Local installion of a JumpScale Portal

Using Cuisine:

```py
j.tools.cuisine.local.portal.install()
```

Your portal content and code can now be placed in the `$JSBASEDIR/apps/portal/main` directory.


### Remote installation of a JumpScale Portal

Using Cuisine:

```py
    j.tools.cuisine.apps.portal.install(mongodbip="<IP address of machine with MongoDB>", mongoport="<MondoDB port>")
```

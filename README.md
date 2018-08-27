![](https://travis-ci.org/Jumpscale/portal9.svg?branch=master)

# JumpScale Portal

JumpScale Portal is a hybrid application server + wiki engine.

- [version & roadmap info](https://github.com/Jumpscale/home/blob/master/README.md)

## Features

* Supports rendering our custom wiki format
* Supports rendering markdown
* Supports our own macros
* Supports actors/webservices


## Installation
* By choosing to install the portal when installing JumpScale9(See [js9 installation](https://github.com/Jumpscale/bash/blob/master/README.md)):

  ```bash
  js9_build -p
  ```
* Or if js9 docker already available, by navigating to portal9 repo and executing:
  ```bash
  bash install.sh
  ```


  > Starting from 9.4.0 if portal is already installed, need to run `9.4.0-user-migration.py` to migrate mongo models.

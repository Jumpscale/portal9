# JumpScale Portal

JumpScale Portal is a hybrid application server + wiki engine.

- [version & roadmap info](../master/releases.md)

## Features

* Supports rendering our custom wiki format
* Supports rendering markdown
* Supports our own macros
* Supports actors/webservices


## Installation
* By choosing to install the portal when installing JumpScale9:

  ```bash
  js9_build -p
  ```
* Or by using prefab inside a js9 docker(Portal repo need to be on the system):
  First navigate to portal9 repo and execute:
  ```bash
  pip3 install -e .
  ```
  Then in a js9 shell:
  ```py
  j.tools.prefab.local.apps.portal.install()
  ```
  Alternatively navigating to portal9 repo and executing:
  ```bash
  bash install.sh
  ```

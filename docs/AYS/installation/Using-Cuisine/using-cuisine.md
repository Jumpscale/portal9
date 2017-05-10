## Installation using JumpScale Cuisine

Side effects of installing a development cockpit:
 - oauth will be disabled for both the portal and cockpit.
 - Everything will be installed locally (all configurations will assume local)
 - You'll get the latest of the branch you're installing from, not the latest stable build. So proceed with caution.
 - Part of the installation pulls in latest code. Make sure your code is committed first.
 - Make sure to specify the branch when installing


To install, in a jshell:
```python
cuisine = j.tools.cuisine.local
cuisine.solutions.cockpit.install_all_in_one(start=True, branch='8.1.0', reset=True)
```

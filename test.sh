#!/bin/bash

# start portal
js9 'j.tools.prefab.local.web.portal.start()'

sleep 30

# check if portal is started
js9 "j.sal.process.checkProcessRunning('portal_start')"

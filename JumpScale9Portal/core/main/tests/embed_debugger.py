from js9 import j
import sys

j.application.debug = (sys.argv[1] == 'True')
# Start debugging if 1+1 == 2
if 1 + 1 == 2:
    j.application.break_into_jshell("DEBUG STARTED")

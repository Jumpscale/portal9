# this must be in the beginning so things are patched before ever imported by other libraries
from gevent import monkey

monkey.patch_socket()
monkey.patch_ssl()
monkey.patch_thread()
monkey.patch_time()

import os
import subprocess
from js9 import j
import JumpScale.portal
import sys

if __name__ == '__main__':
    if 'PORTAL_MAIN' in os.environ:
        args = sys.argv
        instance = args[1]

        j.application.instanceconfig = j.application.getAppInstanceHRD(name="portalminimal", instance=instance)

        j.application.start("portalminimal")

        server = j.portal.server.get()
        server.start()

        j.application.stop()
    else:
        while True:
            env = os.environ.copy()
            env['PORTAL_MAIN'] = 'true'
            print('Loading portal')
            try:
                exitcode = subprocess.call([sys.executable] + sys.argv, env=env)
                if exitcode != 3:
                    j.application.stop(exitcode)
            except KeyboardInterrupt:
                j.application.stop(0)

# this must be in the beginning so things are patched before ever imported by other libraries
from gevent import monkey
# monkey.patch_all()
monkey.patch_socket()
monkey.patch_thread()
monkey.patch_time()
from js9 import j
from JumpScale.tools.cmdutils import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--instance', help="Gridportal instance", required=True)

opts = parser.parse_args()

ays = j.core.atyourservice.get('jumpscale', 'portal', instance=opts.instance)
j.application.instanceconfig = ays.hrd

j.application.start("jumpscale:gridportal")
j.application.initGrid()

j.logger.disable()

j.portal.server.get.start()


j.application.stop()

import time
from js9 import j

j.application.start("jumpscale:portalclientest")
j.application.initGrid()

import JumpScale.portal

client = j.clients.portal.get("127.0.0.1", port=81, secret="1234")
system = client.getActor("system", "master", instance=0)


j.application.stop()

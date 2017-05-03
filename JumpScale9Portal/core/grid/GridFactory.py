from js9 import j


class GridFactory:

    def __init__(self):
        self.__jslocation__ = "j.core.grid"
        self.brokerClient = None
        # self.zobjects = ZCoreModelsFactory()
        self.id = None
        self.nid = None
        self.config = None
        self.roles = list()
        self._healthchecker = None

    @property
    def healthchecker(self):
        return None

    def _loadConfig(self, test=True):
        self.config = j.application.config

        if self.config is None:
            raise RuntimeWarning(
                "Grid/Broker is not configured please run configureBroker/configureNode first and restart jshell")

        self.id = j.application.whoAmI.gid
        self.nid = j.application.whoAmI.nid

        if test:
            if self.id == 0:
                j.errorhandler.raiseInputError(
                    msgpub="Grid needs grid id to be filled in in grid config file", message="", category="", die=True)

            if self.nid == 0:
                j.errorhandler.raiseInputError(
                    msgpub="Grid needs grid node id (grid.nid) to be filled in in grid config file",
                    message="",
                    category="",
                    die=True)

    def init(self, description="", instance=1):
        self._loadConfig(test=False)

        roles = list()
        if self.config.jumpscale['system']['grid'].get("grid.node.roles", False):
            roles = j.application.config.getList('grid.node.roles')
        roles = [role.lower() for role in roles]
        self.roles = roles
        j.logger.consoleloglevel = 5

    def getLocalIPAccessibleByGridMaster(self):
        return j.sal.nettools.getReachableIpAddress(self.config.get("grid.master.ip"), 5544)

    def isGridMasterLocal(self):
        broker = self.config.get("grid.master.ip")
        return j.sal.nettools.isIpLocal(broker)

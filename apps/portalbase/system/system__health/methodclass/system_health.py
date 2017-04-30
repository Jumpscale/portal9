from js9 import j


class system_health(j.tools.code.classGetBase()):

    """
    Alerts handler

    """

    def run(self, nid=None, **kwargs):
        if nid:
            nid = int(nid)
            j.core.grid.healthchecker.runAllOnNode(nid, False)
        else:
            j.core.grid.healthchecker.runOnAllNodes(False)
        return "Scheduled healthcheck"

from . import PortalServer

import time

from js9 import j


class Group():
    pass


class PortalServerFactory():

    def __init__(self):
        self.__jslocation__ = "j.portal.server"
        # self._inited = False
        self.active = None
        self.inprocess = False

    def get(self):
        return PortalServer.PortalServer()

    def getPortalConfig(self, appname):
        cfg = j.sal.fs.joinPaths(j.dirs.base, 'apps', appname, 'cfg', 'portal')
        return j.config.getConfig(cfg)

    def loadActorsInProcess(self, name='main'):
        """
        make sure all actors are loaded on j.apps...
        """
        class FakeServer(object):

            def __init__(self):
                self.actors = dict()
                self.epoch = time.time()
                self.actorsloader = j.portalloader.getActorsLoader()
                self.spacesloader = j.portalloader.getSpacesLoader()

            def addRoute(self, *args, **kwargs):
                pass

            def addSchedule1MinPeriod(self, *args, **kwargs):
                pass

            addSchedule15MinPeriod = addSchedule1MinPeriod

        self.inprocess = True
        # self._inited = False
        j.apps = Group()
        basedir = j.sal.fs.joinPaths(j.dirs.cfgDir, 'portals', name)
        hrd = j.data.hrd.get("%s/config.hrd" % basedir)
        appdir = hrd.get("param.cfg.appdir")
        appdir = appdir.replace("$base", j.dirs.base)
        j.sal.fs.changeDir(appdir)
        server = FakeServer()
        j.portal.server.active = server
        server.actorsloader.scan(appdir)
        server.actorsloader.scan(basedir + "/base")

        for actor in list(server.actorsloader.actors.keys()):
            appname, actorname = actor.split("__", 1)
            try:
                server.actorsloader.getActor(appname, actorname)
            except Exception as e:
                print(("*ERROR*: Could not load actor %s %s:\n%s" % (appname, actorname, e)))

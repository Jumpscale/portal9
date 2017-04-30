from js9 import j
from JumpScale.portal.portalloaders import BucketLoader, SpacesLoader, ActorsLoader, ActorsInfo


class PortalLoaderFactory(object):

    def __init__(self):
        self.__jslocation__ = "j.portalloader"
        self.actorsinfo = ActorsInfo.ActorsInfo()

    def getActorsLoader(self):
        return ActorsLoader.ActorsLoader()

    def getBucketsLoader(self):
        return BucketLoader.BucketLoader()

    def getSpacesLoader(self):
        return SpacesLoader.SpacesLoader()

    def getTemplatesPath(self):
        dirname = j.sal.fs.getDirName(__file__)
        return j.sal.fs.joinPaths(dirname, 'templates')

from js9 import j
from LoaderBase import *


class Bucket(LoaderBaseObject):

    def __init__(self):
        LoaderBaseObject.__init__(self, "bucket")

    def createDefaults(self, path):
        return self._createDefaults(path)

    def loadFromDisk(self, path, reset=False):
        self._loadFromDisk(path, reset=False)


class BucketLoader(LoaderBase):

    def __init__(self):
        """
        """
        LoaderBase.__init__(self, "bucket", Bucket)
        self.bucketIdToBucket = self.id2object
        self.getBucketFromId = self.getLoaderFromId

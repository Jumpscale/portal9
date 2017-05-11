from js9 import j
from .BaseModelFactory import NameSpaceLoader
from . import Models

class PortalSystem(NameSpaceLoader):

    def __init__(self):
        self.__imports__ = "mongoengine"
        super(PortalSystem, self).__init__(Models)

from js9 import j

from . import Models
import inspect

try:
    import mongoengine
except BaseException:
    pass


class NameSpaceLoader:

    def __init__(self, modelsmodule):
        self._module = modelsmodule
        mongoengine.register_connection(self._module.DB, self._module.DB)
        self._getModels()

    def _getModels(self):
        self._models = list()
        self._modelspecs = dict()
        for name, mem in inspect.getmembers(self._module, inspect.isclass):
            if issubclass(mem, mongoengine.base.document.BaseDocument) and mongoengine.Document != inspect.getmro(
                    mem)[0]:
                self._models.append(name)
                self._modelspecs[name] = mem
                self.__dict__[name] = mem

    def addModel(self, modelclass):
        self._models.append(modelclass._class_name)
        self._modelspecs[modelclass._class_name] = modelclass
        self.__dict__[modelclass._class_name] = modelclass

    def listModels(self):
        return self._models

    def connect2mongo(self, host='localhost', port=27017, db='jumpscale_system'):
        """
        """
        mongoengine.connect(db=db, alias=db, host=host, port=port)

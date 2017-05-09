from js9 import j

class CodeGeneratorModelFactory():

    def __init__(self):
        self.__jslocation__ = "j.core.codegeneratormodel"
        # self._inited = False
        self.active = None
        self.inprocess = False

    def get(self, spec, typecheck, dieInGenCode):
        return CodeGeneratorModel(spec=spec, typecheck=typecheck, dieInGenCode=dieInGenCode)


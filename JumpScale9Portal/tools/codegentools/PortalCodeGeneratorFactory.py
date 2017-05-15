from js9 import j

class PortalCodeGeneratorFactory():

    def __init__(self):
        self.active = None
        self.inprocess = False

    def get(self, spec, typecheck, dieInGenCode):
        return CodeGeneratorModel(spec=spec, typecheck=typecheck, dieInGenCode=dieInGenCode)

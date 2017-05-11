from js9 import j
from .CodeGeneratorBase import CodeGeneratorBase


class CodeGeneratorEveModel(CodeGeneratorBase):

    def __init__(self, spec, typecheck=True, dieInGenCode=True, codepath=''):
        CodeGeneratorBase.__init__(self, spec, typecheck, dieInGenCode)
        self.type = "EveModel"

    def generate(self):
        properties = ''
        for prop in self.spec.properties:
            properties += self._generateProperty(prop)
        schema = '''
%s = {
    'scehma': {
        %s
    }
}
''' % (self.spec.name, properties)
        return schema

    def _generateProperty(self, prop):
        result = "'%s': {" % prop.name
        result += "'type': %s" % prop.type
        result += '},'
        return result

from js9 import j

from . import CodeGeneratorBase


class CodeGeneratorModel(CodeGeneratorBase):

    def __init__(self, spec, typecheck=True, dieInGenCode=True):
        CodeGeneratorBase.__init__(self, spec, typecheck, dieInGenCode)
        self.type = "JSModel"

    def getPropertyCode(self, name, type, indent=1):
        value = ""
        pre = ""
        init = ""
        typemap = {'bool': 'boolean', 'str': 'string',
                   'dict': 'dictionary', 'int': 'integer'}
        defaultmap = {'int': '0', 'str': '""', 'float': '0.0',
                      'bool': 'True', 'list': 'list()', 'dict': 'dict()'}
        if '(' in type:
            type = type[0:type.index('(')]

        s = """
if not isinstance(value, %(type)s) and value is not None:
    if isinstance(value, basestring) and j.data.types.%(fulltype)s.checkString(value):
        value = j.data.types.%(fulltype)s.fromString(value)
    else:
        msg="property %(name)s input error, needs to be %(type)s, specfile: %(specfile)s, name model: %(modelname)s, value was:" + str(value)
        raise TypeError(msg)
""" % {'name': name, 'fulltype': typemap.get(type, type), 'type': type,
            'specfile': self.spec.specpath.replace("\\", "/"), 'modelname': self.spec.name}

        if type in defaultmap:
            init = "self._P_%s=%s" % (name, defaultmap.get(type))
        else:
            specfound = j.portal.tools.specparser.specparserfactory.findSpec(
                query=type, findFromSpec=self.spec)

            if specfound.type == "enumeration":
                init = "self._P_%s=0" % name  # is the unknown type
                j.portal.tools.codegentools.portalcodegenerator.generate(specfound, type="enumerator")
                name, path = j.portal.tools.codegentools.portalcodegenerator.getCodeId(
                    specfound, type="enumerator")
                if name not in j.portal.tools.codegentools.portalcodegenerator.classes:
                    raise j.exceptions.RuntimeError(
                        "generation was not successfull for %s, there should be a classes populated" % name)
                enumerationcheck = "j.enumerators.%s" % name.split("enumeration_")[
                    1]
                s = "%s.check(value) or isinstance(value, int)" % enumerationcheck
                type = "enumerator:%s or int" % type
                value = "int(value)"
            elif specfound.type == "model":
                subgen = CodeGeneratorModel(specfound)
                self.content = subgen.generate() + self.content
                pre = "classs= %s\n" % (specfound.getClassName())
                s = "isinstance(value, classs)"
                init = pre
                init += "self._P_%s=classs()" % name
            else:
                s = ""
        s = j.tools.code.indent(s[1:], indent)
        self.initprops += j.tools.code.indent(init, 2)
        return s, value

    def addProperty(self, propertyname, type, default, description):

        s = """
    @property
    def {name}(self):
        return self._P_{name}

    @{name}.setter
    def {name}(self, value):
{optionalvalidation}
        self._P_{name}={value}

    @{name}.deleter
    def {name}(self):
        del self._P_{name}

"""
        s = s.replace("{name}", propertyname)
        validation, value = self.getPropertyCode(propertyname, type, 2)
        if value == "":
            value = "value"
        s = s.replace("{optionalvalidation}", validation)
        s = s.replace("{value}", value)
        self.content += s[1:]

    def addNewObjectMethod(self, propname, rtype, spec):
        if propname[-1] == "s":
            propname2 = propname[:-1]
        else:
            propname2 = propname
        if rtype == "list":
            s = "def new_%s(self,value=None):\n" % propname2
        else:
            s = "def new_%s(self,key,value=None):\n" % propname2
        self.content += "\n%s" % j.tools.code.indent(s, 1)
        s = ""

        if spec not in ["int", "bool", "float", "str", "list", "dict"]:
            gen = CodeGeneratorModel(spec)
            self.content = gen.generate() + self.content
            classstr = "%s()" % (gen.getClassName())
        else:
            if spec == "int":
                classstr = "0"
            elif spec == "bool":
                classstr = "False"
            elif spec == "float":
                classstr = "0.0"
            elif spec == "str":
                classstr = "\"\""
            elif spec == "list":
                classstr = "[]"
            elif spec == "dict":
                classstr = "{}"

        s += "if value==None:\n"
        s += "    value2=%s\n" % classstr
        s += "else:\n"
        s += "    value2=value\n"

        if rtype == "list":
            ssss = """
self._P_{name}.append(value2)
if self._P_{name}[-1].__dict__.has_key("_P_id"):
    self._P_{name}[-1].id=len(self._P_{name})
return self._P_{name}[-1]\n
"""
            ssss = ssss.replace("{name}", propname)
            s += ssss[1:]
        else:
            s += "self._P_%s[key]=value2\n" % propname
            s += "return self._P_%s[key]\n" % propname

        self.content += "\n%s" % j.tools.code.indent(s, 2)

    def addInitExtras(self):
        # following code will be loaded at runtime
        if self.spec.rootobject:
            s = """self._P__meta=["{appname}","{actorname}","{modelname}",{version}] #TODO: version not implemented now, just already foreseen"""
            s = s.replace("{appname}", self.spec.appname)
            s = s.replace("{actorname}", self.spec.actorname)
            s = s.replace("{modelname}", self.spec.name)
            s = s.replace("{version}", "1")
            self.initprops += j.tools.code.indent(s, 2)

    def generate(self):
        if self.spec.rootobject:
            self.addClass(baseclass="j.tools.code.classGetJSRootModelBase()")
        else:
            self.addClass(baseclass="j.tools.code.classGetJSModelBase()")

        for prop in self.spec.properties:
            self.addProperty(propertyname=prop.name, type=prop.type,
                             default=prop.default, description=prop.description)

        if "guid" not in [item.name for item in self.spec.properties]:
            self.addProperty(propertyname="guid", type="str",
                             default="", description="unique guid for object")

        if self.spec.rootobject:
            self.addProperty(propertyname="_meta", type="list",
                             default=[], description="metainfo")

        # if "id" not in [item.name for item in self.spec.properties]:
            #self.addProperty( propertyname="id", type="int", default="", description="unique id for object")

        for prop in self.spec.properties:

            rtype, spec = j.portal.tools.specparser.specparserfactory.getSpecFromTypeStr(
                self.spec.appname, self.spec.actorname, prop.type)
            # print str(rtype)+" : "+str(spec)
            if rtype is not None and rtype != "object" and rtype != "enum":
                if spec not in ["int", "bool", "float", "str"]:
                    self.addNewObjectMethod(prop.name, rtype, spec)

        self.addInitExtras()

        return self.getContent()

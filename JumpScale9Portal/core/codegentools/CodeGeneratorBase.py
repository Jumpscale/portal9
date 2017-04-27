from js9 import j


class CodeGeneratorBase:

    def __init__(self, spec, typecheck=True, dieInGenCode=True):
        self.content = ""
        self.spec = spec
        self.typecheck = typecheck
        self.initprops = ""
        self.die = dieInGenCode
        self.subitems = []

    def descrTo1Line(self, descr):
        descr = descr.strip()
        if descr == "":
            return descr
        descr = descr.replace("\n", "\\n")
        # descr=descr.replace("'n","")
        return descr

    def getClassName(self, subitem=""):
        spec = self.spec
        if subitem == "":
            return "%s_%s_%s_%s" % (self.type, spec.appname, spec.actorname, spec.name.replace(".", "_"))
        else:
            return "%s_%s_%s_%s_%s" % (self.type, spec.appname, spec.actorname, spec.name.replace(".", "_"), subitem)

    def addClass(self, baseclass="", className="", importjumpscale=True, extraImport=""):
        if importjumpscale:
            self.content += "from js9 import j\n"

        if baseclass == "":
            baseclass = "j.tools.code.classGetBase()"
        if className == "":
            className = self.getClassName()

        if extraImport != "":
            self.content += extraImport + "\n"

        self.content += """
class %s({baseclass}):
{descr}
    def __init__(self):
        pass
{initprops}
""" % className
        self.content = self.content.replace("{baseclass}", baseclass)
        if self.spec.description != "":
            self.content = self.content.replace("{descr}\n", j.tools.code.indent(
                '"""\n%s"""\n' % self.spec.description, 1))
        else:
            self.content = self.content.replace("{descr}\n", "")

    def getContent(self):
        self.content = self.content.replace("{initprops}", self.initprops)
        return self.content

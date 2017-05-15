from js9 import j
from .CodeGeneratorActorLocal import CodeGeneratoractorLocal
# from CodeGeneratoractorMethodGreenlet import CodeGeneratoractorMethodGreenlet
# from CodeGeneratorWhoosh import CodeGeneratorWhoosh
from .CodeGeneratorActorTasklets import CodeGeneratoractorTasklets
from .CodeGeneratorActorClass import CodeGeneratoractorClass
from .CodeGeneratorEveModel import CodeGeneratorEveModel
import imp
import sys

# base = j.portal.tools._getBaseClassLoader()

class PortalCodeGenerator():

    def __init__(self):
        self.codepath = j.sal.fs.joinPaths(j.dirs.VARDIR, "code")
        self._target = 'server'
        self.generated = {}  # will have classname inside
        self.classes = {}  # key is name as generated in _getCodeLocation
        j.sal.fs.createDir(self.codepath)
        if self.codepath not in sys.path:
            sys.path.append(self.codepath)
        j.sal.fs.writeFile(j.sal.fs.joinPaths(
            self.codepath, "__init__.py"), "")
        self.appdir = j.sal.fs.getcwd()

    def setTarget(self, target):
        '''
        Sets the target to generate for server or client
        '''
        self._target = target

    def removeFromMem(self, appname, actor):
        appname = appname.lower()
        actor = actor.lower()

        for key2 in list(j.portal.tools.codegentools.portalcodegenerator.classes.keys()):
            type, app, spectype, item, remaining = key2.split("_", 5)
            if app == appname and item.find(actor) == 0:
                # print("remove code generated class %s from memory" % key
                j.portal.tools.codegentools.portalcodegenerator.classes.pop(key2)

        for key2 in list(j.portal.tools.server.active.taskletengines.keys()):
            app, item, remaining = key2.split("_", 2)
            if app == appname and item.find(actor) == 0:
                # print("remove tasklets %s from memory" % key
                j.portal.tools.server.active.taskletengines.pop(key2)

    def resetMemNonSystem(self):
        for key2 in list(j.portal.tools.codegentools.portalcodegenerator.classes.keys()):
            type, app, spectype, item, remaining = key2.split("_", 5)
            if app != "system":
                j.portal.tools.codegentools.portalcodegenerator.classes.pop(key2)

        for key2 in list(j.portal.tools.server.active.taskletengines.keys()):
            app, item, remaining = key2.split("_", 2)
            if app != "system":
                j.portal.tools.server.active.taskletengines.pop(key2)

    def getClassactorLocal(self, appname, actor, typecheck=True, dieInGenCode=True):
        """
        """
        spectype = "actor"
        type = "actorlocal"
        # key="%s_%s_%s_%s_%s" % (type,appname,spectype,actor,actor)
        # if self.classes.has_key(key):
        # return self.classes[key]
        spec = j.portal.tools.specparser.portalspecparserfactory.getactorSpec(appname, actor)
        # spec=j.portal.tools.specparser.portalspecparserfactory.findSpec(appname=appname,actorname=actor,specname=actor,type=spectype,findOnlyOne=True)
        classs = self.generate(
            spec, type=type, typecheck=typecheck, dieInGenCode=dieInGenCode)
        return classs

    def getactorClass(self, appname, actor, typecheck=True, dieInGenCode=True, codepath=None):
        """
        """
        spectype = "actor"
        type = "actorclass"
        # key="%s_%s_%s_%s_%s" % (type,appname,spectype,actor,actor)
        # if self.classes.has_key(key):
        # return self.classes[key]
        spec = j.portal.tools.specparser.portalspecparserfactory.getactorSpec(appname, actor)
        # spec=j.portal.tools.specparser.portalspecparserfactory.findSpec(appname=appname,actorname=actor,specname=actor,type=spectype,findOnlyOne=True)
        classs = self.generate(spec, type=type, typecheck=typecheck,
                               dieInGenCode=dieInGenCode, codepath=codepath)

        return classs

    def getClassesactorMethodGreenlet(self, appname, actor, typecheck=True, dieInGenCode=True):
        """
        return: returns dict with key name methodname and then the class (for each method a class is generated)
        """
        spectype = "actor"
        type = "actormethodgreenlet"
        key = "%s_%s_%s_%s_%s" % (type, appname, spectype, actor, actor)
        # if self.classes.has_key(key):
        # return self.classes[key]
        spec = j.portal.tools.specparser.portalspecparserfactory.getactorSpec(appname, actor)
        # spec=j.portal.tools.specparser.portalspecparserfactory.findSpec(appname=appname,actorname=actor,specname=actor,type=spectype,findOnlyOne=True)
        classs = self.generate(
            spec, type=type, typecheck=typecheck, dieInGenCode=dieInGenCode)
        return classs

    def getClassJSModel(self, appname, actor, modelname, typecheck=True, dieInGenCode=True, codepath=""):
        """
        """
        spectype = "model"
        type = "JSModel"
        key = "%s_%s_%s_%s_%s" % (type, appname, spectype, actor, modelname)
        key = key.replace(".", "_")
        if key in self.classes:
            return self.classes[key]
        # spec=j.portal.tools.specparser.portalspecparserfactory.findSpec(appname=appname,actorname=actor,specname=modelname,type=spectype,findOnlyOne=True)
        spec = j.portal.tools.specparser.portalspecparserfactory.getModelSpec(appname, actor, modelname)
        classs = self.generate(spec, type=type, typecheck=typecheck,
                               dieInGenCode=dieInGenCode, codepath=codepath)
        return classs

    def getCodeJSModel(self, appname, actor, modelname, typecheck=True, dieInGenCode=True, codepath=""):
        """
        """
        spectype = "model"
        type = "JSModel"
        spec = j.portal.tools.specparser.portalspecparserfactory.getModelSpec(appname, actor, modelname)
        cg = j.portal.tools.codegentools.portalcodegeneratorfactory.get(spec, typecheck=True,
                                dieInGenCode=dieInGenCode)
        code = cg.generate()
        return code

    def getCodeEveModel(self, appname, actor, modelname, typecheck=True, dieInGenCode=True, codepath=""):
        """
        """
        spectype = "model"
        type = "EveModel"
        spec = j.portal.tools.specparser.portalspecparserfactory.getModelSpec(appname, actor, modelname)
        cg = CodeGeneratorEveModel(
            spec, typecheck=typecheck, dieInGenCode=dieInGenCode, codepath=codepath)
        code = cg.generate()
        return code

    # def getClassWhoosh(self,appname,actor,modelname,typecheck=True,dieInGenCode=True):
    #     """
    #     """
    #     spectype="model"
    #     type="whoosh"
    #     key="%s_%s_%s_%s_%s" % (type,appname,spectype,actor,modelname)
    #     key=key.replace(".","_")
    # if self.classes.has_key(key):
    # return self.classes[key]
    #     spec=j.portal.tools.specparser.portalspecparserfactory.findSpec(appname=appname,actorname=actor,specname=modelname,type=spectype,findOnlyOne=True)
    #     classs=self.generate(spec,type=type,typecheck=typecheck,dieInGenCode=dieInGenCode)
    #     return classs
    def getClassEnumeration(self, appname, actor, enumname, typecheck=True, dieInGenCode=True):
        """
        """
        spectype = "enumeration"
        type = "enumeration"
        key = "%s_%s_%s_%s_%s" % (type, appname, spectype, actor, enumname)
        # if self.classes.has_key(key):
        # return self.classes[key]
        spec = j.portal.tools.specparser.portalspecparserfactory.findSpec(
            appname=appname, actorname=actor, specname=enumname, type=spectype, findOnlyOne=True)
        self.generate(spec, type=type, typecheck=typecheck,
                      dieInGenCode=dieInGenCode)
        return None

    def getCodeId(self, spec, type):
        return self._getCodeLocation(type, spec.appname, spec.type, spec.actorname, spec.name)

    def generate(
            self,
            spec,
            type,
            typecheck=True,
            dieInGenCode=True,
            appserverclient=None,
            instance=0,
            redis=False,
            wsclient=None,
            codepath=None,
            classpath=None,
            returnClass=True,
            args={},
            makeCopy=False):
        """
        param: spec is spec we want to generate from
        param: type JSModel,actormethodgreenlet,enumeration,actorlocal
        param: typecheck (means in generated code the types will be checked)
        param: dieInGenCode  if true means in generated code we will die when something uneforeseen happens
        return: dict of classes if more than 1 otherwise just the class
        """
        name, path = self._getCodeLocation(
            type, spec.appname, spec.type, spec.actorname, spec.name)
        # path is location in a var dir where code will be generated, is always overwritten
        # if not self.generated.has_key(name):
        if spec.type == "actor" and type == "actorlocal":
            cg = CodeGeneratoractorLocal(spec, typecheck, dieInGenCode)
        elif spec.type == "actor" and type == "actorclass":
            cg = CodeGeneratoractorClass(
                spec, typecheck, dieInGenCode, codepath=codepath, args=args)
        elif spec.type == "actor" and type == "tasklet":
            cg = CodeGeneratoractorTasklets(spec, codepath=codepath)
            cg.generate()
            return {}
        else:
            emsg = "Could not generate code of type %s (did not find) for spec appname:%s actorname:%s type:%s name:%s " % (
                type, spec.appname, spec.actorname, type, spec.name)
            raise j.exceptions.RuntimeError(emsg + " {category:spec.generate}")

        code = cg.generate()

        if not returnClass:
            return

        if classpath is not None:
            path = classpath

        if classpath is not None and j.sal.fs.exists(path):
            pass
        else:
            j.sal.fs.writeFile(path, code)

        if makeCopy:
            j.sal.fs.writeFile(path.replace(".py", ".gen.py"), code)

        # if type.find("enum") != 0:
            # getclass=True
        # else:
            # getclass=True

        classes = []
        result = {}
        if cg.subitems != []:
            # means there is more than 1 class generated
            for subitem in cg.subitems:
                classs = self._import(name, cg.getClassName(subitem), path)
                if classs is not None:
                    result[subitem] = classs
                self.generated[name + "_%s" %
                               subitem] = cg.getClassName(subitem)

        else:
            if classpath is not None:
                result = self._import(
                    cg.getClassName(), cg.getClassName(), path)
            else:
                result = self._import(name, cg.getClassName(), path)

            # self.generated[name]=cg.getClassName()

        return result

    def _getCodeLocation(self, type, appname, spectype, specactor, specname):
        specname = specname.replace(".", "_")
        name = "%s_%s_%s_%s_%s" % (
            type, appname, spectype, specactor, specname)
        path = j.sal.fs.joinPaths(self.codepath, name + ".py")
        return name, path

    def _import(self, name, classname, codepath):
        pp = j.sal.fs.getDirName(j.sal.fs.pathNormalize(codepath))
        # curpath=j.sal.fs.getcwd()
        # j.sal.fs.changeDir(pp)
        if pp not in sys.path:
            sys.path.append(pp)
        ns = dict()
        exec(compile("import %s" % name, '<string>', 'exec'), ns)
        try:
            #exec("from %s import %s" % (name,classname))
            exec("import %s" % name)
        except Exception as e:
            print(e)
            #emsg="could not import code for name:%s " % (name)
            j.errorhandler.raiseBug("", "spec.import", e)

        # if getclass:
        try:
            exec(compile("import imp;imp.reload(%s)" %
                         name, '<string>', 'exec'), ns)
            exec(compile("classs=%s.%s" %
                         (name, classname), '<string>', 'exec'), ns)

            # self.classes[name]=classs
            return ns['classs']
        except Exception as e:
            print(("codepath: %s" % codepath))
            print(e)
            raise

        # j.sal.fs.changeDir(curpath)

        # else:
            # classs=None
            # return None

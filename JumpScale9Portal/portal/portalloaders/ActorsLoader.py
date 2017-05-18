from js9 import j
from .LoaderBase import LoaderBase, LoaderBaseObject

#from JumpScale9Portal.portal.extensions.PMExtensionsGroup import PMExtensionsGroup
#from JumpScale9Portal.portal.extensions.PMExtensions import PMExtensions


# class ActorExtensionsGroup(PMExtensionsGroup):

#    """
#    ActorExtensionsGroup
#    """

#    def __init__(self, path):
#        """
#        ActorExtensionsGroup constructor
#        """

#        PMExtensionsGroup.__init__(self)

#        self.pm_name = "a"
#        self.pm_location = "a"

#        extensionLoader = PMExtensions(self, 'a.')

#        extensionLoader.load(path, True)

#        self._activate()

#    def _activate(self):
#        """
#        Activates all extensions in the extention group
#        """
#        for extensionName in list(self.pm_extensions.keys()):
#            extension = self.pm_extensions[extensionName]
#            extension.activate()

class Class():
    pass


class GroupAppsClass(object):

    def __init__(self, actorsloader):
        self.actorsloader = actorsloader

    def __getattr__(self, appname):
        app = AppClass(appname)
        setattr(self, appname, app)
        return app


class AppClass(object):

    def __init__(self, appname):
        self._appname = appname

    def __getattr__(self, actorname):
        if actorname in ('__members__', '__methods__', 'trait_names', '_getAttributeNames'):
            return object.__getattr__(self, actorname)
        actor = j.apps.actorsloader.getActor(self._appname, actorname)
        setattr(self, actorname, actor)
        return actor


class ActorsLoader(LoaderBase):
    """
    loader for all actors
    """

    def __init__(self):
        """
        """
        LoaderBase.__init__(self, "actor", ActorLoader)
        self.actorIdToActorLoader = self.id2object
        self.getActorLoaderFromId = self.getLoaderFromId
        self.osiscl = None

    def reset(self):
        j.apps = GroupAppsClass(self)
        j.portal.tools.specparser.specparserfactory.app_actornames = {}
        j.portal.tools.specparser.specparserfactory.actornames = []
        j.portal.tools.specparser.specparserfactory.appnames = []
        j.portal.tools.specparser.specparserfactory.modelnames = {}
        j.portal.tools.specparser.specparserfactory.roles = {}
        j.portal.tools.specparser.specparserfactory.specs = {}
        j.portal.tools.codegentools.codegenerator.classes = {}
        # j.portal.tools.server.active._init()

    def getApps(self):
        result = {}
        for item in list(self.id2object.keys()):
            if item.find("__") != -1:
                app = item.split("__")[0]
                result[app] = 1
        return list(result.keys())

    def getAppActors(self):
        result = []
        for item in list(self.id2object.keys()):
            if item.find("__") != -1:
                app, actor = item.split("__", 2)
                result.append([app, actor])
        return result

    def getActor(self, appname, actorname):

        key = "%s__%s" % (appname.lower(), actorname.lower())

        if key in j.portal.tools.server.active.actors:
            return j.portal.tools.server.active.actors[key]

        print(("get actor cache miss for %s %s" % (appname, actorname)))
        if key in self.actorIdToActorLoader:
            loader = self.actorIdToActorLoader[key]
            aobj = loader.activate()
            j.portal.tools.server.active.actors[key] = aobj
            return j.portal.tools.server.active.actors[key]
        else:
            raise RuntimeError("Cannot find actor from app %s with name %s" % (appname, actorname))

    def existsActorLoader(self, appname, actorname):
        key = "%s__%s" % (appname.lower(), actorname.lower())
        return key in self.id2object

    def existsActor(self, appname, actorname):
        key = "%s__%s" % (appname.lower(), actorname.lower())
        return key in j.portal.tools.server.active.actors

    def scan(self, path, reset=False):
        paths = path
        if isinstance(paths, str):
            paths = [paths]

        for path in paths:
            jsonfiles = j.sal.fs.listFilesInDir(path, filter='*.json')
            for jsonfile in jsonfiles:
                j.portal.tools.swaggergen.portalswaggergen.loadSpecFromFile(jsonfile)
                j.portal.tools.swaggergen.portalswaggergen.generateActors(path)

        return super(ActorsLoader, self).scan(paths, reset)

    def loadOsisTasklets(self, actorobject, actorpath, modelname):
        path = j.sal.fs.joinPaths(actorpath, "osis", modelname)
        if j.sal.fs.exists(path):
            for method in ["set", "get", "delete", "list", "find", "datatables"]:
                path2 = j.sal.fs.joinPaths(path, "method_%s" % method)
                actorobject._te["model_%s_%s" % (modelname, method)] = j.tools.taskletengine.get(path2)


class ActorLoader(LoaderBaseObject):

    def __init__(self):
        LoaderBaseObject.__init__(self, "actor")
        self.osiscl = None

    def createDefaults(self, path):
        base = j.sal.fs.joinPaths(j.portal.tools.portalloaders.portalloaderfactory.getTemplatesPath(), "%s" % self.type)
        j.sal.fs.copyDirTree(base, path, overwriteFiles=False)

    def raiseError(self, msg, path=None):
        raise RuntimeError("%s\npath was:%s" % (msg, path))

    def loadFromDisk(self, path, reset=False):
        # the name is $appname__actorname all in lowercase
        name = j.sal.fs.getDirName(path, True)
        # print "load actor dir:%s"%path
        if name.find("__") != -1:
            app, actor = name.split("__", 1)
        else:
            return self.raiseError("Cannot create actor, name of directory needs to be $appname__$actorname", path=path)
        self._loadFromDisk(path, reset=False)
        self.model.application = app
        self.model.actor = actor

    def _removeFromMem(self):
        print(("remove actor %s from memory" % self.model.id))
        j.portal.tools.specparser.specparserfactory.removeSpecsForActor(self.model.application, self.model.actor)
        j.portal.tools.codegentools.codegenerator.removeFromMem(self.model.application, self.model.actor)
        j.portal.tools.server.active.unloadActorFromRoutes(self.model.application, self.model.actor)
        key = "%s_%s" % (self.model.application.lower(), self.model.actor.lower())
        if key in j.portal.tools.server.active.actors:
            j.portal.tools.server.active.actors.pop(key)

    def reset(self):
        self._removeFromMem()
        self.loadFromDisk(self.model.path, reset=True)
        j.portal.tools.server.active.actorsloader.getActor(self.model.application, self.model.actor)

    def _descrTo1Line(self, descr):
        if descr == "":
            return descr
        descr = descr.strip()
        descr = descr.replace("\n", "\\n")
        # descr=descr.replace("'n","")
        return descr

    def activate(self):
        print(("activate actor: %s %s" % (self.model.application, self.model.actor)))

        appname = self.model.application
        actorname = self.model.actor
        actorpath = self.model.path
        # parse the specs
        j.portal.tools.specparser.specparserfactory.parseSpecs("%s/specs" % actorpath, appname=appname, actorname=actorname)

        # retrieve the just parsed spec
        spec = j.portal.tools.specparser.specparserfactory.getactorSpec(appname, actorname, raiseError=False)
        if spec is None:
            return None

        if spec.tags is None:
            spec.tags = ""
        tags = j.data.tags.getObject(spec.tags)

        spec.hasTasklets = tags.labelExists("tasklets")

        # generate the tasklets for the methods of the actor
        # j.portal.tools.codegentools.portalcodegenerator.generate(spec,"tasklet",codepath=actorpath)

        # generate the class for the methods of the actor
        args = {}
        args["tags"] = tags
        classpath = j.sal.fs.joinPaths(actorpath, "methodclass", "%s_%s.py" % (spec.appname, spec.actorname))
        modelNames = j.portal.tools.specparser.specparserfactory.getModelNames(appname, actorname)

        actorobject = j.portal.tools.codegentools.codegenerator.generate(spec, "actorclass", codepath=actorpath, classpath=classpath,
                                                    args=args, makeCopy=True)()

        if len(modelNames) > 0:
            actorobject.models = Class()

            for modelName in modelNames:
                modelspec = j.portal.tools.specparser.specparserfactory.getModelSpec(appname, actorname, modelName)
                modeltags = j.data.tags.getObject(modelspec.tags)

                # will generate the tasklets
                modelHasTasklets = modeltags.labelExists("tasklets")
                if modelHasTasklets:
                    j.portal.tools.codegentools.codegenerator.generate(modelspec, "osis", codepath=actorpath, returnClass=False, args=args)

                if spec.hasTasklets:
                    self.loadOsisTasklets(actorobject, actorpath, modelname=modelspec.name)

                classs = j.portal.tools.codegentools.codegenerator.getClassJSModel(appname, actorname, modelName, codepath=actorpath)
                if modelspec.tags is None:
                    modelspec.tags = ""
                index = j.data.tags.getObject(modelspec.tags).labelExists("index")
                tags = j.data.tags.getObject(modelspec.tags)

                db = j.data.kvs.getMemoryStore()
                osis = False
                if tags.tagExists("dbtype"):
                    dbtypes = [item.lower() for item in tags.tagGet("dbtype").split(",")]
                    if "arakoon" in dbtypes:
                        if dbtypes.index("arakoon") == 0:
                            db = j.data.kvs.getArakoonStore(modelName)
                    if "fs" in dbtypes:
                        if dbtypes.index("fs") == 0:
                            db = j.data.kvs.getFSStore(
                                namespace=modelName, serializers=[
                                    j.data.serializer.getSerializerType('j')])
                    if "redis" in dbtypes:
                        if dbtypes.index("redis") == 0:
                            db = j.data.kvs.getRedisStore(
                                namespace=modelName, serializers=[
                                    j.data.serializer.getSerializerType('j')])
                    if "osis" in dbtypes:
                        osis = True

                if osis:
                    # We need to check if the correct namespace is existing and
                    # the namespace maps to the actor name, every object is a
                    # category
                    namespacename = actorname
                    if not self.osiscl:
                        self.osiscl = j.clients.osis.getByInstance('main')
                    if actorname not in self.osiscl.listNamespaces():
                        template = tags.tagGet('osis_template', 'modelobjects')
                        self.osiscl.createNamespace(actorname, template=template)
                    if modelName not in self.osiscl.listNamespaceCategories(namespacename):
                        self.osiscl.createNamespaceCategory(namespacename, modelName)
                try:
                    if not osis:
                        actorobject.models.__dict__[modelName] = j.core.osismodel.get(
                            appname, actorname, modelName, classs, db, index)
                    else:
                        actorobject.models.__dict__[modelName] = j.core.osismodel.getRemoteOsisDB(
                            appname, actorname, modelName, classs)
                except Exception as e:
                    raise
                    msg = "Could not get osis model for %s_%s_%s.Error was %s." % (appname, actorname, modelName, e)
                    raise RuntimeError(msg)
        # add routes to webserver
        for methodspec in spec.methods:
            # make sure tasklets are loaded

            methodtags = j.data.tags.getObject(methodspec.tags)
            methodspec.hasTasklets = methodtags.labelExists("tasklets")

            if methodspec.hasTasklets or spec.hasTasklets:
                taskletpath = j.sal.fs.joinPaths(actorpath, "methodtasklets", "method_%s" % methodspec.name)
                if not j.sal.fs.exists(taskletpath):
                    j.sal.fs.createDir(taskletpath)
                    taskletContent = """
def main(j, args, params, actor, tags, tasklet):
    return params

def match(j, args, params, actor, tags, tasklet):
    return True
                    """
                    methodtasklet = j.sal.fs.joinPaths(taskletpath, "5_%s.py" % methodspec.name)
                    j.sal.fs.writeFile(methodtasklet, taskletContent)
                actorobject._te[methodspec.name] = j.tools.taskletengine.get(taskletpath)

            if j.portal.tools.server.active is not None:

                params = {}
                for var in methodspec.vars:
                    param = {'optional': False, 'description': '', 'default': None, 'type': None}
                    tags = j.data.tags.getObject(var.tags)
                    if tags.labelExists("optional"):
                        param['optional'] = True
                        descr = var.description + " (optional)"
                    else:
                        descr = var.description
                    param['description'] = descr
                    param['type'] = var.ttype
                    if var.defaultvalue:
                        param['default'] = var.defaultvalue
                    params[var.name] = param

                tags = j.data.tags.getObject(methodspec.tags)
                if tags.tagExists("returnformat"):
                    returnformat = tags.tagGet("returnformat")
                else:
                    returnformat = None

                auth = not tags.labelExists("noauth")
                methodcall = getattr(actorobject, methodspec.name)
                j.portal.tools.server.active.addRoute(methodcall, appname, actorname, methodspec.name, params=params,
                                                description=methodspec.description, auth=auth, returnformat=returnformat)

        # load taskletengines if they do exist
        tepath = j.sal.fs.joinPaths(actorpath, "taskletengines")
        if j.sal.fs.exists(tepath):
            if "taskletengines" not in actorobject.__dict__:
                actorobject.taskletengines = Class()
            tepaths = j.sal.fs.listDirsInDir(tepath)
            for tepath in tepaths:
                actorobject.taskletengines.__dict__[j.sal.fs.getBaseName(tepath)] = j.tools.taskletengine.get(tepath)

        # LOAD actorobject to qbase tree
        if appname not in j.apps.__dict__:
            j.apps.__dict__[appname] = AppClass(appname)

        if actorname not in j.apps.__dict__[appname].__dict__:
            j.apps.__dict__[appname].__dict__[actorname] = actorobject

        if "runningAppserver" in j.portal.__dict__:
            key = "%s_%s" % (spec.appname.lower(), spec.actorname.lower())
            j.portal.tools.server.active.actors[key] = actorobject

        # load extensions
        #actorobject.__dict__['extensions'] = ActorExtensionsGroup(j.sal.fs.joinPaths(actorpath, "extensions"))

        return actorobject

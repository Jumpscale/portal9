from js9 import j
from JumpScale9Portal.portal.auth import auth
from JumpScale9Portal.portal import exceptions


class system_contentmanager(j.tools.code.classGetBase()):

    """
    this actor manages all content on the wiki
    can e.g. notify wiki/appserver of updates of content

    """

    def __init__(self):

        self._te = {}
        self.actorname = "contentmanager"
        self.appname = "system"
        self.dbmem = j.data.kvs.getRedisStore('contentmanager')

    def getActors(self, **args):
        """
        result list(str)

        """
        return list(j.portal.tools.server.active.actorsloader.actors.keys())

    def getActorsWithPaths(self, **args):
        """
        result list([name,path])

        """
        actors = []
        for actor in list(j.portal.tools.server.active.actorsloader.id2object.keys()):
            actor = j.portal.tools.server.active.actorsloader.id2object[actor]
            actors.append([actor.model.id, actor.model.path])
        return actors

    def getBuckets(self, **args):
        """
        result list(str)

        """
        return list(j.portal.tools.server.active.bucketsloader.buckets.keys())

    def getBucketsWithPaths(self, **args):
        """
        result list([name,path])

        """
        buckets = []
        for bucket in list(j.portal.tools.server.active.bucketsloader.id2object.keys()):
            bucket = j.portal.tools.server.active.bucketsloader.id2object[bucket]
            buckets.append([bucket.model.id, bucket.model.path])
        return buckets

    def getContentDirsWithPaths(self, **args):
        """
        return root dirs of content (actors,buckets,spaces)
        result list([name,path])

        """
        objects = []
        for objectname in list(j.portal.tools.server.active.contentdirs.keys()):
            objectpath = j.portal.tools.server.active.contentdirs[objectname]
            objects.append([objectname, objectpath])
        return objects

    def getSpaces(self, **args):
        """
        result list(str)

        """
        return list(j.portal.tools.server.active.spacesloader.spaces.keys())

    def getSpacesWithPaths(self, **args):
        """
        result list([name,path])

        """
        spaces = []
        for space in list(j.portal.tools.server.active.spacesloader.spaces.keys()):
            space = j.portal.tools.server.active.spacesloader.spaces[space]
            spaces.append([space.model.id, space.model.path])
        return spaces

    def modelobjectlist(self, namespace, category, key, **args):
        """
        TODO describe what the goal is of this method
        param:appname
        param:actorname
        param:modelname
        param:key
        """
        dtext = j.portal.tools.datatables.portaldatatables
        data = dtext.getData(namespace, category, key, **args)
        return data

    def modelobjectupdate(self, appname, actorname, key, **args):
        """
        post args with ref_$id which refer to the key which is stored per actor in the cache
        param:appname
        param:actorname
        param:key
        result html

        """
        actor = j.apps.__dict__[appname].__dict__[actorname]
        ctx = args["ctx"]
        data = actor.dbmem.get("form_%s" % key)
        for ref in [item for item in list(ctx.params.keys()) if item.find("ref") == 0]:
            ref0 = int(ref.replace("ref_", ""))
            key, refS = data[1][ref0]  # @ref is how to retrieve info from the object
            model = data[0][key]
            exec("model.%s=args[\"%s\"]" % (refS, ref))

        for modelkey in list(data[0].keys()):
            model = data[0][modelkey]
            exec("actor.model_%s_set(model)" % model._meta[2])
        if 'HTTP_REFERER' in ctx.env:
            headers = [('Location', ctx.env['HTTP_REFERER'])]
            ctx.start_response('302', headers)

    def notifyActorDelete(self, id, **args):
        """
        param:id id of space which changed
        result bool

        """
        self.reloadAll(id)

    def bitbucketreload(self, spacename, **args):
        import os
        s = os.getcwd()
        path = s.split('/apps/')[0]
        mc = j.clients.mercurial.getClient(path)
        mc.pullupdate()
        if spacename != 'None':
            j.portal.tools.server.active.loadSpace(spacename)
        else:
            j.portal.tools.server.active.loadSpace(self.appname)
        return []

    def reloadAll(self, id):
        def reloadApp():
            print("RELOAD APP FOR ACTORS Delete")
            j.portal.tools.server.active.reset()

        j.portal.tools.server.active.actorsloader.id2object.pop(id)

        j.portal.tools.server.active.scheduler.scheduleFromNow(2, 9, reloadApp)
        j.portal.tools.server.active.scheduler.scheduleFromNow(10, 9, reloadApp)

    def notifyActorModification(self, id, **args):
        """
        param:id id of actor which changed
        result bool

        """
        loaders = j.portal.tools.server.active.actorsloader
        loader = loaders.getLoaderFromId(id)
        loader.reset()

    def notifyActorNew(self, path, name, **args):
        """
        param:path path of content which got changed
        param:name name
        result bool

        """
        result = False
        key = name.strip().lower()
        # print "name:%s"%name
        if name.find("__") == -1:
            raise RuntimeError(
                "Cannot create actor with name which is not constructed as $appname__$actorname, here %s" %
                name)
        appname, actorname = name.split("__")
        path = path

        if key not in j.portal.tools.server.active.actorsloader.actors:
            # actor does not exist yet, create required dirs in basedir
            if path == "":
                path = j.sal.fs.joinPaths(j.portal.tools.server.active.basepath, "actors", key)
                j.sal.fs.createDir(path)
                j.sal.fs.createDir(j.sal.fs.joinPaths(path, ".actor"))
            else:
                j.sal.fs.createDir(path)
                j.sal.fs.createDir(j.sal.fs.joinPaths(path, ".actor"))

            print(("scan path:%s" % path))
            j.portal.tools.server.active.actorsloader.scan(path)
            result = True
        else:
            result = False
        return result

    def notifyActorNewDir(self, actorname, actorpath, path, **args):
        """
        param:actorname
        param:actorpath
        param:path

        """
        # put your code here to implement this method
        raise NotImplementedError("not implemented method notifyActorNewDir")

    def notifyBucketDelete(self, id, **args):
        """
        param:id id of bucket which changed
        result bool

        """
        result = None

        # immediate remove
        loaders = j.portal.tools.server.active.bucketsloader
        loaders.removeLoader(id)

        def reloadApp(id=None):
            j.portal.tools.server.active.loadSpaces(reset=True)

        # loader.pop(id)
        # j.portal.tools.server.active.scheduler.scheduleFromNow(1,9,reloadApp,id=id)
        j.portal.tools.server.active.scheduler.scheduleFromNow(10, 9, reloadApp, id=id)
        return result

    def notifyBucketModification(self, id, **args):
        """
        param:id id of bucket which changed
        result bool

        """
        loaders = j.portal.tools.server.active.bucketsloader
        loader = loaders.getLoaderFromId(id)
        loader.reset()

    def notifyBucketNew(self, path, name, **args):
        """
        param:path path of content which got changed
        param:name name
        result bool

        """
        result = False

        key = name.strip().lower()
        path = path

        loader = j.portal.tools.server.active.bucketsloader

        if key not in loader.id2object:
            # does not exist yet, create required dirs in basedir
            if path == "":
                path = j.sal.fs.joinPaths(j.portal.tools.server.active.basepath, "buckets", key)
                j.sal.fs.createDir(path)
                j.sal.fs.createDir(j.sal.fs.joinPaths(path, ".bucket"))
            else:
                j.sal.fs.createDir(path)
                j.sal.fs.createDir(j.sal.fs.joinPaths(path, ".bucket"))

            loader.scan(path)
            result = True
        else:
            result = False

        return result

    def notifyFiledir(self, path, **args):
        """
        param:path path of content which got changed
        result bool

        """
        # put your code here to implement this method
        raise NotImplementedError("not implemented method notifyFiledir")

    def notifySpaceDelete(self, id, **args):
        """
        param:id id of space which changed
        result bool

        """

        # immediate remove
        loaders = j.portal.tools.server.active.spacesloader
        loaders.removeLoader(id)

        def reloadApp():
            print("RELOAD APP SPACE DELETE")
            j.portal.tools.server.active.loadSpaces(reset=True)

        # loader=j.portal.tools.server.active.spacesloader.id2object
        # loader.pop(id)

        j.portal.tools.server.active.addSchedule1MinPeriod(name="reloadportal", method=reloadApp)

    def notifySpaceModification(self, id, **args):
        """
        param:id id of space which changed
        result bool

        """
        id = id.lower()
        loaders = j.portal.tools.server.active.spacesloader
        loader = loaders.getLoaderFromId(id)
        loader.reset()

        ctx = args["ctx"]

        if "payload" in ctx.params:

            payload = j.data.serializer.json.loads(ctx.params["payload"])

            owner = payload["repository"]["owner"]
            name = payload["repository"]["name"]

            cmd = "cd %s/%s/%s;hg pull;hg update -C" % (j.dirs.CODEDIR, owner, name)
            print(("execute %s" % cmd))
            j.system.process.execute(cmd)

    def notifySpaceNew(self, path, name, **args):
        """
        param:path path of content which got changed
        param:name name
        result bool

        """
        result = False

        key = name.strip().lower()

        path = path

        loader = j.portal.tools.server.active.spacesloader

        if key not in loader.id2object:
            # does not exist yet, create required dirs in basedir
            if path == "":
                path = j.sal.fs.joinPaths(j.portal.tools.server.active.basepath, "spaces", name)
            else:
                j.sal.fs.createDir(path)

            # create default content
            mddir = j.sal.fs.joinPaths(path, ".space")
            dest = j.sal.fs.joinPaths(path, "%s.wiki" % name)
            j.sal.fs.createDir(mddir)
            loader.scan(path)
            source = j.sal.fs.joinPaths(mddir, "template.wiki")
            j.sal.fs.copyFile(source, dest)
            result = True
        else:
            result = False
        return result

    def notifySpaceNewDir(self, spacename, spacepath, path, **args):
        """
        param:spacename
        param:spacepath
        param:path

        """
        args = {}
        args["spacename"] = spacename
        args["spacepath"] = spacepath
        args["path"] = path
        return self._te["notifySpaceNewDir"].execute4method(args, params={}, actor=self)

    def prepareActorSpecs(self, app, actor, **args):
        """
        compress specs for specific actor and targz in appropriate download location
        param:app name of app
        param:actor name of actor
        result bool

        """
        result = None

        actorname = actor
        appname = app

        filesroot = j.portal.tools.server.active.filesroot
        actorloader = j.portal.tools.server.active.actorsloader.id2object["%s__%s" % (appname, actorname)]

        path = j.sal.fs.joinPaths(actorloader.model.path, "specs")

        pathdest = j.sal.fs.joinPaths(filesroot, "specs", "%s_%s.tgz" % (appname, actorname))
        j.sal.fs.remove(pathdest)
        # j.sal.fs.createDir(j.sal.fs.joinPaths("files","specs"))

        if not j.sal.fs.exists(path):
            return {"error": "could not find spec path for app %s actor %s" % (appname, actorname)}
        else:
            j.sal.fs.targzCompress(path, pathdest)

        return result

    @auth(['admin'])
    def wikisave(self, cachekey, text, **args):
        """
        param:cachekey key to the doc
        param:text content of file to edit
        result bool

        """
        def decode(value):
            if isinstance(value, bytes):
                return value.decode()
            return value
        contents = j.apps.system.contentmanager.dbmem.get(cachekey)
        contents = {decode(k):decode(v) for k, v in contents.items()}
        j.sal.fs.writeFile(contents['path'], text)
        # after writing the conent, we need to make sure that the doc is marked dirty so that it will be reloaded from the disk
        # there is already a watchdog that monitor all the docs but there is no guarantee that it will mark the doc on time before the redirect is executed
        space = j.portal.tools.server.active.spacesloader.getLoaderFromId(contents['space'])
        if contents['page'] in space.docprocessor.name2doc:
            doc = space.docprocessor.name2doc[contents['page']]
            doc.dirty = True
        returnpath = "/%s/%s" % (contents['space'], contents['page'])
        if contents['querystr']:
            returnpath += "?%s" % contents['querystr']
        raise exceptions.Redirect(returnpath)

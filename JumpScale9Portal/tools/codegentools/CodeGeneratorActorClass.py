from js9 import j
from .CodeGeneratorBase import CodeGeneratorBase


class CodeGeneratoractorClass(CodeGeneratorBase):

    def __init__(self, spec, typecheck=True, dieInGenCode=True, codepath=None, args={}):
        CodeGeneratorBase.__init__(self, spec, typecheck, dieInGenCode)
        self.codepath = j.sal.fs.joinPaths(codepath, "methodclass")
        j.sal.fs.createDir(self.codepath)
        self.type = "actorclass"

        self.tags = args["tags"]

    def getClassName(self):
        return "%s_%s" % (self.spec.appname, self.spec.actorname)

    def getCodeTaskletExecute(self, method):
        key = method.name
        s = "args={}\n"
        for var in method.vars:
            s += "args[\"%s\"]=%s\n" % (var.name, var.name)
        s += "return self._te[\"%s\"].execute4method(args,params={},actor=self)" % key
        return s

#     def getCodeOsisExecute(self, method):

#         na, modelname, methodcall = method.name.split("_", 3)

#         if methodcall == "set":
#             s = """
# return self.models.{modelname}.set(data)
#             """
#         elif methodcall == "get":
#             s = """
# obj = self.models.{modelname}.get(id=id,guid=guid).obj2dict()
# obj.pop('_meta', None)
# return obj
#             """
#         elif methodcall == "delete":
#             s = """
# return self.models.{modelname}.delete(guid=guid, id=id)
#             """
#         elif methodcall == "list":
#             s = """
# return self.models.{modelname}.list()
#             """
#         elif methodcall == "find":
#             s = """
# return self.models.{modelname}.find(query)
#             """
#         elif methodcall == "new":
#             s = """
# return self.models.{modelname}.new()
#             """
#         elif methodcall == "datatables":
#             s = """
# return self.models.{modelname}.datatables()
#             """
#         elif methodcall == "create":
#             s = """
# {modelname} = self.models.{modelname}.new()
# {populatemodel}
# return self.models.{modelname}.set({modelname})
#         """
#         else:
#             raise j.exceptions.RuntimeError("Cound not find method %s for osis.\n%s" % (methodcall, method))

#         s = s.replace("{modelname}", modelname)
#         populateparams = ""
#         vs = method.vars
#         for v in method.vars:
#             newparam = """%(modelname)s.%(v)s = %(v)s\n""" % {'modelname': modelname, 'v': v.name}
#             populateparams += newparam
#         s = s.format(modelname=modelname, populatemodel=populateparams)
#         return s

    def addMethod(self, method):
        spec = self.spec
        s = "def %s({paramcodestr}, **kwargs):\n" % method.name
        descr = ""
        methodtags = j.data.tags.getObject(method.tags)
        method.hasTasklets = methodtags.labelExists("tasklets")

        if method.description != "":
            if method.description[-1] != "\n":
                method.description += "\n\n"
            descr = method.description

        for var in method.vars:
            descr += "param:%s %s" % (var.name,
                                      self.descrTo1Line(var.description))
            if var.defaultvalue is not None:
                descr += " default=%s" % var.defaultvalue
            descr += "\n"

        if method.result is not None:
            descr += "result %s" % method.result.type
            linedescr = self.descrTo1Line(method.result.description)
            if linedescr:
                descr += " %s" % linedescr
            descr += "\n"

        if descr != "":
            s += j.tools.code.indent("\"\"\"\n%s\n\"\"\"\n" %
                                     descr.strip('\n'), 1)

        params = ['self']
        paramsd = list()
        for param in method.vars:
            if param.defaultvalue is not None:
                paramsd.append("%s=%r" % (param.name, param.defaultvalue))
            else:
                params.append(param.name)
        params.extend(paramsd)
        s = s.format(paramcodestr=", ".join(params))
        self.content += "\n%s" % j.tools.code.indent(s, 1)

        # BODY OF METHOD
        # if method.name.find("model_") == 0:
        #     if self.spec.hasTasklets:
        #         s = self.getCodeTaskletExecute(method)
        #         self.content += j.tools.code.indent(s, 2)
        #     else:
        #         s = self.getCodeOsisExecute(method)
        #         self.content += j.tools.code.indent(s, 2)
        # else:
        if method.hasTasklets or self.spec.hasTasklets:
            s = self.getCodeTaskletExecute(method)
            self.content += j.tools.code.indent(s, 2)
        else:
            # generate when no tasklets
            s = "#put your code here to implement this method\n"
            s += "raise NotImplementedError (\"not implemented method %s\")" % method.name
            self.content += j.tools.code.indent(s, 2)

        return

    def addInitExtras(self):
        # following code will be loaded at runtime
        s = """
self._te={}
self.actorname="{actorname}"
self.appname="{appname}"
#{appname}_{actorname}_osis.__init__(self)
"""
        s = s.replace("{appname}", self.spec.appname)
        s = s.replace("{actorname}", self.spec.actorname)
        self.initprops += j.tools.code.indent(s, 2)

    def addInitModel(self):

        if self.tags.labelExists("nomodel"):
            return

        s = ""

        if self.tags.tagExists("dbtype"):
            dbtypes = [item.lower()
                       for item in self.tags.tagGet("dbtype").split(",")]
            ok = False
            if "arakoon" in dbtypes:
                s += """self.dbarakoon=j.data.kvs.getArakoonStore("main", namespace="{appname}_{actorname},serializers=[j.data.serializer.serializers.getSerializerType('j')]")\n"""
                if dbtypes.index("arakoon") == 0:
                    ok = True
                    s += "self.db=self.dbarakoon\n"

            s += "self.dbmem=j.data.kvs.getMemoryStore()\n"
            if "mem" in dbtypes:
                if dbtypes.index("mem") == 0:
                    ok = True
                    s += "self.db=self.dbmem\n"

            if "fs" in dbtypes:
                s += "self.dbfs=j.data.kvs.getFSStore(namespace=\"{actorname}\", baseDir=None,serializers=[j.data.serializer.serializers.getSerializerType('j')])\n"
                if dbtypes.index("fs") == 0:
                    ok = True
                    s += "self.db=self.dbfs\n"

            if ok is False:
                raise j.exceptions.RuntimeError(
                    "Cannot find default db, there needs to be fs,mem or arakoon specified as db on aktor level.")

            if False:  # TODO: "redis" in dbtypes:
                if j.portal.server.active.rediscfg is not None and appname != "system":
                    redisip, redisport, redisdb, rediskey = j.portal.server.active.startConnectRedisServer(
                        appname, actorname)
                    actorobject.dbredis = j.data.kvs.getRedisStore(
                        namespace="", host=redisip, port=redisport, db=redisdb, key=rediskey)
                    actorobject.dbredis.getQueue = actorobject.dbredis.redisclient.getQueue
                if dbtypes.index("redis") == 0:
                    actorobject.db = actorobject.dbredis

        s = s.replace("{appname}", self.spec.appname)
        s = s.replace("{actorname}", self.spec.actorname)
        self.initprops += j.tools.code.indent(s, 2)

    def generate(self):

        mainMethods = {}
        # osisMethods = {}
        for method in self.spec.methods:
            # if method.name.find("model_") == 0:
            #     osisMethods[method.name] = method
            # else:
            mainMethods[method.name] = method

        mainMethods_list = sorted(mainMethods.keys())
        # osisMethods_list = osisMethods.keys()
        # osisMethods_list.sort()

        # OSIS methods
        # self.addClass(className="%s_%s_osis" % (self.spec.appname, self.spec.actorname))

        # self.addInitModel()

        # for methodname in osisMethods_list:
        #     method = osisMethods[methodname]
        #     self.addMethod(method)

        # # write class file
        # ppath = j.sal.fs.joinPaths(self.codepath, "%s_%s_osis.py" % (self.spec.appname, self.spec.actorname))
        # if j.sal.fs.exists(path=ppath):
        #     ppath = j.sal.fs.joinPaths(self.codepath, "%s_%s_osis.gen.py" % (self.spec.appname, self.spec.actorname))
        # else:
        #     from IPython import embed
        #     print "DEBUG NOW opopop"
        #     embed()

        # j.sal.fs.writeFile(ppath, self.getContent())

        # main methods
        self.initprops = ""
        self.content = ""

        # bcls = "%s_%s_osis" % (self.spec.appname, self.spec.actorname)
        # extraimport = "from %s import %s\n" % (bcls, bcls)
        # self.addClass(className="%s_%s" % (self.spec.appname, self.spec.actorname), baseclass=bcls, extraImport=extraimport)
        self.addClass(className="%s_%s" %
                      (self.spec.appname, self.spec.actorname))

        self.addInitExtras()

        for methodname in mainMethods_list:
            method = mainMethods[methodname]
            self.addMethod(method)

        # write class file
        # ppath=j.sal.fs.joinPaths(self.codepath,"%s_%s.py"%(self.spec.appname,self.spec.actorname))
        # ppath2=j.sal.fs.joinPaths(self.codepath,"%s_%s.gen.py"%(self.spec.appname,self.spec.actorname))
        # if True or not j.sal.fs.exists(ppath):
        #     j.sal.fs.writeFile(ppath,self.getContent())
        # j.sal.fs.writeFile(ppath2,self.getContent())

        return self.getContent()

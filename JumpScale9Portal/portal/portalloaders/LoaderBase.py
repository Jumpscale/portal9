from js9 import j
import imp

_INITEDCONTENTDIRS = set()


class LoaderBase(object):
    """
    is loader for all objects e.g. for all actors or spaces
    """

    def __init__(self, type, objectClass):
        """
        """
        self.id2object = {}
        self.__dict__["%ss" % type] = self.id2object
        self.type = type
        self._objectClass = objectClass

    def getLoaderFromId(self, id):
        id = id.lower()
        if id in self.id2object:
            return self.id2object[id]
        else:
            raise RuntimeError("Could not find loader with id %s" % id)

    def removeLoader(self, id):
        id = id.lower()
        if id in self.id2object:
            self.id2object.pop(id)
            loader = self.__dict__["%ss" % self.type]
            if id in loader:
                loader.pop(id)

    # def _getSystemLoaderForUsersGroups(self):
    #     lba = LoaderBaseObject("")
    #     userspath = j.sal.fs.joinPaths(j.portal.tools.server.active.cfgdir, 'users.cfg')
    #     if not j.sal.fs.exists(userspath):
    #         ini = j.config.getInifile(userspath)
    #         ini.addSection('admin')
    #         ini.addParam('admin', 'passwd', 'admin')
    #         ini.addParam('admin', 'groups', 'admin')
    #         ini.addParam('admin', 'reset', '1')
    #         ini.addSection('guest')
    #         ini.addParam('guest', 'passwd', '')
    #         ini.addParam('guest', 'groups', 'guest')
    #         ini.addParam('guest', 'reset', '1')

    #     lba.processUsers(j.portal.tools.server.active.cfgdir)

    def scan(self, path, reset=False):
        """
        path can be 1 path or list of paths
        """
        paths = path
        if isinstance(path, str):
            paths = [path]

        for path in paths:
            items = [j.sal.fs.pathNormalize(item.replace(".%s" % self.type, "") + "/") for
                     item in j.sal.fs.listDirsInDir(path, True, False, True)
                     if j.sal.fs.getDirName(item + "/", True) == ".%s" % self.type]

            if items and str(path) not in _INITEDCONTENTDIRS:
                _INITEDCONTENTDIRS.add(str(path))
                initpath = j.sal.fs.joinPaths(path, 'init.py')
                if j.sal.fs.exists(initpath):
                    module = imp.load_source(str(path), str(initpath))
                    if hasattr(module, 'init'):
                        module.init()

            # find objects like spaces,actors,...
            for path in items:
                object = self._objectClass()
                result = object.loadFromDisk(path, reset)
                if result != False:
                    print(("load %s %s" % (self.type, path)))
                    self.id2object[object.model.id.lower()] = object


class Model():
    pass


class LoaderBaseObject():
    """
    is loader for 1 object
    """

    def __init__(self, type):
        self.model = Model()
        if type == "actor":
            self.model.application = ""
            self.model.actor = ""
        self.model.id = ""
        self.model.path = ""
        self.model.acl = {}  # dict with key the group or username; and the value is a string
        self.type = type
        self.model.hidden = False

    def _createDefaults(self, path):
        if self.type == "space":
            macros = j.sal.fs.joinPaths(j.portal.tools.portalloaders.loaderfactory.getTemplatesPath(), "space/.macros")
            dest = j.sal.fs.joinPaths(path, ".macros")
            j.sal.fs.copyDirTree(macros, dest, keepsymlinks=False, deletefirst=False, overwriteFiles=False)
            if (j.sal.fs.exists("%s/home.md" % path) or j.sal.fs.exists("%s/Home.md" % path)):
                space = "spaceMD"
            elif (j.sal.fs.exists("%s/home.wiki" % path) or j.sal.fs.exists("%s/Home.wiki" % path)):
                space = "spaceWIKI"
            spaces = j.sal.fs.joinPaths(j.portal.tools.portalloaders.loaderfactory.getTemplatesPath(), "space/.%s" % space)
            dest = j.sal.fs.joinPaths(path, ".space")
            j.sal.fs.copyDirTree(spaces, dest, keepsymlinks=False, deletefirst=False, overwriteFiles=False)
        else:
            src = j.sal.fs.joinPaths(j.portal.tools.portalloaders.loaderfactory.getTemplatesPath(), "%s" % self.type)
            dest = j.sal.fs.joinPaths(path)
            j.sal.fs.copyDirTree(src, dest, keepsymlinks=False, deletefirst=False, overwriteFiles=False)

    def _loadFromDisk(self, path, reset=False):
        # path=path.replace("\\","/")
        # print "loadfromdisk:%s" % path

        # remove old cfg and write new one with only id
        cfgpath = j.sal.fs.joinPaths(path, ".%s" % self.type, "main.cfg")

        if not j.sal.fs.exists(cfgpath):
            self.createDefaults(path)

        if j.sal.fs.exists(cfgpath):
            ini = j.tools.inifile.open(cfgpath)
        else:
            ini = j.tools.inifile.new(cfgpath)
        ini.addSection("main")
        name = j.sal.fs.getDirName(path, True)
        ini.setParam("main", "id", name)
        ini.write()

        self.model.id = name
        if ini.checkParam('main', 'name'):
            self.model.name = ini.getValue('main', 'name')
        else:
            self.model.name = name

        if ini.checkParam('main', 'hidden'):
            self.model.hidden = ini.getBooleanValue('main', 'hidden')
        self.model.path = path
        self.processAcl()

    def processAcl(self, cfgdir=""):
        # populate acl
        if cfgdir == "":
            cfgfile = j.sal.fs.joinPaths(self.model.path, ".%s" % self.type, "acl.cfg")
        else:
            cfgfile = j.sal.fs.joinPaths(cfgdir, "acl.cfg")

        lines = j.sal.fs.fileGetContents(cfgfile).split("\n")
        for line in lines:
            line = line.strip()
            if line.strip() == "" or line[0] == "#":
                continue
            for separator in ["=", ":"]:
                if line.find(separator) != -1:
                    name, rights = line.split(separator)
                    name = name.lower().strip()
                    rights = str(rights.lower().strip())
                    self.model.acl[name] = rights
                    # print "ACE:%s %s"%(name,rights)

    def deleteOnDisk(self):
        if j.sal.fs.isLink(self.model.path):
            actualpath = j.sal.fs.readlink(self.model.path)
            j.sal.fs.removeDirTree(actualpath)
        j.sal.fs.removeDirTree(self.model.path)

    def reset(self):
        self.loadFromDisk(self.model.path, reset=True)

from js9 import j
import os

fs = j.sal.fs

from .Doc import *


class DocPreprocessor():

    def __init__(self, contentDirs=[], varsPath="", spacename=""):
        """
        @param contentDirs are the dirs where we will load wiki files from & parse
        @param varsPath is the file with fars (just multiple lines with something like customer = ABC Data)
        @param macrosPath is dir where macro's are they are in form of tasklets
        @param cacheDir if non std caching dir override here

        """
        self.varsPath = varsPath

        self.macroexecutorPreprocessor = j.portal.tools.server.active.macroexecutorPreprocessor
        self.macroexecutorPage = j.portal.tools.server.active.macroexecutorPage
        self.macroexecutorWiki = j.portal.tools.server.active.macroexecutorWiki
        self.macroexecutorMarkDown = j.portal.tools.server.active.macroexecutorMarkDown

        if spacename == "":
            raise RuntimeError("spacename cannot be empty")
        self.spacename = spacename
        self.ignoreDirs = ["/.hg*"]
        self.docs = []
        self.name2doc = {}  # key= name or alias
        self.nametype2doc = {}  # key is name_type
        self.author2docs = {}  # key is authorname
        self._errors = []
        self.params = {}
        self._parsed = {}
        if self.varsPath != "" and fs.exists(self.varsPath):
            lines = fs.fileGetContents(self.varsPath).split("\n")
            for line in lines:
                if line.strip() != "":
                    if line.strip()[0] != "#":
                        if line.find("=") != -1:
                            paramname, value = line.split("=")
                            self.params[paramname.lower()] = value.strip()
        self.images = {}

        from JumpScale9Portal.portal.docpreprocessor.DocHandler import DocHandler, Observer
        self.file_observers = []
        self.doc_handler = DocHandler(self)

        if contentDirs != []:

            from watchdog.events import FileSystemEventHandler
            # The default Observer on Linux (InotifyObserver) hangs in the call to `observer.schedule` because the observer uses `threading.Lock`, which is
            # monkeypatched by `gevent`. To work around this, I use `PollingObserver`. It's more CPU consuming than `InotifyObserver`, but still better than
            # reloading the doc processor
            #
            #from watchdog.observers import Observer
            from watchdog.observers.polling import PollingObserver as Observer

            for contentdir in contentDirs:
                self.scan(contentdir)

                # Watch the contentdir for changes
                observer = Observer()
                self.file_observers.append(observer)
                print(('Monitoring', contentdir))
                observer.schedule(self.doc_handler, contentdir, recursive=True)
                observer.start()

            # add observer for system macros
            observer = Observer()
            self.file_observers.append(observer)
            observer.schedule(self.doc_handler, 'macros', recursive=True)
            observer.start()

    def docNew(self):
        return Doc(self)

    def docAdd(self, doc):
        if doc.pagename == "":
            doc.pagename = doc.name
        self.docs.append(doc)
        self.name2doc[doc.name.lower()] = doc
        self.nametype2doc["%s_%s" % (doc.name, doc.type)] = doc
        for alias in doc.alias:
            if alias.lower().strip() != "":
                self.name2doc[alias] = doc
                self.nametype2doc["%s_%s" % (alias, doc.type)] = doc
        for author in doc.author:
            if author not in self.author2docs:
                self.author2docs[author] = []
            self.author2docs[author].append(doc)

    def docGet(self, docname):

        if docname.lower() in self.name2doc:
            doc = self.name2doc[docname.lower()]
            if doc.dirty:
                doc.loadFromDisk()
                doc.preprocess()
            return doc
        raise RuntimeError("Could not find doc with name %s" % docname)

    def docExists(self, docname):
        return docname.lower() in self.name2doc

    def _pathIgnoreCheck(self, path):
        base = fs.getBaseName(path)
        if base.strip() == "":
            return False
        dirname = fs.getDirName(path, True)
        if dirname.find(".") == 0:
            return True
        if base.find(".tmb") == 0:
            return True
        if base.find(".quarantine") == 0:
            return True
        if path[0] == "_":
            return False
        for item in self.ignoreDirs:
            item = item.replace(".", "\\.")
            item = item.replace("*", ".*")
            if j.data.regex.match(item, path):
                return True
        return False

    def findDocs(self, types=[], products=[], nameFilter=None, parent=None, filterTagsLabels=None):

        if filterTagsLabels is not None:
            if filterTagsLabels.tagExists("name"):
                nameFilter = filterTagsLabels.tagGet("name").lower()
            else:
                nameFilter = None

            if filterTagsLabels.tagExists("parent"):
                parent = filterTagsLabels.tagGet("parent").lower()
            else:
                parent = None

            if filterTagsLabels.tagExists("product"):
                products = filterTagsLabels.tagGet("product")
                products = [item.strip().lower() for item in products.split(",")]
            else:
                products = []

            if filterTagsLabels.tagExists("type"):
                types = filterTagsLabels.tagGet("type")
                types = [item.strip().lower() for item in types.split(",")]
            else:
                types = []

        result = []
        for doc in self.docs:
            typefound = False
            productfound = False
            namefound = False
            parentfound = False

            if parent is None:
                parentfound = True
            else:
                parentfound = doc.parent.lower() == parent.lower()

            if types == []:
                typefound = True
            else:
                if doc.type in types:
                    typefound = True

            if products == []:
                productfound = True
            else:
                for product in products:
                    if product in doc.products:
                        productfound = True

            if nameFilter is None:
                namefound = True
            else:
                if j.data.regex.match(nameFilter.lower(), doc.name.lower()):
                    namefound = True
                for alias in doc.alias:
                    if alias != "":
                        if j.data.regex.match(nameFilter.lower(), alias.lower()):
                            namefound = True
            if typefound and productfound and namefound and parentfound:
                result.append(doc)
        return result

    def scan(self, path):
        print(("DOCPREPROCESSOR SCAN space:%s" % path))
        self.space_path = path

        spaceconfigdir = fs.getDirName(path + "/" + ".space" + "/")
        if fs.exists(spaceconfigdir):
            lastDefaultPath = ""
            if fs.exists(spaceconfigdir + "/default.wiki"):
                lastDefaultPath = spaceconfigdir + "/default.wiki"
            elif fs.exists(spaceconfigdir + "/default.md"):
                lastDefaultPath = spaceconfigdir + "/default.md"
            defaultdir = path
            lastparamsdir = ""
            lastparams = {}
            paramscfgfile = fs.joinPaths(spaceconfigdir, "params.cfg")
            if fs.exists(paramscfgfile):
                paramsfile = fs.fileGetContents(paramscfgfile)
                lastparamsdir = path
                for line in paramsfile.split("\n"):
                    if line.strip() != "" and line[0] != "#":
                        param1, val1 = line.split("=", 1)
                        lastparams[param1.strip().lower()] = val1.strip()
            lastnavdir = path
            lastnav = ""
            if fs.exists(spaceconfigdir + "/nav.wiki"):
                lastnav = fs.fileGetTextContents(spaceconfigdir + "/nav.wiki")
            elif fs.exists(spaceconfigdir + "/nav.md"):
                lastnav = fs.fileGetTextContents(spaceconfigdir + "/nav.md")
        else:
            raise RuntimeError("space dir needs to have a dir .space for %s" % path)
        docs = self._scan(path, defaultdir, lastDefaultPath, lastparams, lastparamsdir, lastnav, lastnavdir)
        # print "SCANDONE"
        for doc in docs:
            doc.loadFromDisk()

        self.findChildren()
        self.spacename = fs.getDirName(path, True).lower()

    def parseHtmlDoc(self, path):
        subject = fs.fileGetTextContents(path)
        head = j.data.regex.findHtmlBlock(subject, "head", path, False)
        body = j.data.regex.findHtmlBlock(subject, "body", path, True)
        return head, body

    @staticmethod
    def is_image(img):
        return img.lower().endswith((".jpg", ".jpeg", ".png", ".gif"))

    def add_image(self, img):
        img = img.strip()
        img2 = fs.getBaseName(img.replace("\\", "/")).lower()
        self.images[img2] = img

    def _scan(self, path, defaultdir="", lastDefaultPath="", lastparams={}, lastparamsdir="",
              lastnav="", lastnavdir="", parent="", docs=[]):
        """
        directory to walk over and find story, task, ... statements
        """
        images = fs.listFilesInDir(path, True)
        for image in images:
            if DocPreprocessor.is_image(image):
                self.add_image(image)

        files = fs.listFilesInDir(path, False)
        parent2 = fs.getDirName(path + "/", True).lower()
        files.sort()

        def isRootDir(path):
            "check if dir is a bucket, actor or space dir, if yes should not descend"
            dirname = fs.getDirName(path + "/", True).lower()
            if dirname[0] == ".":
                return True
            # check if .space or .bucket or .actor in directory (subdir) if so return False
            return any(fs.exists(fs.joinPaths(path, item)) for item in [".space", ".bucket", ".actor"])

        lastBaseNameHtmlLower = ""
        for pathItem in files:
            defaultdir, lastDefaultPath, lastparams, lastparamsdir, lastnav, lastnavdir, lastBaseNameHtmlLower = self.add_doc(pathItem, path, docs, defaultdir, lastDefaultPath, lastparams, lastparamsdir,
                                                                                                                              lastnav, lastnavdir, parent, lastBaseNameHtmlLower)

        ddirs = fs.listDirsInDir(path, False)
        # print "dirs:%s" % ddirs
        for ddir in ddirs:
            if not isRootDir(ddir):
                self._scan(ddir, defaultdir, lastDefaultPath, lastparams, lastparamsdir,
                           lastnav, lastnavdir, parent=parent2)

        return docs

    def add_doc(self, pathItem, path, docs, defaultdir="", lastDefaultPath="", lastparams={}, lastparamsdir="",
                lastnav="", lastnavdir="", parent="", lastBaseNameHtmlLower=''):
        def checkDefault(path, name):
            name2 = fs.getDirName(path, True).lower()
            if name == name2:
                return True
            dirpath = fs.getDirName(path)
            return fs.exists(fs.joinPaths(dirpath, ".usedefault"))

        parent2 = fs.getDirName(path + "/", True).lower()

        if self._pathIgnoreCheck(pathItem):
            return defaultdir, lastDefaultPath, lastparams, lastparamsdir, lastnav, lastnavdir, lastBaseNameHtmlLower

        basename = fs.getBaseName(pathItem).lower()
        # print "basename:%s" % basename

        # DEAL WITH DEFAULTS & NAVIGATIONS
        if pathItem.find(lastparamsdir) != 0:
            # previous default does not count
            lastparamsdir = ""
            lastparams = {}
        if pathItem.find(defaultdir) != 0:
            # previous default does not count
            defaultdir = ""
            lastDefaultPath = ""
        if pathItem.find(lastnavdir) != 0:
            print(("CANCEL lastnav %s cancel" % lastnavdir))
            lastnavdir = ""
            lastnav = ""
        if basename in [".nav.wiki", "nav.wiki", ".nav.md", "nav.md"]:
            lastnav = fs.fileGetTextContents(pathItem)
            lastnavdir = fs.getDirName(pathItem)
            return defaultdir, lastDefaultPath, lastparams, lastparamsdir, lastnav, lastnavdir, lastBaseNameHtmlLower
        if basename in [".default.wiki", "default.wiki", ".default.md", "default.md"]:
            lastDefaultPath = pathItem
            defaultdir = fs.getDirName(pathItem)
            return defaultdir, lastDefaultPath, lastparams, lastparamsdir, lastnav, lastnavdir, lastBaseNameHtmlLower
        if basename in ["params.cfg", ".params.cfg", "params", ".params"]:
            paramsfile = fs.fileGetContents(pathItem)
            lastparamsdir = fs.getDirName(pathItem)

            for line in paramsfile.split("\n"):
                if line.strip() != "" and line[0] != "#":
                    param1, val1 = line.split("=", 1)
                    paramskey = os.path.normpath(lastparamsdir)
                    if paramskey in lastparams:
                        newparams = lastparams[paramskey]
                        newparams[param1.strip().lower()] = val1.strip()
                    else:
                        newparams = {param1.strip().lower(): val1.strip()}
                    lastparams[paramskey] = newparams
            return defaultdir, lastDefaultPath, lastparams, lastparamsdir, lastnav, lastnavdir, lastBaseNameHtmlLower

        # print pathItem
        # print "lastnav %s" % lastnavdir

        # path2 is relative part of path
        if pathItem.find(path) == 0:
            path2 = pathItem[len(path):]
        else:
            path2 = pathItem

        # print "parse %s" % path2
        # normalize relative path call path3
        path3 = path2.lstrip("/").lstrip("\\")

        # process the html docs
        if fs.getFileExtension(pathItem) == "html":
            # because of sorting html doc should always come first
            lastBaseNameHtml = fs.getBaseName(pathItem).replace(".html", "")
            if lastBaseNameHtml[0] not in ["_", "."]:
                lastDirHtml = fs.getDirName(pathItem)
                wikiCorrespondingPath = fs.joinPaths(lastDirHtml, lastBaseNameHtml + ".wiki")
                if not fs.exists(wikiCorrespondingPath):
                    C = "@usedefault\n\n{{htmlloadheader}}\n\n{{htmlloadbody}}\n"
                    fs.writeFile(wikiCorrespondingPath, C)

        extension = fs.getFileExtension(pathItem)
        if extension in ('md', "wiki"):

            # print "lastdefaultpath:%s" % lastDefaultPath
            if extension == 'md':
                doc = DocMD(self)
            else:
                doc = Doc(self)

            doc.original_name = fs.getBaseName(pathItem).replace(".%s" % extension, "")
            doc.name = doc.original_name.lower()
            print(("doc:%s path:%s" % (doc.name, pathItem)))

            if extension == 'md':
                doc.parent = parent
                doc.usedefault = True

            if checkDefault(pathItem, doc.name):
                # print "default %s" %lastDefaultPath
                doc.parent = parent
                doc.usedefault = True
            else:
                doc.parent = parent2

            doc.defaultPath = lastDefaultPath

            htmlpath = j.sal.fs.joinPaths(fs.getDirName(path), "%s.html" % doc.original_name)

            if j.sal.fs.exists(path=htmlpath):
                lastHeaderHtml, lastBodyHtml = self.parseHtmlDoc(htmlpath)
                doc.htmlHeadersCustom.append(lastHeaderHtml)
                doc.htmlBodiesCustom.append(lastBodyHtml)

            docdir = os.path.normpath(fs.getDirName(pathItem))

            while(docdir != ''):
                if docdir in lastparams:
                    newparams = lastparams[docdir]
                    if doc.docparams:
                        doc.docparams = newparams.update(doc.docparams)
                    else:
                        doc.docparams = newparams
                docdir = fs.getParent(docdir)
            # print "**********lastnav"
            # print lastnav
            # print "**********lastnavend"
            doc.navigation = lastnav
            doc.path = pathItem  # .replace("\\","/")
            doc.shortpath = path3

            self.docAdd(doc)
            docs.append(doc)

        return defaultdir, lastDefaultPath, lastparams, lastparamsdir, lastnav, lastnavdir, lastBaseNameHtmlLower

    def findChildren(self):
        for doc in self.docs:
            if doc.parent != "":
                if doc.parent in self.name2doc:
                    #from JumpScale.core.Shell import ipshellDebug,ipshell
                    # print "DEBUG NOW "
                    # ipshell()

                    #raise RuntimeError("Could not find parent %s for doc %s" % (doc.parent,doc.path))
                    # else:
                    self.name2doc[doc.parent].children.append(doc)

    def __str__(self):
        ss = ""
        ss += "%s\n" % self.docs
        return ss

    def __repr__(self):
        return self.__str__()

base_loader = j.portal.tools._getBaseClassLoader()


class docpreprocessor(base_loader):

    def __init__(self):
        base_loader.__init__(self)

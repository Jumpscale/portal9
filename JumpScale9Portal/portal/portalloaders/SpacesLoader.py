from js9 import j
from LoaderBase import LoaderBaseObject, LoaderBase


class Space(LoaderBaseObject):

    def __init__(self):
        LoaderBaseObject.__init__(self, "space")
        self._docprocessor = None
        self._loading = False

    @property
    def docprocessor(self):
        if not self._docprocessor:
            self.loadDocProcessor(False)
        return self._docprocessor

    def loadDocProcessor(self, force=False):
        if self._loading and force == False:
            return
        self._loading = True
        self.createDefaultDir()
        if j.sal.fs.exists(j.sal.fs.joinPaths(self.model.path, ".macros")):
            # load the macro's only relevant to the space, the generic ones are loaded on docpreprocessorlevel
            macroPathsPreprocessor = [j.sal.fs.joinPaths(self.model.path, ".macros", "preprocess")]
            macroPathsWiki = [j.sal.fs.joinPaths(self.model.path, ".macros", "wiki")]
            macroPathsPage = [j.sal.fs.joinPaths(self.model.path, ".macros", "page")]
            macroPathsMarkDown = [j.sal.fs.joinPaths(self.model.path, ".macros", "markdown")]

            name = self.model.id.lower()
            webserver = j.portal.server.active
            webserver.macroexecutorPage.addMacros(macroPathsPage, name)
            webserver.macroexecutorPreprocessor.addMacros(macroPathsPreprocessor, name)
            webserver.macroexecutorWiki.addMacros(macroPathsWiki, name)
            webserver.macroexecutorMarkDown.addMacros(macroPathsMarkDown, name)

        self._docprocessor = j.portal.tools.docpreprocessorparser.get(
            contentDirs=[self.model.path], spacename=self.model.id)

    def createTemplate(self, path, templatetype='wiki'):
        header = '##' if templatetype == 'md' else 'h2.'
        template = '''
%(header)s $$page

%(header)s children

{{children: bullets}}
''' % {'header': header}
        templatepath = j.sal.fs.joinPaths(path, '.space', 'template.%s' % templatetype)
        j.sal.fs.writeFile(templatepath, template)

    def createDefaults(self, path):
        self._createDefaults(path)

    def createDefaultDir(self):

        def callbackForMatchDir(path, arg):
            dirname = j.sal.fs.getDirName(path + "/", lastOnly=True)
            if dirname.find(".") == 0:
                return False
            # l = len(j.sal.fs.listFilesInDir(path))
            # if l > 0:
            #     return False
            return True

        def callbackFunctionDir(path, arg):
            dirname = j.sal.fs.getDirName(path + "/", lastOnly=True)
            dirname = j.sal.fs.getDirName(path + "/", lastOnly=True)

            wikipath = j.sal.fs.joinPaths(path, "%s.wiki" % dirname)
            mdpath = j.sal.fs.joinPaths(path, "%s.md" % dirname)
            if not j.sal.fs.exists(wikipath) and not j.sal.fs.exists(mdpath):
                dirnamel = dirname.lower()
                for item in j.sal.fs.listFilesInDir(path):
                    item = j.sal.fs.getDirName(item + "/", lastOnly=True)
                    extension = j.sal.fs.getFileExtension(item)
                    item = item.lower()
                    item = item.rstrip(".%s" % extension)
                    print(item)
                    if item == dirnamel:
                        return
                spacepath = j.sal.fs.joinPaths(self.model.path, '.space/')
                templates = j.sal.fs.walk(spacepath, recurse=0, pattern='template[.]*')
                if not templates:
                    self.createTemplate(self.model.path)
                    source = j.sal.fs.joinPaths(spacepath, 'template.wiki')
                    templatetype = 'wiki'
                else:
                    source = templates[0]
                    templatetype = j.sal.fs.getFileExtension(source)
                dest = j.sal.fs.joinPaths(path, "%s.%s" % (dirname, templatetype))
                j.sal.fs.copyFile(source, dest)

                print(("NOTIFY NEW DIR %s IN SPACE %s" % (path, self.model.id)))

            return True

        j.sal.fswalker.walkFunctional(self.model.path, callbackFunctionFile=None, callbackFunctionDir=callbackFunctionDir, arg=self.model,
                                      callbackForMatchDir=callbackForMatchDir, callbackForMatchFile=False)  # false means will not process files

    def loadFromDisk(self, path, reset=False):
        self._loadFromDisk(path, reset=False)

    def reset(self):
        self.docprocessor = None
        self.loadFromDisk(self.model.path, reset=True)


class SpacesLoader(LoaderBase):

    def __init__(self):
        """
        """
        LoaderBase.__init__(self, "space", Space)
        self.macrospath = ""
        self.spaceIdToSpace = self.id2object
        self.getSpaceFromId = self.getLoaderFromId

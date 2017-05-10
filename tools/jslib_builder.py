

from js9 import j


class builder():

    # @property
    # def buildDir(self):
    #     return j.sal.fs.joinPaths(j.dirs.TMPDIR, "jsbuilder")

    @property
    def cuisine(self):
        return j.tools.cuisine.local

    # ALL NOT NEEDED ANY LONGER USE bower

    # def angular(self):
    #     version = "1.5.9"
    #     url = "http://code.angularjs.org/%s/angular-%s.zip" % (version, version)
    #     path = j.do.download(url, to='', overwrite=False, retry=3, timeout=0)
    #     dpath = j.sal.fs.joinPaths(self.buildDir, "angular")
    #     j.sal.fs.removeDirTree(dpath)
    #     z = j.tools.zipfile.get(path)
    #     z.extract(self.buildDir)
    #     z.close()
    #     j.sal.fs.renameDir(j.sal.fs.joinPaths(self.buildDir, "angular-%s" % sversion), dpath)
    #     # self._removeMapFiles(dpath)
    #
    # def _removeMapFiles(self, path):
    #     for item in j.sal.fs.find(path, "*.js.map"):
    #         item = "%s/%s" % (path, item)
    #         # print(item)
    #         j.sal.fs.remove(item)
    #
    # def bootstrap(self):
    #     version = "3.3.7"
    #     url = "https://github.com/twbs/bootstrap/releases/download/v%s/bootstrap-%s-dist.zip" % (version, version)
    #     path = j.do.download(url, to='', overwrite=False, retry=3, timeout=0)
    #     dpath = j.sal.fs.joinPaths(self.buildDir, "bootstrap")
    #     j.sal.fs.removeDirTree(dpath)
    #     z = j.tools.zipfile.get(path)
    #     z.extract(self.buildDir)
    #     z.close()
    #     j.sal.fs.renameDir(j.sal.fs.joinPaths(self.buildDir, "bootstrap-%s-dist" % version), dpath)
    #     # self._removeMapFiles(dpath)
    #
    # def codemirror(self):
    #
    #     version = "5.9"
    #     url = "http://codemirror.net/codemirror-%s.zip" % version
    #     path = j.do.download(url, to='', overwrite=False, retry=3, timeout=0)
    #     dpath = j.sal.fs.joinPaths(self.buildDir, "codemirror")
    #     j.sal.fs.removeDirTree(dpath)
    #     z = j.tools.zipfile.get(path)
    #     z.extract(self.buildDir)
    #     z.close()
    #     j.sal.fs.renameDir(j.sal.fs.joinPaths(self.buildDir, "codemirror-%s" % version), dpath)

    # @property
    # def npm(self):
    #     if self._npm == False:
    #         if j.sal.fs.exists("%s/npm" % j.dirs.BINDIR, followlinks=True) == False:
    #             self.cuisine.apps.nodejs.install()
    #         self._npm = "%snpm" % j.dirs.BINDIR
    #     return self._npm

    # @property
    # def bower(self):
    #     if self._bower == False:
    #         if j.sal.fs.exists("%s/bower" % j.dirs.BINDIR, followlinks=True) == False:
    #             self.cuisine.apps.nodejs.install()
    #         self._bower = "%sbower" % j.dirs.BINDIR
    #     return self._bower
    # def famous(self):
    #     url = "https://github.com/Famous/engine-seed"
    #     cdest = j.do.pullGitRepo(url)
    #     res = j.sal.process.executeWithoutPipe("cd %s;%s install" % (cdest, self.npm))
    #
    # def flatui(self):
    #     url = "https://github.com/designmodo/Flat-UI.git"
    #     cdest = j.do.pullGitRepo(url)
    #     print("npm/bower install")
    #     res = j.sal.process.executeWithoutPipe("cd %s;%s install;%s install" % (cdest, self.npm, self.bower))
    #
    # def do1(self):
    #     j.sal.fs.createDir(j.sal.fs.joinPaths(j.dirs.TMPDIR, "jsbuilder"))
    #     if self.checkIPFS == False:
    #         self.getIPFS()
    #     # self.angular()
    #     # self.bootstrap()
    #     # self.codemirror()
    #     # self.famous()
    #     self.flatui()

    def do(self):

        if self.checkIPFS == False:
            self.getIPFS()

        # self.cuisine.apps.nodejs.bowerInstall(["jquery", "flatui", "bootstrap", "famous", "codemirror", "font-awesome", "jqplot",
        #                                        "underscore", "spin", "moment", "http://DlhSoft.com/Packages/DlhSoft.KanbanLibrary.zip", "jqwidgets", "d3", "angular-latest"])

        cmd = "cd $TMPDIR/bower;ipfs -c $JSCFGDIR/ipfs/main/ add -r bower_components"
        print("IPFS upload, can take couple of minutes")

        res = self.cuisine.core.run(cmd)

    def checkIPFS(self):
        return j.sal.nettools.checkUrlReachable("http://localhost:5001/webui") == True

    def getIPFS(self):
        j.tools.cuisine.local.apps.ipfs.install()
        j.tools.cuisine.local.apps.ipfs.start()


b = builder()
b.do()

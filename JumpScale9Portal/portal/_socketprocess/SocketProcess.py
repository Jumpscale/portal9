import gevent
import sys
from gevent.server import StreamServer

from js9 import j
import inspect
import time
import os
from PortalTCPChannels import ManholeSession, WorkerSession, TCPSessionLog

try:
    import fcntl
except:
    pass


raise RuntimeError("is not working now")
# THERE ARE SOME GOOD IDEAS IN HERE IN HOW TO BUILD A SOCKET SERVER WITH MANOLE, ...


class PortalProcess():

    """
    """

    def __init__(self, mainLoop=None, inprocess=False, cfgdir="", startdir=""):

        self.started = False
        # self.logs=[]
        # self.errors=[]
        self.epoch = time.time()
        self.lock = {}

        # j.errorconditionhandler.setExceptHook() #@does not do much?

        # Trigger the key value store extension so the enum is loaded
        self.cfgdir = cfgdir

        if self.cfgdir == "":
            self.cfgdir = "cfg"

        # check if the dir we got started from is a link, if so will create a new dir and copy the config files to there
        if j.sal.fs.isLink(startdir, True):
            # we are link do not use this config info
            name = j.sal.fs.getDirName(startdir + "/", True) + "_localconfig"
            newpath = j.sal.fs.joinPaths(j.sal.fs.getParent(startdir + "/"), name)
            if not j.sal.fs.exists(newpath):
                j.sal.fs.createDir(newpath)
                pathcfgold = j.sal.fs.joinPaths(startdir, "cfg")
                j.sal.fs.copyDirTree(pathcfgold, newpath)
            self.cfgdir = newpath

        ini = j.tools.inifile.open(self.cfgdir + "/portal.cfg")

        if ini.checkParam("main", "appdir"):
            self.appdir = self._replaceVar(ini.getValue("main", "appdir"))
            self.appdir = self.appdir.replace("$base", j.dirs.base)
        else:
            self.appdir = j.sal.fs.getcwd()

        # self.codepath=ini.getValue("main","codepath")
        # if self.codepath.strip()=="":
            # self.codepath=j.sal.fs.joinPaths( j.dirs.varDir,"actorscode")
        # j.sal.fs.createDir(self.codepath)

        # self.specpath=ini.getValue("main","specpath")
        # if self.specpath.strip()=="":
            # self.specpath="specs"
        # if not j.sal.fs.exists(self.specpath):
            # raise RuntimeError("spec path does have to exist: %s" % self.specpath)

        dbtype = ini.getValue("main", "dbtype").lower().strip()
        if dbtype == "fs":
            self.dbtype = "FS"
        elif dbtype == "mem":
            self.dbtype = "MEMORY"
        elif dbtype == "redis":
            self.dbtype = "REDIS"
        elif dbtype == "arakoon":
            self.dbtype = "ARAKOON"
        else:
            raise RuntimeError(
                "could not find appropriate core db, supported are: fs,mem,redis,arakoon, used here'%s'" %
                dbtype)

        # self.systemdb=j.data.kvs.getFSStore("appserversystem",baseDir=self._replaceVar(ini.getValue("systemdb","dbdpath")))

        self.wsport = int(ini.getValue("main", "webserverport"))

        secret = ini.getValue("main", "secret")
        admingroups = ini.getValue("main", "admingroups").split(",")

        # self.filesroot = self._replaceVar(ini.getValue("main", "filesroot"))

        if self.wsport > 0 and inprocess is False:
            self.webserver = j.portal.get(self.wsport, cfgdir=cfgdir, secret=secret, admingroups=admingroups)
        else:
            self.webserver = None

        self._greenLetsPath = j.sal.fs.joinPaths(j.dirs.varDir, "portal_greenlets", self.wsport)
        j.sal.fs.createDir(self._greenLetsPath)
        sys.path.append(self._greenLetsPath)

        self.tcpserver = None
        self.tcpservercmds = {}
        tcpserverport = int(ini.getValue("main", "tcpserverport", default=0))
        if tcpserverport > 0 and inprocess is False:
            self.tcpserver = StreamServer(('0.0.0.0', tcpserverport), self.socketaccept)

        manholeport = int(ini.getValue("main", "manholeport", default=0))
        self.manholeserver = None
        if manholeport > 0 and inprocess is False:
            self.manholeserver = StreamServer(('0.0.0.0', manholeport), self.socketaccept_manhole)

        if inprocess is False and (manholeport > 0 or tcpserverport > 0):
            self.sessions = {}
            self.nrsessions = 0

        # self.messagerouter=MessageRouter()

        # self.logserver=None
        self.logserver_enable = False
        # if logserver==True:
        # self.logserver=StreamServer(('0.0.0.0', 6002), self.socketaccept_log)
        # self.logserver_enable=True
        # elif logserver != None:
        # TODO: configure the logging framework
        # pass

        self.ecserver_enable = False
        # self.ecserver=None #errorconditionserver
        # if ecserver==True:
        # self.ecserver=StreamServer(('0.0.0.0', 6003), self.socketaccept_ec)
        # self.ecserver_enable=True
        # elif ecserver != None:
        # TODO: configure the errorcondition framework
        # pass

        self.signalserver_enable = False
        # self.signalserver=None #signal handling
        # if signalserver==True:
        # self.signalserver=StreamServer(('0.0.0.0', 6004), self.socketaccept_signal)
        # self.signalserver_enable=True
        # elif signalserver != None:
        # TODO: configure the signal framework
        # pass

        self.mainLoop = mainLoop
        j.portal.server.active = self

        self.cfg = ini

        # toload=[]
        self.bootstrap()

        # if self.ismaster:
        #     self.actorsloader.getActor("system", "master")
        #     self.master = j.apps.system.master.extensions.master
        #     # self.master._init()
        #     # self.master.gridmapPrevious=None
        #     # self.master.gridMapSave()
        #     # self.master.gridMapRegisterPortal(self.ismaster,self.ipaddr,self.wsport,self.secret)

        #     # look for nginx & start
        #     #self.startNginxServer()
        #     # self.scheduler = Scheduler()

        # else:
        #     self.master = None
        #     #from JumpScale.core.Shell import ipshellDebug,ipshell
        #     # print "DEBUG NOW not implemented yet in appserver6process, need to connect to other master & master client"
        #     # ipshell()

        self.loadFromConfig()

    def reset(self):
        self.bootstrap()
        self.loadFromConfig()

    def bootstrap(self):
        self.actorsloader.reset()
        self.actorsloader._generateLoadActor("system", "contentmanager", actorpath="system/system__contentmanager/")
        # self.actorsloader._generateLoadActor("system", "master", actorpath="system/system__master/")
        self.actorsloader._generateLoadActor("system", "usermanager", actorpath="system/system__usermanager/")
        self.actorsloader.scan("system")
        self.actorsloader.getActor("system", "usermanager")
        # self.actorsloader.getActor("system", "errorconditionhandler")

        # self.actorsloader._getSystemLoaderForUsersGroups()

    def loadFromConfig(self, reset=False):
        if reset:
            j.core.codegenerator.resetMemNonSystem()
            j.core.specparser.resetMemNonSystem()
            self.webserver.contentdirs = {}

        loader = self.actorsloader
        self.webserver.loadFromConfig4loader(loader, reset)

    def _replaceVar(self, txt):
        # txt = txt.replace("$base", j.dirs.base).replace("\\", "/")
        txt = txt.replace("$appdir", j.sal.fs.getcwd()).replace("\\", "/")
        txt = txt.replace("$vardir", j.dirs.varDir).replace("\\", "/")
        txt = txt.replace("$htmllibdir", j.portal.tools.html.getHtmllibDir()).replace("\\", "/")
        txt = txt.replace("\\", "/")
        return txt

    # def startNginxServer(self):

    #     ini = j.tools.inifile.open("cfg/appserver.cfg")
    #     local = int(ini.getValue("nginx", "local")) == 1

    #     configtemplate = j.sal.fs.fileGetContents(j.sal.fs.joinPaths(j.portal.getConfigTemplatesPath(), "nginx", "appserver_template.conf"))
    #     configtemplate = self._replaceVar(configtemplate)

    #     if local:
    #         varnginx = j.sal.fs.joinPaths(j.dirs.varDir, 'nginx')
    #         j.sal.fs.createDir(varnginx)
    #         if j.system.platformtype.isWindows():

    #             apppath = self._replaceVar(ini.getValue("nginx", "apppath")).replace("\\", "/")

    #             cfgpath = j.sal.fs.joinPaths(apppath, "conf", "sites-enabled", "appserver.conf")
    #             j.sal.fs.writeFile(cfgpath, configtemplate)

    #             apppath2 = j.sal.fs.joinPaths(apppath, "start.bat")
    #             cmd = "%s %s" % (apppath2, apppath)
    #             cmd = cmd.replace("\\", "/").replace("//", "/")

    #             extpath = inspect.getfile(self.__init__)
    #             extpath = j.sal.fs.getDirName(extpath)
    #             maincfg = j.sal.fs.joinPaths(extpath, "configtemplates", "nginx", "nginx.conf")
    #             configtemplate2 = j.sal.fs.fileGetContents(maincfg)
    #             configtemplate2 = self._replaceVar(configtemplate2)
    #             j.sal.fs.writeFile("%s/conf/nginx.conf" % apppath, configtemplate2)

    #             pid = j.system.windows.getPidOfProcess("nginx.exe")
    #             if pid != None:
    #                 j.system.process.kill(pid)

    #             pid = j.system.windows.getPidOfProcess("php-cgi.exe")
    #             if pid != None:
    #                 j.system.process.kill(pid)

    #             j.sal.fs.createDir(j.sal.fs.joinPaths(j.dirs.varDir, "nginx"))

    #             print "start nginx, cmd was %s" % (cmd)
    #             j.system.process.executeAsync(cmd, outputToStdout=False)

    #         else:
    #             j.system.platform.ubuntu.check()

    #             j.sal.fs.remove("/etc/nginx/sites-enabled/default")

    #             cfgpath = j.sal.fs.joinPaths("/etc/nginx/sites-enabled", "appserver.conf")
    #             j.sal.fs.writeFile(cfgpath, configtemplate)

    #             if not j.sal.fs.exists("/etc/nginx/nginx.conf.backup"):
    #                 j.sal.fs.createDir(j.sal.fs.joinPaths(j.dirs.varDir, "nginx"))
    #                 maincfg = j.sal.fs.joinPaths(j.portal.getConfigTemplatesPath(), "nginx", "nginx.conf")
    #                 configtemplate2 = j.sal.fs.fileGetContents(maincfg)
    #                 configtemplate2 = self._replaceVar(configtemplate2)
    #                 j.sal.fs.copyFile("/etc/nginx/nginx.conf", "/etc/nginx/nginx.conf.backup")
    #                 j.sal.fs.writeFile("/etc/nginx/nginx.conf", configtemplate2)
    #                 j.system.process.execute("/etc/init.d/nginx restart")

    #             j.system.process.execute("/etc/init.d/nginx reload")

    #     else:
    #         pass
    #         #raise RuntimeError("only supported in nginx mode")

    def activateActor(self, appname, actor):
        if not "%s_%s" % (appname, actor) in list(self.actors.keys()):
            # need to activate
            result = self.actorsloader.getActor(appname, actor)
            if result is None:
                # there was no actor
                return False

    def addTCPServerCmd(self, cmdName, function):
        self.tcpservercmds[cmdName] = function

    def setTcpServer(self, socketAcceptFunction):
        self.tcpserver = StreamServer(('0.0.0.0', 6000), socketAcceptFunction)

    def _addsession(self, session):
        self.sessions[self.nrsessions] = session
        session.sessionnr = self.nrsessions
        self.nrsessions += 1
        session.ready()
        return self.nrsessions - 1

    # this handler will be run for each incoming connection in a dedicated greenlet
    def socketaccept_manhole(self, socket, address):
        ip, port = address
        socket.sendall('Manhole For Portal Server \n\n')
        session = ManholeSession(ip, port, socket)
        self._addsession(session)
        session.run()

    def socketaccept(self, socket, address):
        ip, port = address
        session = WorkerSession(ip, port, socket)
        self._addsession(session)

    def socketaccept_log(self, socket, address):
        ip, port = address
        session = TCPSessionLog(ip, port, socket)
        self._addsession(session)

    # def socketaccept_ec(self,socket, address):
    #    ip,port=address
    #    session=TCPSessionEC(ip,port,socket)
    #    self._addsession(session)

    # def socketaccept_signal(self,socket, address):
    #    ip,port=address
    #    session=TCPSessionSignal(ip,port,socket)
    #    self._addsession(session)

    def _timer(self):
        """
        will remember time every 1/10 sec
        """
        while True:
            # self.epochbin=struct.pack("I",time.time())
            self.epoch = time.time()
            gevent.sleep(0.1)

    # def _taskSchedulerTimer(self):
    #     """
    #     every 4 seconds check maintenance queue
    #     """
    #     while True:
    #         gevent.sleep(5)
    #         self.scheduler.check(self.epoch)

    def addQGreenlet(self, appName, greenlet):
        """
        """
        if self.webserver is None:
            return
        qGreenletObject = greenlet()
        if qGreenletObject.method == "":
            raise RuntimeError("greenlet class needs to have a method")
        if qGreenletObject.actor == "":
            raise RuntimeError("greenlet class needs to have a actor")

        qGreenletObject.server = self
        self.webserver.addRoute(function=qGreenletObject.wscall,
                                appname=appName,
                                actor=qGreenletObject.actor,
                                method=qGreenletObject.method,
                                paramvalidation=qGreenletObject.paramvalidation,
                                paramdescription=qGreenletObject.paramdescription,
                                paramoptional=qGreenletObject.paramoptional,
                                description=qGreenletObject.description, auth=qGreenletObject.auth)

    def start(self, key=None, reset=False):

        # this is the trigger to start
        print(("STARTING applicationserver on port %s" % self.wsport))

        TIMER = gevent.greenlet.Greenlet(self._timer)
        TIMER.start()

        if self.mainLoop is not None:
            MAINLOOP = gevent.greenlet.Greenlet(self.mainLoop)
            MAINLOOP.start()

        self.started = True

        if self.tcpserver is not None:
            self.tcpserver.start()
        if self.manholeserver is not None:
            self.manholeserver.start()
        if self.logserver_enable == True:
            self.logserver.start()
        if self.ecserver_enable == True:
            self.ecserver.start()
        if self.signalserver_enable == True:
            self.signalserver.start()

        # self.redirectErrors()

        if self.webserver is not None:
            self.webserver.start(reset=reset)

    def processErrorConditionObject(self, eco):
        eco.process()

    def restartInProcess(self, app):
        args = sys.argv[:]
        args.insert(0, sys.executable)
        apppath = j.sal.fs.joinPaths(j.dirs.appDir, app)
        max_fd = 1024
        for fd in range(3, max_fd):
            try:
                flags = fcntl.fcntl(fd, fcntl.F_GETFD)
            except IOError:
                continue
            fcntl.fcntl(fd, fcntl.F_SETFD, flags | fcntl.FD_CLOEXEC)
        os.chdir(apppath)
        os.execv(sys.executable, args)

    # def get(self,appname,actorname):

        # if ini.checkSection("redis"):
        # redisip=ini.getValue("redis","ipaddr")
        # redisport=ini.getValue("redis","port")
        # redisclient=redis.StrictRedis(host=redisip, port=int(redisport), db=0)
        # else:
        # redisclient=None
        # return redisclient

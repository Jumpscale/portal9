import gevent
import sys

import pickle
from js9 import j

from gevent.server import StreamServer

#from MessageRouter import MessageRouter


class TCPSession():

    """
    is the baseclass to do socket handling for the worker or manhole
    """

    def __init__(self, addr, port, socket):
        self.addr = addr
        self.port = port
        self.socket = socket
        self.socket.timeout = 10
        self.active = True
        self.whoami = ""
        self.type = None
        self.sessionnr = 0
        self.dataleftover = ""

    def ready(self):
        print(("%s active %s : %s" % (self.type, self.whoami, self.sessionnr)))

    def read(self):
        print("read classic 4k block & wait")
        return self.socket.recv(4096)

    def kill(self):
        self.fileobj.close()
        self.socket.close()
        print(("kill\n%s" % self))

    def write(self, msg):
        try:
            self.socket.sendall(msg)
        except Exception as e:
            print("failed to send")
            print(e)

    def sendread(self, msg):
        self.write(msg)
        return self.read()

    def __repr__(self):
        s = "type:%s " % self.type
        s += "nr:%s ip:%s port:%s " % (self.sessionnr, self.addr, self.port)
        s += "active:%s " % self.active
        s += "whoami:%s\n" % self.whoami
        return s

    __str__ = __repr__


class WorkerSession(TCPSession):

    def __init__(self, addr, port, socket):
        """
        """
        Session.__init__(self, addr, port, socket)

        dtype, length, epoch, gid, nid, pid, cmd = self.read(False)
        tags = j.data.tags.getObject(cmd)
        self.key = tags.tagGet("key")
        self.whoami = tags.tagGet("whoami")
        if str(tags.tagGet("type")) == "executor":
            self.executor = True  # means is executing commands for us
        else:
            self.executor = False  # means this channel will be used as client connection from worker out
        self.write("OK")
        if out:
            pass
        else:
            self.run()

    def run(self):
        # keeps on checking for incoming messages
        # try:
        while True:
            print("loopstart")
            dtype, length, epoch, gid, nid, pid, data = self.read()
            print("loopend")
            j.portal.tools.server.active.messagerouter.queue(gid, nid, pid, data)

        # except Exception,e:
            # print("read error in appserver6 workergreenlet %s\n" % self.sessionnr
            # print(e
            # gevent.sleep(1)
            # self.kill()

    def read(self, rpc=True):
        """
        @return type,length,epoch,gid,nid,pid,data
        """
        data = self.dataleftover
        while len(data) < 5:
            data += self.socket.recv(4096)

        # length, we are ok
        size = j.core.messagehandler.getMessageSize(data)
        print(("rpc:%s size:%s" % (rpc, size)))

        while len(data) < size:
            print((1))
            data += self.socket.recv(4096)
            print((2))
        dataOut = data[0:size]
        self.dataleftover = data[size:]

        if rpc:
            dtype, length, epoch, gid, nid, pid, data = j.core.messagehandler.unPackMessage(dataOut)
            if dtype == 11:
                data = pickle.loads(data)
        else:
            dtype, length, epoch, gid, nid, pid, data = j.core.messagehandler.unPackMessage(data)

        print(("data:%s" % data))
        return dtype, length, epoch, gid, nid, pid, data

    def ping(self):
        result = self.sendmessage("ping")
        if result != "ping":
            return False
        else:
            return True


class TCPSessionLog(TCPSession):

    def __init__(self, addr, port, socket):
        Session.__init__(self, addr, port, socket)
        self.type = "manhole"

    def run(self):
        while True:
            line = self.read()

    def process(self, line):
        from JumpScale.core.Shell import ipshell
        print("DEBUG NOW logger on tcpsession")
        ipshell()


class ManholeSession(TCPSession):

    def __init__(self, addr, port, socket):
        TCPSession.__init__(self, addr, port, socket)
        self.type = "manhole"
        self.cmds = j.portal.tools.server.active.tcpservercmds
        self.socket.settimeout(None)

    def run(self):

        while True:
            lines = self.read()
            if lines == "":
                continue
            lines = lines.split("\n")
            for line in lines:
                result = self.process(line)
                if result != "" and result is not None:
                    if result[-1] != "\n":
                        result += "\n"
                    # print("***%s*END*"%result
                    self.write(result)

    def read(self):
        return self.socket.recv(4096)

    def process(self, line):
        # print(line
        cmd = line.strip()
        result = """\
commands:
- ping
- killall
- list
"""
        if cmd.find(" ") != -1:
            args = " ".join(cmd.split(" ")[1:])
            cmd = cmd.split(" ")[0]
        else:
            args = ""

        if cmd == "":
            return ""

        if cmd in self.cmds:
            try:
                cmdgreenlet = self.cmds[cmd](cmd, args)
            except Exception as e:
                return "**ERROR** %s" % (str(e).replace("\n", "--"))
            cmdgreenlet.start()
            cmdgreenlet.waiter.wait()
            result = cmdgreenlet.result
            if result is not None:
                result = str(result)
                return result
            return ""

        if cmd == "ipshell":
            from JumpScale.core.Shell import ipshellDebug, ipshell
            print("DEBUG NOW manhole local")
            ipshell()

        # if cmd.find("exec")==0:
            # cmd=cmd[5:]
            # self.sockets

        if cmd.find("ping") == 0:
            cmd = cmd[5:]
            session = self.getsession(int(cmd))
            if session.ping():
                self.write("OK")
            else:
                self.write("Ping failed to %s\n" % session)

        if cmd.find("killall") == 0:
            return self.killallsessions()

        if cmd.find("list") == 0:
            return self.listsessions()

        for key in list(self.cmds.keys()):
            result += "- %s\n" % key

        return result

    def getsession(self, id):
        if id not in j.portal.tools.server.active.sessions:
            self.send("Could not find session with id %s" % id)
            return False
        return j.portal.tools.server.active.sessions[id]

    def killallsessions(self):
        result = ""
        for key in list(j.portal.tools.server.active.sessions.keys()):
            session = j.portal.tools.server.active.sessions[key]
            if session.type != "manhole":
                session.active = False
                session.kill()
                result += "killed %s\n" % session.whoami
        result += "Kill DONE\n"
        return result

    def listsessions(self):
        result = ""
        for key in list(j.portal.tools.server.active.sessions.keys()):
            session = j.portal.tools.server.active.sessions[key]
            result += "%s" % session
        return result

# TODO: don't understand this client, some weird test maybe, can never work


class TCPClient():

    def __init__(self, addr='127.0.0.1', key="1234"):
        self.addr = addr
        self.key = key
        self.init()
        self.dataleftover = ""

    def init(self):
        for t in range(100000):
            if self._init() == True:
                return True
        raise RuntimeError("Connection timed out to master server %s" % addr)

    def _init(self):
        print(("try to connect to %s:%s" % (self.addr, 6000)))
        self.socketout = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socketin = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.sender.settimeout(2)
        dataout = 'type:executor whoami:%s key:%s' % (j.application.whoAmI, self.key)
        msgout = j.core.messagehandler.data2Message(20, dataout)
        datain = 'type:client whoami:%s key:%s' % (j.application.whoAmI, self.key)
        msgin = j.core.messagehandler.data2Message(20, datain)

        try:
            self.socketout.connect((self.addr, 6000))
            self.socketin.connect((self.addr, 6000))
            # try to init the out channel
            self.socketout.sendall(msgout)
            if self.socketout.recv(2) != "OK":
                raise RuntimeError("bad result, could not connect the out channel")
            # try to init the in channel
            self.socketin.sendall(msgin)
            if self.socketin.recv(2) != "OK":
                raise RuntimeError("bad result")

        except Exception as e:
            print(e)
            try:
                self.socketout.close()
                self.socketin.close()
            except:
                pass
            time.sleep(5)
            return False
        print("connected")
        return True

    def sendcmd(self, appName, actorName, instance, method, params, timeout=0, sync=True):
        msg = j.core.messagehandler.getRPCMessage(appName, actorName, instance, method, params, timeout, sync)
        self.send(msg)
        print("sent")
        return self.read()

    def read(self):
        """
        @return type,length,epoch,gid,nid,pid,data
        """
        data = self.dataleftover
        while len(data) < 5:
            data += self.socket.recv(4096)

        # length, we are ok
        size = j.core.messagehandler.getMessageSize(data)
        while len(data) < size:
            data += self.socket.recv(4096)
        dataOut = data[0:size]
        self.dataleftover = data[size:]

        dtype, length, epoch, gid, nid, pid, data = j.core.messagehandler.unPackMessage(dataOut)

        if dtype == 11:
            data = pickle.loads(data)

        return type, length, epoch, gid, nid, pid, data

    def process(self, line):
        print(line)

    def send(self, message, maxtry=10):
        run = 1
        while run < maxtry:
            try:
                self.socket.sendall(message)
                return True
            except Exception as e:
                self._init()
        raise RuntimeError("could not send message, could not reach after %s times" % maxtry)

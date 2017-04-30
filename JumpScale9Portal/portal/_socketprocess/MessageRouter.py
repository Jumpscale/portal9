import gevent
from gevent import queue
from js9 import j


class MessageRouter(gevent.Greenlet):

    def __init__(self):
        """
        this is the class which knows how to work with messages
        """
        self.actors = {}  # key = app_actor_instanceid #value=ActorQueues

    def queue(self, gid, nid, pid, message):
        """
        @param if only 1 instance use 0
        """
        key = "%s_%s_%s_%s" % (message["app"], message["actor"], message["inst"], message["method"])
        if key not in self.actors:
            self.actors[key] = ActorMethodQueue(gid, nid, pid, message["app"], message["actor"],
                                                message["inst"], message["method"])
            self.actors[key].start()
        message = Message(message)
        self.actors[key].queue(message)

    def watchdog(self):
        return

    def start(self):
        print("messagerouter started")
        while True:
            watchdog()
            gevent.sleep(1)


class ActorMethodQueue(gevent.Greenlet):

    def __init__(self, gid, nid, pid, appname, actorname, instance, methodname):
        self.gid = gid
        self.nid = nid
        self.pid = pid
        self.appname = appname
        self.actorname = actorname
        self.instance = instance
        self.methodname = methodname

        self.methodQueueToActor = queue.Queue()
        self.methodQueueFromActor = queue.Queue()

    def queue(self, message):
        self.methodQueueToActor.put(message)
        print("queue message")

    def processQueues(self):
        print("process queue")
        #from JumpScale.core.Shell import ipshellDebug,ipshell
        # print("DEBUG NOW queue"
        # ipshell()

    def start(self):
        print(("actor queue for %s %s %s %s %s %s %s" % (self.gid, self.nid, self.pid, self.appname, self.actorname,
                                                         self.instance, self.methodname)))
        while True:
            self.processQueues()
            gevent.sleep(1)


class Message():

    """
    this holds all usefull information about a message which goes to an actor
    """

    def __init__(self, messagedata):
        self.messagedata = messagedata
        self.starttime = j.portal.server.active.epoch
        self.timedout = False
        self.jobid = jobid
        self.caller = None
        self.state = "W"  # values are WAITING,TIMEOUT, RUNNING, ERROR,DONE (always first letter)
        self.result = None
        self.resultcode = 4
        self.event = AsyncResult()
        self.sync = sync

    def __str__(self):
        out = "%s %s %s" % (self.taskid, self.state, self.starttime)
        return out

    def __repr__(self):
        return self.__str__()

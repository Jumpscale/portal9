from js9 import j
from JumpScale9Portal.portal import exceptions
import gevent
import json


EVENTKEY = 'events.data.%s'
EVENTCOUNT = 'events.count'
SESSIONKEY = 'events.session.'


class Events(object):
    GETS = {}

    def __init__(self, ctx):
        self.redis = j.core.db
        self.ctx = ctx
        self.eventstreamid = j.data.idgenerator.generateGUID()

    def get(self, cursor):
        head = int(self.redis.get(EVENTCOUNT) or 0)
        if cursor <= 0 or cursor < head - 100 or cursor > head + 1:
            cursor = head + 1
        if cursor < head:
            # find first available queue or head
            while not self.redis.exists(self.redis.getQueue(EVENTKEY % cursor).key) and cursor < head + 1:
                cursor += 1

        event = self.redis.getQueue(EVENTKEY % cursor).fetch(timeout=50)
        if not event:
            return {'event': None, 'cursor': cursor}
        else:
            cursor += 1
            return {'event': json.loads(event.decode('utf8')), 'cursor': cursor}

    def sendMessage(self, title, text, level='info', **kwargs):
        msg = {'eventtype': 'message',
               'title': title,
               'text': text,
               'type': level,
               'eventstreamid': self.eventstreamid}
        if kwargs:
            msg.update(kwargs)
        self.sendEvent(msg)

    def sendEvent(self, event):
        count = self.redis.incr(EVENTCOUNT)
        queue = self.redis.getQueue(EVENTKEY % count)
        queue.put(json.dumps(event))
        queue.set_expire(60)

        # delete tail
        qkey = self.redis.getQueue(EVENTKEY % (count - 100)).key
        self.redis.delete(qkey)

    def runAsync(self, func, args, kwargs, title, success, error, errorcb=None, successcb=None):
        def runner():
            try:
                func(*args, **kwargs)
            except (Exception, exceptions.BaseError) as e:
                eco = j.errorhandler.processPythonExceptionObject(e)
                if errorcb:
                    try:
                        errorcb(eco)
                    except:
                        pass
                print(eco)
                errormsg = error + "</br> For more info check <a href='/system/error condition?id=%s'>error</a> details" % eco.guid
                self.sendMessage(title, errormsg, 'error', hide=False)
                return
            refreshhint = self.ctx.env.get('HTTP_REFERER')
            self.sendMessage(title, success, 'success', refresh_hint=refreshhint)
            if successcb:
                successcb()
        self.sendMessage(title, 'Started')
        gevent.spawn(runner)

    def waitForJob(self, job, success, error, title=None):
        gevent.spawn(self._waitForJob, job, success, error, title)

    def _waitForJob(self, job, success, error, title):
        title = title or 'Job Info'
        acl = j.clients.agentcontroller.get()
        job = acl.waitJumpscript(job=job)
        if job['state'] != 'OK':
            error += "</br> For more info check <a href='/grid/job?id=%(guid)s'>job</a> details" % job
            self.sendMessage(title, error, 'error', hide=False)
        else:
            refreshhint = self.ctx.env.get('HTTP_REFERER')
            self.sendMessage(title, success, 'success', refresh_hint=refreshhint)

from js9 import j
import time


class system_webhooks(j.tools.code.classGetBase()):

    """
    """

    def __init__(self):
        pass

        self._te = {}
        self.actorname = "webhooks"
        self.appname = "system"
        # system_atyourservice_osis.__init__(self)

    def github(self, payload, ctx, **kwargs):
        """
        param:payload
        result json
        """
        environ = ctx.env
        key = '%s.%s.%s' % (environ.get('HTTP_X_GITHUB_EVENT'), environ.get(
            'HTTP_X_GITHUB_DELIVERY'), j.data.time.epoch)
        j.core.db.hset('webhooks', key, payload)
        return True

    def mandrill(self, mandrill_events, **kwargs):
        """
        param:mandrill_events
        result json
        """
        messages = j.data.serializer.json.loads(mandrill_events)
        dir = j.sal.fs.joinPaths(j.dirs.varDir, 'email')

        for message in messages:
            ts = time.gmtime(message['ts'])
            # we generate a random guid to avoid ts conflict if 2 or more
            # messages are received with the same timestamp. We also don't
            # only use the guid, so we don't lose the time information
            key = "%s-%s" (message['ts'], j.data.idgenerator.generateGUID())
            path = j.sal.fs.joinPaths(dir, ts.tm_year, ts.tm_mon, ts.tm_mday)
            j.sal.fs.createDir(path)
            msg = message['msg']
            j.sal.fs.writeFile(j.sal.fs.joinPaths(path, key), j.data.serializer.json.dumps(msg))

            # set the email hset, and push key to queue, but we keep only meta information
            for k in ('raw_msg', 'headers', 'text', 'html', 'attachments', 'images', 'spam_report'):
                msg.pop(k, None)

            j.core.db.hset('mails', key, j.data.serializer.json.dumps(msg))
            j.core.db.rpush('mails.queue', key)

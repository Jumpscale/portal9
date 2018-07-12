from js9 import j
import json


class ErrorHandler:
    def __init__(self):
        self.logger = j.logger.get('errorhandler')
        j.errorhandler.escalateToRedis = True
        if j.core.db.__module__ == 'fakeredis':
            j.clients.redis.core_get()


    def start(self):
        while True:
            res = j.core.db.blpop('queues:eco')
            if res:
                _, ecoid = res
                ecostring = j.core.db.hget('eco:objects', ecoid)
                if ecostring:
                    try:
                        eco = json.loads(ecostring.decode())
                    except Exception as e:
                        self.logger.error(e)
                        # don't escalate cause we might get in error loop
                        continue
                    ecoobj = j.portal.tools.models.system.Errorcondition.objects(uniquekey=eco['uniquekey']).first()
                    if ecoobj:
                        ecoobj.update(inc__occurrences=1, errormessage=eco['errormessage'], lasttime=eco['lasttime'])
                    else:
                        j.portal.tools.models.system.Errorcondition(
                            pid=eco['pid'],
                            uniquekey=eco['uniquekey'],
                            jid=eco['jid'],
                            masterjid=eco['masterjid'],
                            appname=eco['appname'],
                            level=eco['level'],
                            type=eco['type'],
                            state=eco['state'],
                            errormessage=eco['errormessage'],
                            errormessagePub=eco['errormessagePub'],
                            category=eco['category'],
                            tags=eco['tags'],
                            code=eco['code'],
                            funcname=eco['funcname'],
                            funcfilename=eco['funcfilename'],
                            funclinenr=eco['funclinenr'],
                            backtrace=eco['_traceback'],
                            lasttime=eco['lasttime'],
                            closetime=eco['closetime'],
                            occurrences=eco['occurrences']
                        ).save()


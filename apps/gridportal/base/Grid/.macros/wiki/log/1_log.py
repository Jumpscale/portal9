import datetime

def main(j, args, params, tags, tasklet):
    id = args.getTag('id')
    if not id:
        out = 'Missing log id param "id"'
        params.result = (out, args.doc)
        return params
    log = j.apps.system.gridmanager.getLogs(id=id)
    if not log:
        params.result = ('Log with id %s not found' % id, args.doc)
        return params
    log = log.to_dict()

    def objFetchManipulate(id):
        for attr in ['epoch']:
            log[attr] = datetime.datetime.fromtimestamp(log[attr]).strftime('%Y-%m-%d %H:%M:%S')
        for attr in ['jid', 'masterjid']:
            log['jid'] = '[%(jid)s|job?id=%(jid)s]|' % log if log[attr] else 'N/A'
        return log
    push2doc=j.portal.tools.macrohelper.push2doc

    return push2doc(args,params,objFetchManipulate)


def match(j, args, params, tags, tasklet):
    return True

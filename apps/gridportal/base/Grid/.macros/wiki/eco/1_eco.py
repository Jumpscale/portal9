import datetime

def main(j, args, params, tags, tasklet):
    id = args.getTag('id')
    if not id:
        out = 'Missing ECO id param "id"'
        params.result = (out, args.doc)
        return params

    obj = j.apps.system.gridmanager.getErrorconditions(id=id)
    if not obj:
            params.result = ('Could not find Error Condition Object with id %s' % id, args.doc)
            return params
    obj = obj.to_dict()

    obj['epoch'] = j.data.time.epoch2HRDateTime(obj['epoch'])
    obj['lasttime'] = j.data.time.epoch2HRDateTime(obj['lasttime'])
    for attr in ['errormessage', 'errormessagePub']:
        obj[attr] = j.portal.tools.html.escape(obj[attr])
    for attr in ['jid']:
        obj['jid'] = '[%(jid)s|job?id=%(jid)s]|' % obj if obj[attr] != 0 else 'N/A'
    obj['id'] = id

    args.doc.applyTemplate(obj)
    params.result = (args.doc, args.doc)
    return params

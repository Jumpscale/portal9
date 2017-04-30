import yaml
import datetime

def main(j, args, params, tags, tasklet):
    id = args.getTag('id')
    if not id:
        out = "No ID given for audit"
        params.result = (out, args.doc)
        return params

    audit = j.apps.system.gridmanager.getAudits(id=id)
    if not audit:
        out = "No audit with id %s exists" % id
        params.result = (out, args.doc)
        return params

    audit = audit.to_dict()
    for key in ('kwargs', 'args', 'result'):
        audit[key] = yaml.dump(j.data.serializer.json.loads(audit[key])).replace("!!python/unicode ", "")

    audit['time'] = datetime.datetime.fromtimestamp(audit['timestamp']).strftime('%m-%d %H:%M:%S') or 'N/A'

    args.doc.applyTemplate(audit)
    params.result = (args.doc, args.doc)
    return params

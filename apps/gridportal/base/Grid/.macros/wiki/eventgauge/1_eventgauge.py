import datetime
import time

def main(j, args, params, tags, tasklet):
    doc = args.doc
    id = args.getTag('id')
    width = args.getTag('width')
    height = args.getTag('height')
    result = "{{jgauge width:%(width)s id:%(id)s height:%(height)s val:%(last24h)s start:0 end:%(total)s}}"
    now = datetime.datetime.now()

    firsteco = j.apps.system.gridmanager.getErrorconditions(from_='-7d')
    total = len(firsteco)

    current = len(j.apps.system.gridmanager.getErrorconditions(from_='-1d'))
    average = total

    if firsteco:
        date = datetime.datetime.fromtimestamp(firsteco[0]['lasttime'])
        delta = now - date
        if delta.days != 0:
            average = int(total / delta.days) * 2

    if average < current:
        average = current

    result = result % {'height': height,
                       'width': width,
                       'id': id,
                       'last24h': current,
                       'total': average}
    params.result = (result, doc)
    return params

def match(j, args, params, tags, tasklet):
    return True


def main(j, args, params, tags, tasklet):
    id = args.getTag('id')
    if not id:
        out = 'Missing alert param "id"'
        params.result = (out, args.doc)
        return params            

    alert = j.apps.system.gridmanager.getAlerts(id=id)
    if not alert:
        params.result = ('Alert with id %s not found' % id, args.doc)
        return params

    color = 'green' if alert['state'] in ['RESOLVED', 'CLOSED'] else ('red' if alert['state'] in ['ALERT', 'UNRESOLVED'] else 'orange')
    alert['state'] = '{color:%s}%s{color}' % (color, alert['state'])


    ecos_id = alert['errorconditions']

    for eco in ecos_id:
        if not j.data.model.Errorcondition.exists(eco):
            alert['errorconditions'] = None

    args.doc.applyTemplate(alert)

    params.result = (args.doc, args.doc)
    return params
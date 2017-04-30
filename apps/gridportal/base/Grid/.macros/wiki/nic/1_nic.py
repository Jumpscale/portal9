import datetime

def main(j, args, params, tags, tasklet):
    id = args.getTag('id')
    if not id:
        out = 'Missing NIC id param "id"'
        params.result = (out, args.doc)
        return params
    nic = j.apps.system.gridmanager.getNics(id=id)
    if not nic:
        params.result = ('NIC with id %s not found' % id, args.doc)
        return params

    nic = nic.to_dict()
    node = j.apps.system.gridmanager.getNodes(nid=nic['nid'])
    nic['lastcheck'] = datetime.datetime.fromtimestamp(nic['lastcheck']).strftime('%Y-%m-%d %H:%M:%S')
    nic['ipaddr'] = ', '.join([str(x) for x in nic['ipaddr']])
    nic['nodename'] = node[0]['name']

    args.doc.applyTemplate(nic)
    params.result = (args.doc, args.doc)
    return params

def match(j, args, params, tags, tasklet):
    return True

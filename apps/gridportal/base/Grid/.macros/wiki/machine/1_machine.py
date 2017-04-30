import datetime

def main(j, args, params, tags, tasklet):
    id = args.getTag('id')
    if not id:
        out = 'Missing machine id param "id"'
        params.result = (out, args.doc)
        return params
    machine = j.apps.system.gridmanager.getMachines(id=id)
    if not machine:
        params.result = ('Machine with id %s not found' % id, args.doc)
        return params

    machine = machine.to_dict()
    obj = machine
    for attr in ['roles', 'ipaddr']:
        obj[attr] = ', '.join([str(x) for x in obj[attr]]) 

    netaddr = obj['netaddr']
    netinfo = ''
    for k, v in netaddr.items():
        netinfo += 'mac address: %s, interface: %s, ip: %s<br>' % (k, v[0], v[1])
    obj['netaddr'] = netinfo

    obj['lastcheck'] = datetime.datetime.fromtimestamp(obj['lastcheck']).strftime('%Y-%m-%d %H:%M:%S')
    args.doc.applyTemplate(obj)
    params.result = (args.doc, args.doc)
    return params

def match(j, args, params, tags, tasklet):
    return True

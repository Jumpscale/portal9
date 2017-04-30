def main(j, args, params, tags, tasklet):

    #macro puts obj info as params on doc, when show used as label, shows the content of the obj in nicely structured code block
    nid = args.getTag('nid')
    gid = args.getTag('gid')
    id = args.getTag('id')
    if not nid or not gid:
        params.result = ('Node "nid" and "gid" must be passed.', args.doc)
        return params
    gid = int(gid)
    nid = int(nid)

    node = j.apps.system.gridmanager.getNodes(gid=gid, nid=nid)
    grid = j.apps.system.gridmanager.getGrids()
    if grid:
        grid = grid[0].to_dict()
    if not node:
        params.result = ('Node with and gid %s and nid %s not found' % (gid, nid), args.doc)
        return params

    node = node[0].to_dict()

    #obj is a dict
    node["ipaddr"]=", ".join(node["ipaddr"])
    node["roles"]=", ".join(node["roles"])

    r=""
    for netitem in node["netaddr"]:
        dev = netitem['name']
        ip = netitem['ip']
        mac = netitem['mac']
        r+="|%-15s | %-20s | %s| \n"%(dev,mac,ip)

    node["netaddr"]=r
    node['gridname'] = grid['name']
    node['nodename'] = node['name']

    args.doc.applyTemplate(node)
    params.result = (args.doc, args.doc)
    return params


def match(j, args, params, tags, tasklet):
    return True



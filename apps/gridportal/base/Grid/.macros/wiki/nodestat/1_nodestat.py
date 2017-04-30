
def main(j, args, params, tags, tasklet):
    params.merge(args)

    doc = params.doc

    nid = args.getTag('nid')
    width = args.getTag('width', 800)
    height = args.getTag('height', 400)

    if not nid:
        out = 'Missing node id param "id"'
        params.result = (out, doc)
        return params

    _data = {'nid': nid, 'height':height, 'width':width}

    cpustats = args.tags.labelExists("cpustats")
    netstats = args.tags.labelExists("netstats")
    memstats = args.tags.labelExists("memstats")

    out = ''

    if cpustats:
        out += '\nh3. CPU Statistics\n'
        out += '|| || ||\n'
        
        out += '|{{stat key:n%(nid)s.system.cpu.percent&title=CPU%%20Percent&areaMode=stacked&yMax=100 width:%(width)s height:%(height)s}}|{{stat key:n%(nid)s.system.cpu.time.system,n%(nid)s.system.cpu.time.user,n%(nid)s.system.cpu.time.iowait,n%(nid)s.system.cpu.time.idle&title=CPU%%20Time&graphType=pie width:%(width)s height:%(height)s}}|\n' % _data

    if memstats:
        out += '\nh3. Memory Statistics\n'
        out += '{{stat key:n%(nid)s.system.memory.percent&areaMode=stacked&yMax=100 width:%(width)s height:%(height)s}}<br><br>' % _data

    if netstats:
        out += '\nh3. Network Statistics\n'
        out += '|| || ||\n'
        
        out += '|{{stat key:n%(nid)s.system.network.kbytes.recv,n%(nid)s.system.network.kbytes.send&title=KBytes width:%(width)s height:%(height)s}}|{{stat key:n%(nid)s.system.network.packets.recv,n%(nid)s.system.network.packets.send&title=Packets width:%(width)s height:%(height)s}}|\n' % _data

        out += '|{{stat key:n%(nid)s.system.network.drop.in,n%(nid)s.system.network.drop.out&title=Drop width:%(width)s height:%(height)s}}|{{stat key:n%(nid)s.system.network.error.in,n%(nid)s.system.network.error.out&title=Error width:%(width)s height:%(height)s}}|\n' % _data

    params.result = (out, doc)

    return params


def match(j, args, params, tags, tasklet):
    return True

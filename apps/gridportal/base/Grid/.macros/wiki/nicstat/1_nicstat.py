def main(j, args, params, tags, tasklet):
    params.merge(args)

    doc = params.doc

    nid = args.getTag('nid')
    width = args.getTag('width', 800)
    height = args.getTag('height', 400)
    nic = args.getTag('nic')

    out = ''
    missing = False

    for k,v in {'nid':nid, 'nic':nic}.items():
        if not v:
            out += 'Missing param %s.\n' % k
            missing = True
    
    if not missing:            
        _data = {'nid': nid, 'height':height, 'width':width, 'nic': nic}
        
        out += '\nh3. Statistics\n'
        out += '|| || ||\n'
        out += '|{{stat key:n%(nid)s.nic.%(nic)s.kbytes_recv,n%(nid)s.nic.%(nic)s.kbytes_sent&title=KBytes width:%(width)s height:%(height)s}}|{{stat key:n%(nid)s.nic.%(nic)s.packets_recv,n%(nid)s.nic.%(nic)s.packets_sent&title=Packets width:%(width)s height:%(height)s}}|\n' % _data

        out += '|{{stat key:n%(nid)s.nic.%(nic)s.dropin,n%(nid)s.nic.%(nic)s.dropout&title=Drop width:%(width)s height:%(height)s}}|{{stat key:n%(nid)s.nic.%(nic)s.errin,n%(nid)s.nic.%(nic)s.errout&title=Error width:%(width)s height:%(height)s}}|\n' % _data


    params.result = (out, doc)

    return params


def match(j, args, params, tags, tasklet):
    return True

import datetime

def main(j, args, params, tags, tasklet):
    id = args.getTag('id')
    gid = args.getTag('gid')
    if not id or not gid:
        out = 'Missing vdisk id'
        params.result = (out, args.doc)
        return params

    vdisk = j.apps.system.gridmanager.getVDisks(id=id)
    if not vdisk:
        params.result = ('VDisk with id %s not found' % id, args.doc)
        return params

    def objFetchManipulate(id):
        obj = vdisk.to_dict()
        for attr in ['lastcheck', 'expiration', 'backuptime']:
            value = obj.get(attr)
            if value: 
                obj[attr] = datetime.datetime.fromtimestamp(value).strftime('%Y-%m-%d %H:%M:%S')
            else:
                obj[attr] = 'N/A'
        for attr in ['size', 'free', 'sizeondisk']:
            size, unit = j.data.units.bytes.converToBestUnit(obj[attr], 'K')
            if unit:
                unit += "i"
            obj[attr] = "%s %sB" % (size, unit)
        return obj

    push2doc=j.portal.tools.macrohelper.push2doc

    return push2doc(args,params,objFetchManipulate)

def match(j, args, params, tags, tasklet):
    return True

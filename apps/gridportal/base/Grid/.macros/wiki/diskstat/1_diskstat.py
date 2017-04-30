
def main(j, args, params, tags, tasklet):
    params.merge(args)
    id = args.getTag('id')
    
    if not id:
        return params

    disk = j.apps.system.gridmanager.getDisks(id=id)

    if not disk:
        return params

    def objFetchManipulate(id):
        obj = disk.to_dict()
        name = obj['path'].replace('/dev/', '')
        diskkey = 'n%s.disk.%s' % (obj['nid'], name)
        obj['diskkey'] = diskkey
        return obj

    push2doc=j.portal.tools.macrohelper.push2doc

    return push2doc(args,params,objFetchManipulate)
def match(j, args, params, tags, tasklet):
    return True

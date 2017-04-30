def main(j, args, params, tags, tasklet):
    params.merge(args)

    id = args.getTag('id')
    if not id:
        return params

    process = j.apps.system.gridmanager.getProcesses(id=id)
    if not process:
        return params

    def objFetchManipulate(id):
        obj = process.to_dict()
        prockey = "n%s.process.%%s.%%s" % obj['nid']
        if obj['type'] == 'jsprocess':
            obj['prockey'] = prockey % ('js', "%s_%s" % (obj['aysdomain'], obj['sname']))
        else:
            obj['prockey'] = prockey % ('os', "%s" % (obj['pname']))
        return obj

    push2doc=j.portal.tools.macrohelper.push2doc

    return push2doc(args,params,objFetchManipulate)

def match(j, args, params, tags, tasklet):
    return True
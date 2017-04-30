def main(j, args, params, tags, tasklet):
    doc = args.doc

    dbdata = j.core.grid.healthchecker.checkDBs()
    out = list()
    results = list()
    for result in dbdata:
        results.append(result)
    for noderesults in results:
        for nid, result in sorted(noderesults.items()):
            for category, data in result.items():
                 status = ''
                 out.append('h5. %s' % category)
                 for dataitem in data:
                    if isinstance(dataitem, dict):
                        if dataitem.get('state'):
                            status = j.core.grid.healthchecker.getWikiStatus(dataitem.get('state'))
                        if dataitem.get('message'):
                            message = dataitem.get('message', '')
                            out.append('|%s |%s |' % (message, status))
                    else:
                        out.append(dataitem)

    out = '\n'.join(out)
    params.result = (out, doc)
    return params

def match(j, args, params, tags, tasklet):
    return True

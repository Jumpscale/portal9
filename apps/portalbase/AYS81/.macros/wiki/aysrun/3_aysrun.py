

def main(j, args, params, tags, tasklet):
    arg_repo = args.getTag('repo')
    arg_runid = args.getTag('runid')

    repo = j.core.atyourservice.repoGet(arg_repo)
    runmodel = repo.runGet(runkey=arg_runid)
    if runmodel:
        import datetime
        data = runmodel.dictFiltered
        data['lastModDate'] = datetime.datetime.fromtimestamp(data['lastModDate']).strftime('%Y-%m-%d %H:%M:%S.%f')
        args.doc.applyTemplate({'run': runmodel, 'data': data, 'reponame': repo.name})
    else:
        args.doc.applyTemplate({'error': 'No run found'})

    params.result = (args.doc, args.doc)
    return params

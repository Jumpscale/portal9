

def main(j, args, params, tags, tasklet):
    try:
        reponame = args.getTag('reponame')
        runid = args.getTag('runid')

        ctx = args.requestContext
        aysactor = j.apps.actorsloader.getActor('system', 'atyourservice')
        client = aysactor.get_client(ctx=ctx)

        run = client.getRun(runid, reponame).json()
        if run:
            args.doc.applyTemplate({'run': run, 'reponame': reponame})
        else:
            args.doc.applyTemplate({'error': 'No run found'})
    except Exception as e:
        args.doc.applyTemplate({'error': e.__str__()})

    params.result = (args.doc, args.doc)
    return params



def main(j, args, params, tags, tasklet):
    try:
        reponame = args.getTag('reponame') or ''
        ctx = args.requestContext
        aysactor = j.apps.actorsloader.getActor('system', 'atyourservice')
        client = aysactor.get_client(ctx=ctx)

        services = client.listServices(reponame).json()
        args.doc.applyTemplate({'services': services, 'reponame': reponame})
    except Exception as e:
        args.doc.applyTemplate({'error': str(e)})

    params.result = (args.doc, args.doc)

    return params

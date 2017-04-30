

def main(j, args, params, tags, tasklet):
    doc = args.doc
    ayspath = args.getTag('ayspath') or ''
    params.merge(args)

    # actor = j.apps.actorsloader.getActor("ays81", "atyourservice")
    repo = j.core.atyourservice.repoGet(ayspath)
    out = []
    try:
        # for _, services in actor.listServices(ayspath, ctx=args.requestContext).items():
            # out.extend(services)
        services = repo.services
        args.doc.applyTemplate({'services': services, 'reponame': j.sal.fs.getBaseName(ayspath)})
    except Exception as e:
        args.doc.applyTemplate({'error': str(e)})

    params.result = (args.doc, args.doc)

    return params

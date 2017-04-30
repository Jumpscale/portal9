

def main(j, args, params, tags, tasklet):
    try:
        repos = j.core.atyourservice.reposList()
        # repos = j.apps.ays81.atyourservice.listRepos(ctx=args.requestContext)
        args.doc.applyTemplate({'repos': repos})
    except Exception as e:
        args.doc.applyTemplate({'error': str(e)})

    params.result = (args.doc, args.doc)
    return params



def main(j, args, params, tags, tasklet):
    try:
        reponame = args.getTag('reponame')
        runid = args.getTag('runid')
        ctx = args.requestContext
        aysactor = j.apps.actorsloader.getActor('system', 'atyourservice')
        client = aysactor.get_client(ctx=ctx)

        run = client.getRun(runid, reponame).json()
        # import ipdb; ipdb.set_trace()
        runstate = run['state']
        runkey = run['key']
        beakercookie = ctx.env['HTTP_COOKIE']

        headers = ""

        # production = False
        # authheader = ""
        # cfg = j.application.instanceconfig
        # if isinstance(cfg, dict):
        #     # need to upgrade config
        #     production = cfg.get('production', False)
        # if production:
        #     jwt = ctx.env['beaker.session'].get('oauth', None)
        #     authheader = '"Authorization": "Bearer: {jwt}"'.format(jwt) if jwt else ""
        #     headers = """
        #       headers: {{
        #         {authheader}
        #       }},
        #     """.format(authheader)

        if run:
            args.doc.applyTemplate({'run': run, 'bearercookie': beakercookie, 'reponame': reponame, 'runkey': runkey, 'runstate': runstate, 'headers': headers})
        else:
            args.doc.applyTemplate({'error': 'No run found'})
    except Exception as e:
        args.doc.applyTemplate({'error': e.__str__()})

    params.result = (args.doc, args.doc)
    return params

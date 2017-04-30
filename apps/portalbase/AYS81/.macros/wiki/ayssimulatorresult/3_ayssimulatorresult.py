from collections import OrderedDict

def main(j, args, params, tags, tasklet):
    query_params = args.requestContext.params
    repo = query_params.get('reponame', None)
    repopath = query_params.get('repo', None)

    actor = j.apps.actorsloader.getActor("system", "atyourservice")
    out = ""
    out = "h3. Result of simulation for repository %s \n" % repo
    try:
        run = actor.simulate(repositorypath=repopath, ctx=args.requestContext)
        out += "{{code: " + str(run) + " }}"
        
    except Exception as e:
        out.append(str(e))

    params.result = out, args.doc
    return params

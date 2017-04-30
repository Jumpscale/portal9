def main(j, args, params, tags, tasklet):
    doc = args.doc
    out = []
    account = tags.tagGet('account')
    repo = tags.tagGet('repo')
    provider = tags.tagGet('provider')

    # First try to get the version/branch from the build.xml if it is exists
    # this mean you are on a mounted file system
    # if not get them from the repo itself

    cuisine = j.tools.cuisine.local
    cfg_path = cuisine.core.args_replace("$optDir/build.yaml")
    if cuisine.core.file_exists(cfg_path):
        config = j.data.serializer.yaml.loads(cuisine.core.file_read(cfg_path))
        if repo == 'jumpscale_core8':
            repo = 'jumpscale'
        elif repo == 'jumpscale_portal8':
            repo = 'portal'
        elif repo == 'jscockpit':
            repo = 'cockpit'
        if repo in config:
            out.append(config[repo])
    else:
        path = j.do.getGitReposListLocal(provider, account, repo).get(repo)
        if path:
            branch = j.clients.git.get(path).describe()[1]
            out.append(branch)

    out = '\n'.join(out)

    params.result = (out, doc)
    return params

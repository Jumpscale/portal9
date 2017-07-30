def main(j, args, params, tags, tasklet):
    try:
        doc = args.doc
        out = []
        account = tags.tagGet('account')
        repo = tags.tagGet('repo')
        provider = tags.tagGet('provider')

        # First try to get the version/branch from the build.xml if it is exists
        # this mean you are on a mounted file system
        # if not get them from the repo itself

        cfg_path = j.sal.fs.joinPaths(j.dirs.BASEDIR, "build.yaml")
        if j.sal.fs.exists(cfg_path):
            config = j.data.serializer.yaml.loads(j.sal.fs.fileGetContents(cfg_path))
            if repo == 'jumpscale_core8':
                repo = 'jumpscale'
            elif repo == 'jumpscale_portal8':
                repo = 'portal'
            elif repo == 'jscockpit':
                repo = 'cockpit'
            if repo in config:
                out.append(config[repo])
        else:
            path = j.clients.git.getGitReposListLocal(provider, account, repo).get(repo)
            if path:
                branch = j.clients.git.get(path).describe()[1]
                out.append(branch)

        out = '\n'.join(out)
    except Exception as e:
        out.append(str(e))

    params.result = (out, doc)
    return params

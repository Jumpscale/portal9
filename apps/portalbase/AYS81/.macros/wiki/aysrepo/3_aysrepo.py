

def main(j, args, params, tags, tasklet):
    arg_repo = args.getTag('repo')
    reponame = j.sal.fs.getBaseName(arg_repo)
    repos = j.core.atyourservice.reposList()
    repo = None
    for r in repos:
        if reponame == r.name:
            repo = r
            break

    if repo is not None:
        repo.path = repo.path.replace(j.dirs.codeDir, '$codedir')
        repo.path = repo.path.replace(j.dirs.varDir, '$varDir')
        args.doc.applyTemplate({'repo': repo})
        params.result = (args.doc, args.doc)
    else:
        params.result = ("Cant find repository %s" % repo, args.doc)
    return params

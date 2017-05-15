def main(j, args, params, tags, tasklet):
    print('hello world')
    import time
    params.merge(args)
    doc = params.doc
    tags = params.tags.getDict()
    spacename = params.paramsExtra['space']
    out = ""
    logdir = j.portal.tools.server.active.logdir
    backupdir = j.sal.fs.joinPaths(logdir, 'backup')
    if 'filename' in list(tags.keys()):
        filen = tags['filename']
        if not j.sal.fs.exists(backupdir):
            j.sal.fs.createDir(backupdir)
        originalfile = j.sal.fs.joinPaths(logdir, filen)
        destfile = j.sal.fs.joinPaths(backupdir, "%s_%s" % (time.ctime(), filen))
        j.sal.fs.copyFile(originalfile, destfile)
        j.sal.fs.writeFile(originalfile, "")

    spaces = j.portal.tools.server.active.getSpaces()
    if spacename in spaces:
        sp = j.portal.tools.server.active.getSpace(spacename)
    else:
        params.result = (out, params.doc)
        return params
    if spacename == 'system':
        logfiles = j.sal.fs.listFilesInDir(logdir)
    else:
        logfiles = j.sal.fs.joinPaths(logdir, 'space_%s.log') % spacename
    for lfile in logfiles:
        baselfile = j.sal.fs.getBaseName(lfile)
        out += "|%s | [Reset | /system/ResetAccessLog?filename=%s] | [Show | system/ShowSpaceAccessLog?filename=%s]|\n" % (
            baselfile, baselfile, baselfile)

    params.result = (out, params.doc)
    return params


def match(j, args, params, tags, tasklet):
    return True

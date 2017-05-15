def main(j, args, params, tags, tasklet):
    params.merge(args)
    doc = params.doc
    tags = params.tags.getDict()
    space = params.paramsExtra['space']
    out = ""
    nroflines = int(tags.get('nroflines', 0))
    logdir = j.dirs.LOGDIR
    if 'filename' in list(tags.keys()):
        filename = tags['filename']
        logs = j.sal.fs.joinPaths(logdir, filename)
    else:
        spaces = j.portal.tools.server.active.getSpaces()
        if space in spaces:
            logs = j.sal.fs.joinPaths(logdir, 'space_%s.log') % space
        else:
            params.result = (out, params.doc)
            return params
    if not j.sal.fs.exists(logs):
        out = 'no access logs available  on this enviroment'
        params.result = (out, args.doc)
        return params
    logcontent = j.sal.fs.fileGetContents(logs)
    loglines = logcontent.splitlines()
    out += "||Time || Client ipaddress || User || Page || Full Path||\n"
    for line in loglines[-nroflines:]:
        linecontent = line.split('|')
        out += "|| %s | %s | %s | %s | %s |\n" % (linecontent[0],
                                                  linecontent[1],
                                                  linecontent[3],
                                                  linecontent[4],
                                                  linecontent[5])
    params.result = (out, params.doc)
    return params


def match(j, args, params, tags, tasklet):
    return True

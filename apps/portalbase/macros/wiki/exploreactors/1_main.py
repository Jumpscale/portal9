import os


def main(j, args, params, tags, tasklet):
    params.merge(args)

    out = ""

    actors = j.portal.tools.server.active.actorsloader.id2object

    for actorname in sorted(actors.keys()):
        model = actors[actorname].model  # TODO: security breach
        path = os.path.abspath(model.path)
        if not j.sal.fs.exists(path):
            j.sal.fs.createDir(path)
        path = path.replace(":", "___")
        # out+="|[%s | /system/Explorer/?path=%s] |[reload | /system/reloadactor/?name=%s]|\n" % (model.id,path,model.id)
        out += "|%s|[Spec|/system/Explorer?ppath=%s]|[Actions|/system/Explorer?ppath=%s]|\n" % (actorname.capitalize(),
                                                                                                j.sal.fs.joinPaths(
                                                                                                    path, 'specs'),
                                                                                                j.sal.fs.joinPaths(path, 'methodclass'))

    params.result = out

    params.result = (params.result, params.doc)

    return params


def match(j, args, params, tags, tasklet):
    return True

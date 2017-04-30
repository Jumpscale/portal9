import os
# import urllib.request, urllib.parse, urllib.error

try:
    import urllib.request
    import urllib.parse
    import urllib.error
except:
    import urllib.parse as urllib


def main(j, args, params, tags, tasklet):
    params.merge(args)

    out = ""

    spaces = j.portal.server.active.spacesloader.spaces

    for spacename in sorted(spaces.keys()):
        model = spaces[spacename].model  # TODO: security breach
        path = os.path.abspath(model.path)
        querystr = urllib.parse.urlencode({'ppath': path})

        out += "| [%s | /system/Explorer?%s] | [Reload | /system/ReloadSpace?name=%s] | [Delete | /system/DeleteSpace?spacename=%s]|\n" % \
            (model.id, querystr, model.id, model.id)

    params.result = (out, params.doc)

    return params


def match(j, args, params, tags, tasklet):
    return True


def main(j, args, params, tags, tasklet):
    params.merge(args)

    out = ""
    spaces = j.portal.tools.server.active.spacesloader.spaces
    for spacename in spaces:
        out += "* [%s|/system/ReloadSpace/?name=%s]\n" % (spacename, spacename)

    params.result = (out, params.doc)

    return params


def match(j, args, params, tags, tasklet):
    return True

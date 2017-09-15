def main(j, args, params, tags, tasklet):
    params.merge(args)

    doc = params.doc

    out = "||Name||Description||Active||\n"
    groups = j.portal.tools.server.active.auth.listGroups()
    for group in groups:

        out += "|[%(name)s|group?id=%(id)s]|%(description)s|%(active)s|\n" % group

    params.result = (out, doc)

    return params


def match(j, args, params, tags, tasklet):
    return True

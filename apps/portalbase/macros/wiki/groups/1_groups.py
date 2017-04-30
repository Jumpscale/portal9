def main(j, args, params, tags, tasklet):
    params.merge(args)

    doc = params.doc
    out = "{{datatables_use}}}}\n\n"

    out += "||Name||Description||Domain||Active||\n"
    groups = j.portal.server.active.auth.listGroups()
    for group in groups:

        out += "|[%(name)s|group?id=%(id)s]|%(description)s|%(domain)s|%(active)s|\n" % group

    params.result = (out, doc)

    return params


def match(j, args, params, tags, tasklet):
    return True

def main(j, args, params, tags, tasklet):
    params.merge(args)

    doc = params.doc
    tags = params.tags

    defmanager = j.portal.tools.defmanager.portaldefmanager

    defs = defmanager.getDefListWithLinks()

    out = "{{code:\n"

    firstletter = ""
    for name, link, aliases in defs:
        aliases.sort()
        if aliases != []:
            out += "* %s (%s)\n" % (name, ",".join(aliases))
        else:
            out += "* %s\n" % name

    out += "}}\n"

    params.result = (out, doc)

    return params


def match(j, args, params, tags, tasklet):
    return True

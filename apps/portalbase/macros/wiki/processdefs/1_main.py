def main(j, args, params, tags, tasklet):
    params.merge(args)

    doc = params.doc
    tags = params.tags

    doc = j.portal.tools.defmanager.portaldefmanager.processDefs(doc)

    params.result = ("", doc)

    return params


def match(j, args, params, tags, tasklet):
    return True

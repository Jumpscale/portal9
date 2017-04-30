
def main(j, args, params, tags, tasklet):

    doc = args.doc

    params.result = ""
    spaces = sorted([(x.model.id, x.model.name) for x in list(j.portal.server.active.spacesloader.spaces.values())])

    C = "{{menudropdown: %s\n" % args.tags
    for spaceid, spacename in spaces:
        C += "%s:/%s\n" % (spacename, spaceid)
    C += "}}\n"

    if j.portal.server.active.isAdminFromCTX(args.requestContext):
        params.result = C

    params.result = (params.result, doc)

    return params


def match(j, args, params, tags, tasklet):
    return True

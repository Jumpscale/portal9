
def main(j, args, params, tags, tasklet):
    params.merge(args)

    doc = params.doc

    params.result = ""

    C = args.macrostr.replace("menuloggedin", "menu")

    if j.portal.tools.server.active.isLoggedInFromCTX(params.requestContext):
        params.result = C

    params.result = (params.result, doc)

    return params


def match(j, args, params, tags, tasklet):
    return True

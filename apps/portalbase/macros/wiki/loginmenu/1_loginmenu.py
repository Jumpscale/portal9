
def main(j, args, params, tags, tasklet):
    params.merge(args)
    doc = params.doc

    macrostr = params.macrostr
    macrostr = macrostr.split('\n')

    if j.portal.tools.server.active.isLoggedInFromCTX(params.requestContext):
        loginorlogout = "Logout: /system/login?user_logoff_=1"
    else:
        loginorlogout = "Login: /system/login"

    params.result = result

    params.result = (params.result, doc)

    return params


def match(j, args, params, tags, tasklet):
    return True

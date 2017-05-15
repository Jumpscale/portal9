
def main(j, args, params, tags, tasklet):
    page = args.page

    if "actorname" in args.paramsExtra:
        actorname = args.paramsExtra["actorname"]
    else:
        actorname = ""

    if "appname" in args.paramsExtra:
        appname = args.paramsExtra["appname"]
    else:
        appname = ""

    page2 = j.portal.tools.portalloaders.portalloaderfactory.actorsinfo.getActorsInfoPage(appname=appname, actor=actorname)

    page.addBootstrap()
    page.addMessage(page2.body)

    params.result = page
    return params


def match(j, args, params, tags, tasklet):
    return True

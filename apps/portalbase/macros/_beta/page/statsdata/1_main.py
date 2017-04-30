
def main(j, args, params, tags, tasklet):
    page = args.page

    infomgr = j.apps.actorsloader.getActor("system", "infomgr")

    args = args.tags.getValues(id=None, start=0, stop=0)
    id = args["id"]

    data = infomgr.extensions.infomgr.getInfo5Min(id, args["start"], args["stop"], epoch2human=True)

    if data is not None:

        page.addList(data)
    else:
        page.addMessage("No data for %s" % id)

    params.result = page
    return params


def match(j, args, params, tags, tasklet):
    return True

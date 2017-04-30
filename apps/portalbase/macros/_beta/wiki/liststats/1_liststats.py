
def main(j, args, params, tags, tasklet):
    params.merge(args)

    doc = params.doc
    tags = params.tags

    params.result = ""

    # args=params.tags.getValues(id="",width="800",height=400,title="")

    infomgr = j.apps.actorsloader.getActor("system", "infomgr")

    ids = infomgr.extensions.infomgr.listHistoryObjects()
    out = ""
    for key in ids:
        C = "|[Graph for $key|/system/ShowMonthStat?key=$key]|[Data for $key|/system/ShowMonthStatData?key=$key]|"
        C = C.replace("$key", key)
        out += "%s\n" % C

    params.result = (out, doc)

    return params


def match(j, args, params, tags, tasklet):
    return True

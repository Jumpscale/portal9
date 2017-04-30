
def main(j, args, params, tags, tasklet):
    params.merge(args)

    doc = params.doc
    tags = params.tags

    params.result = ""

    args = params.tags.getValues(id="", width="800", height=400, title="", mod=100)

    C = """
{{stats: id:$id start:-2h stop:-1h title:'$t1' width:$w height:$h mod:$mod}}

{{stats: id:$id start:-24h stop:-1h title:'$t2' width:$w height:$h mod:$mod}}

{{stats: id:$id start:-7d stop:-1h title:'$t3' width:$w height:$h mod:$mod}}

{{stats: id:$id start:-30d stop:-1h title:'$t4' width:$w height:$h mod:$mod}}
"""
    C = C.replace("$id", args["id"])
    C = C.replace("$w", args["width"])
    C = C.replace("$h", args["height"])
    C = C.replace("$t1", "%s Hourly" % args["title"])
    C = C.replace("$t2", "%s Daily" % args["title"])
    C = C.replace("$t3", "%s Weekly" % args["title"])
    C = C.replace("$t4", "%s Monthly" % args["title"])
    C = C.replace("$mod", str(args["mod"]))

    params.result = (C, doc)

    return params


def match(j, args, params, tags, tasklet):
    return True

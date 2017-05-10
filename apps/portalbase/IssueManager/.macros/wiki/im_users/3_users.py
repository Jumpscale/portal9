
def main(j, args, params, tags, tasklet):

    res = {}
    uc = j.tools.issuemanager.getUserCollectionFromDB()
    keys = []

    for item in uc.find():
        res[item.dbobj.name] = []
        keys.append(item.dbobj.name)
        res[item.dbobj.name].append(item.dbobj.fullname)
        res[item.dbobj.name].append(item.dbobj.email)
        url = item.dbobj.gitHostRefs[0].url
        res[item.dbobj.name].append(url)
        res[item.dbobj.name].append(item.key)

    out = "||name||fullname||email||info||\n"

    keys.sort()
    for key in keys:
        fullname, email, url, ref = res[key]
        info = "[gitlink|(%s)] [kanban|%s]" % (url, "todourl")  #
        out += "|%s|%s|%s|%s|\n" % (key, fullname, email, info)

    # params.result = out
    doc = args.doc

    params.result = (out, doc)

    return params


def match(j, args, params, tags, tasklet):
    return True

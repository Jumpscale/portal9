
def main(j, args, params, tags, tasklet):

    page = args.page

    infomgr = j.apps.actorsloader.getActor("system", "infomgr")

    args3 = args.tags.getValues(id=None, start="-3d", stop="-1h", maxvalues=200)

    args2 = args.tags.getValues(width="800", height=400, title=args3["id"], mod=100)

    header, rows = infomgr.getInfoWithHeaders(**args3)  # TODO: is args 3

    mod = int(args2["mod"])

    if mod != 100:
        mod = float(mod)
        rows2 = []
        for row in rows:
            row = [(float(item) / 100.0 * mod) for item in row]
            rows2.append(row)
        rows = rows2

    page.addBootstrap()
    page.addLineChart(args2["title"], rows, header, width=args2["width"], height=args2["height"])

    params.result = page
    return params


def match(j, args, params, tags, tasklet):
    return True


def main(j, args, params, tags, tasklet):

    doc = args.doc
    tags = args.tags

    out = ""

    bullets = args.tags.labelExists("bullets")
    table = args.tags.labelExists("table")

    if table:
        rows = []

        for item in sorted(j.portal.tools.server.active.getActors()):
            app, actor = item.split("__")
            out += "|[%s|/rest/%s/%s]|\n" % (item, app.lower().strip("/"), actor.lower().strip("/"))

    else:

        for item in sorted(j.portal.tools.server.active.getActors()):
            if item[0] != "_" and item.strip() != "":
                app, actor = item.split("__")
                if bullets:
                    out += "* [%s|/rest/%s/%s]\n" % (item, app.lower().strip("/"), actor.lower().strip("/"))
                else:
                    out += "|[%s|/rest/%s/%s]|\n" % (item, app.lower().strip("/"), actor.lower().strip("/"))

    params.result = (out, doc)

    return params


def match(j, args, params, tags, tasklet):
    return True

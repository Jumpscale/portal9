
def main(j, args, params, tags, tasklet):

    page = args.page

    args2 = args.tags.getValues(exclude="")
    excl = args2["exclude"]
    if excl != "":
        for item in excl.split(","):
            page.removeCSS(item, permanent=False)

    cmdstr = args.cmdstr.split("exclude")[0]
    page.addCSS(cssLink=cmdstr)

    if excl != "":
        for item in excl.split(","):
            key = item.strip().lower()
            page.jscsslinks[key] = True

    params.result = page

    return params


def match(j, args, params, tags, tasklet):
    return True

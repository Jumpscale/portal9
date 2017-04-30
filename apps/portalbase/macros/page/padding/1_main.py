
def main(j, args, params, tags, tasklet):
    page = args.page

    if args.tags.tagExists("top"):
        top = args.tags.tagGet("top")
        try:
            bottom = args.tags.tagGet("bottom")
        except:
            bottom = 0
        page.padding = "%s-%s" % (top, bottom)
    else:
        page.padding = True

    params.result = page
    return params


def match(j, args, params, tags, tasklet):
    return True

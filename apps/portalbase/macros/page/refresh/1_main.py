
def main(j, args, params, tags, tasklet):
    page = args.page

    refresh = int(args.tags.tagGet("time", 60))
    if args.doc.destructed is False:
        page.head += "<meta http-equiv=\"refresh\" content=\"%s\" >" % refresh
        page.head += '<meta http-equiv="Cache-Control" content="no-store, no-cache, must-revalidate" /> '

    params.result = page
    return params


def match(j, args, params, tags, tasklet):
    return True

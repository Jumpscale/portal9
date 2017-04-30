
def main(j, args, params, tags, tasklet):
    page = args.page
    page.addBootstrap()
    page.addMessage("<footer><p>%s</p></footer>" % args.cmdstr)
    params.result = page
    return params


def match(j, args, params, tags, tasklet):
    return True

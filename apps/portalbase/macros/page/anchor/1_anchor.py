
def main(j, args, params, tags, tasklet):
    params.result = page = args.page
    page.addMessage('<a name="{0}"></a>'.format(args.cmdstr))

    return params


def match(j, args, params, tags, tasklet):
    return True

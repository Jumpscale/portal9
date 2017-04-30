
def main(j, args, params, tags, tasklet):
    args.page.addBootstrap()
    args.page.projectname = args.cmdstr

    params.result = args.page
    return params


def match(j, args, params, tags, tasklet):
    return True

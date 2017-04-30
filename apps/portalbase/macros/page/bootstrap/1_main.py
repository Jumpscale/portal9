
def main(j, args, params, tags, tasklet):
    page = args.page
    page.addBootstrap()

    params.result = page
    return params


def match(j, args, params, tags, tasklet):
    return True

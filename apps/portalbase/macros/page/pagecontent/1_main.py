
def main(j, args, params, tags, tasklet):
    page = args.page
    page.addBootstrap()
    page.addCodeBlock(args.doc.source)

    params.result = page
    return params


def match(j, args, params, tags, tasklet):
    return True

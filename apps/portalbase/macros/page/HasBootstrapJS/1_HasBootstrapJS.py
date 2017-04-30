
def main(q, args, params, *other_args):
    params.result = page = args.page
    page._hasBootstrapJS = True
    return params


def match(q, args, params, tags, tasklet):
    return True

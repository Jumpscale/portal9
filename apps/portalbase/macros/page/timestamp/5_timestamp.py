def main(j, args, params, *other_args):
    klass = args.getTag('class') or 'jstimestamp'
    args.page.addTimeStamp(klass)
    params.result = args.page
    return params


def match(j, args, params, tags, tasklet):
    return True

def main(j, args, params, *other_args):
    klass = 'jstimestamp'
    ts = args.cmdstr
    args.page.addTimeStamp(klass)
    args.page.addMessage("<span class='%s' data-ts='%s'></span>" % (klass, ts))
    params.result = args.page
    return params


def match(j, args, params, tags, tasklet):
    return True

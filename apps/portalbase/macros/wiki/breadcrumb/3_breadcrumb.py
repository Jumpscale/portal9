
def main(j, args, params, tags, tasklet):
    import yaml
    args.requestContext.params['breadcrumbdata'] = yaml.load(args.cmdstr)
    params.result = ('', args.doc)
    return params


def match(j, args, params, tags, tasklet):
    return True

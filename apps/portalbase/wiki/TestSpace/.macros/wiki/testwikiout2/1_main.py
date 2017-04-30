
def main(j, args, params, tags, tasklet):
    params.merge(args)

    doc = params.doc
    tags = params.tags

    params.result = "h5. hello\nThis content is from the included macro\n"

    params.result = (params.result, doc)

    return params


def match(j, args, params, tags, tasklet):
    return True

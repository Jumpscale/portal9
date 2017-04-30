
def main(j, args, params, tags, tasklet):
    params.merge(args)

    doc = params.doc
    tags = params.tags

    content = "TEST all the rest is gone"

    params.result = (content, doc)

    return params


def match(j, args, params, tags, tasklet):
    return True

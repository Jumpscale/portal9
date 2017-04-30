
def main(j, args, params, tags, tasklet):
    params.merge(args)

    doc = params.doc
    tags = params.tags

    params.result = "h2. hello\nThis content is just added to page at runtime so can be dynamic.\n Is also working recursive so can insert other macro.\nFormat is confluence\n\nh3. includedmacro\n{{testwikiout2}}\n"

    params.result = (params.result, doc)

    return params


def match(j, args, params, tags, tasklet):
    return True

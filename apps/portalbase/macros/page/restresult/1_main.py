
def main(j, args, params, tags, tasklet):
    import pprint
    result = args.paramsExtra.get("result")
    if result:
        result = pprint.pformat(result)
        args.page.addCodeBlock(result)
    else:
        args.page.addMessage("No result set")
    params.result = args.page
    return params


def match(j, args, params, tags, tasklet):
    return True

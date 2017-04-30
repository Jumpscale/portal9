
def main(j, args, params, tags, tasklet):
    session = args.requestContext.env['beaker.session']
    msg = session.get('autherror', '')
    params.result = (msg, args.doc)

    return params


def match(j, args, params, tags, tasklet):
    return True

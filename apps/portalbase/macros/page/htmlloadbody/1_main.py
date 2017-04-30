
def main(j, args, params, tags, tasklet):

    page = args.page

    if len(args.doc.htmlBodiesCustom) < 1:
        raise RuntimeError("Could not find custom html body on doc %s" % args.doc.name)

    page.addMessage(args.doc.htmlBodiesCustom[0])
    params.result = page
    return params


def match(j, args, params, tags, tasklet):
    return True


def main(j, args, params, *other_args):
    params.result = page = args.page
    page.addMessage(args.cmdstr.title())
    return params


def match(*whatever):
    return True

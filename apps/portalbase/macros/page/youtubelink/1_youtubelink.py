def main(j, args, params, *other_args):
    params.result = page = args.page
    link = 'https://www.youtube.com/watch?v={}'.format(args.cmdstr)
    page.addMessage(link)
    return params


def match(*whatever):
    return True

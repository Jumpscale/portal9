from JumpScale9Portal.portal.macrolib.blog import BlogPost


def main(j, args, params, *other_args):
    params.result = page = args.page
    post = BlogPost(args.doc.path)
    page.addMessage(post.title)
    return params


def match(j, args, params, tags, tasklet):
    return True

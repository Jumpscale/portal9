from JumpScale9Portal.portal.macrolib.blog import BlogPost


def main(j, args, params, *other_args):
    params.result = page = args.page

    blog_posts = BlogPost.get_posts_in(args.doc.path)

    blog_template = args.cmdstr.strip() or '''
        <article>
            <h2><a href="{blog_url}">{blog_title}</a></h2>
            <date>{blog_date}</date>
            {blog_content}
        </article>
    '''

    page.addMessage(''.join(blog_template.format(blog_url=post.url,
                                                 blog_title=post.title,
                                                 blog_date=post.date,
                                                 blog_content=post.content)
                            for post in blog_posts))
    return params


def match(j, args, params, tags, tasklet):
    return True

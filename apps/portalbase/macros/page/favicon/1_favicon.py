import os

# Usage::
#
#   {{favicon:.files/img/favicon.png}}
#


def main(j, args, params, tags, tasklet):
    page = args.page
    icon_path = args.cmdstr
    _, extension = os.path.splitext(icon_path)
    image_type = {'.png': 'png', '.ico': 'x-icon'}.get(extension, 'png')

    page.addHTMLHeader(
        '<link rel="shortcut icon" type="image/{2}" href="/{0}/{1}" />'.format(args.doc.getSpaceName(),
                                                                               icon_path,
                                                                               image_type))

    params.result = page
    return params


def match(j, args, params, tags, tasklet):
    return True

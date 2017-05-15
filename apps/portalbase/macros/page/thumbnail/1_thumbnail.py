# Usage::
#
#   {{thumbnail:.files/img/favicon.png 200x100 exact_size}}
#
# where width = 200 & height = 100
#
# By default, the macro preserves the aspect ratio of the image. If you set 'exact_size', then the generated thumbnail
# will be of the same passed size exactly. 'exact_size' is optional

import os

DEFAULT_THUMB_SIZE = '150x100'


def main(j, args, params, tags, tasklet):
    page = args.page

    try:
        import Image
    except ImportError:
        # pyflakes.ignore
        from PIL import Image

    space_name = args.doc.getSpaceName()
    space_path = j.portal.tools.server.active.getSpace(space_name).model.path

    macro_params = args.cmdstr.split(' ')
    img_url = macro_params[0]
    if len(macro_params) >= 2:
        thumb_size = macro_params[1]
    else:
        thumb_size = args.doc.docparams.get('thumb_size', DEFAULT_THUMB_SIZE)

    if len(macro_params) >= 3:
        exact_size = macro_params[2]
    else:
        exact_size = False

    thumb_size = thumb_size or args.doc.docparams.get('thumb_size', DEFAULT_THUMB_SIZE)

    width, height = [int(x) for x in thumb_size.split('x')]

    img_path = img_url.strip('/')
    full_img_path = os.path.join(space_path, img_path)
    # Add 's_' to file name to tell that this is a thumbnail, and add width & height too
    thumbnail_path = ('{0}s_{1}x{2}_').format(os.path.sep, width, height).join(os.path.split(full_img_path))
    img_url_base, img_name = os.path.split(img_url)
    thumbnail_url = os.path.join(space_name, img_url_base.strip('/'), r's_{0}x{1}_{2}'.format(width, height, img_name))

    # If the thumbnail doesn't exist on the desk, generate it
    if not os.path.exists(thumbnail_path):
        im = Image.open(full_img_path)
        if exact_size:
            im = im.resize((width, height), Image.ANTIALIAS)
        else:
            im.thumbnail((width, height), Image.ANTIALIAS)
        im.save(thumbnail_path)

    page.addMessage('<img src="/{0}" />'.format(thumbnail_url))
    params.result = page
    return params


def match(j, args, params, tags, tasklet):
    return True

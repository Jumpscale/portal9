import os


def main(j, args, params, tags, tasklet):
    params.result = args.page

    space = j.portal.tools.server.active.spacesloader.spaces[args.doc.getSpaceName()]
    imagedir = j.sal.fs.joinPaths(space.model.path, '.files', 'img')
    pars = args.expandParamsAsDict()

    if 'title' not in pars:
        title = ""
    else:
        title = pars['title']
    if 'picturedir' in pars:
        base_url = "$$space/.files/img/%s" % pars['picturedir']
        images_root = j.sal.fs.joinPaths(imagedir, pars['picturedir'])
    else:
        base_url = "images/$$space"
        localpath = args.doc.path
        images_root = j.sal.fs.getDirName(localpath)

    img_files = (j.sal.fs.listFilesInDir(images_root, filter="*.jpg", case_sensitivity='insensitive') +
                 j.sal.fs.listFilesInDir(images_root, filter="*.jpeg", case_sensitivity='insensitive') +
                 j.sal.fs.listFilesInDir(images_root, filter="*.png", case_sensitivity='insensitive') +
                 j.sal.fs.listFilesInDir(images_root, filter="*.gif", case_sensitivity='insensitive') +
                 j.sal.fs.listFilesInDir(images_root, filter="*.bmp", case_sensitivity='insensitive'))

    # Make sure we don't include the thumbnails
    thumbnails = (j.sal.fs.listFilesInDir(images_root, filter="s_*.*", case_sensitivity='insensitive') +
                  j.sal.fs.listFilesInDir(images_root, filter=".*-s[.].*", case_sensitivity='insensitive'))
    img_files = [x for x in img_files if x not in thumbnails]

    thumb_size = pars.get('thumb_size', args.doc.docparams.get('thumb_size', '150x100'))
    thumb_size = [int(x) for x in thumb_size.split('x')]

    for image in img_files:
        img_name = j.sal.fs.getBaseName(image)

        # Generate a thumbnail from the existing image
        thumbnail_path = os.path.join(images_root, 's_{0}x{1}_{2}'.format(thumb_size[0], thumb_size[1], img_name))
        if not j.sal.fs.exists(thumbnail_path):
            j.tools.imagelib.resize(image, thumbnail_path, width=thumb_size[0])

    out = '''
    <script src="/$$space/.files/js/blueimp-gallery.min.js"></script>
    <script src="/$$space/.files/js/blueimp-gallery-fullscreen.js"></script>
    <script src="/$$space/.files/js/blueimp-gallery-indicator.js"></script>
    <script src="/$$space/.files/js/jquery.blueimp-gallery.min.js"></script>
    <div id="links" class="links">
    '''

    for image in img_files:
        img_name = j.sal.fs.getBaseName(image)
        img_url = "/%s/%s" % (base_url.strip('/'), img_name)
        thumb_url = "/%s/s_%sx%s_%s" % (base_url, thumb_size[0], thumb_size[1], img_name)

        out += '''<a href="%s" data-gallery><img src="%s" alt=""></a>''' % (img_url, thumb_url)

    out += '''
    </div>
    <div id="blueimp-gallery" class="blueimp-gallery blueimp-gallery-controls">
        <div class="slides"></div>
        <h3 class="title">%s</h3>
        <a class="prev">&lsaquo;</a>
        <a class="next">&rsaquo;</a>
        <a class="close">&times;</a>
        <a class="play-pause"></a>
        <ol class="indicator"></ol>
    </div>
    ''' % title

    out = out.replace('$$space', args.doc.getSpaceName())

    params.result.addCSS("/%s/.files/css/blueimp-gallery.css" % args.doc.getSpaceName())
    params.result.addCSS("/%s/.files/css/blueimp-gallery-indicator.css" % args.doc.getSpaceName())
    params.result.addCSS(
        cssContent=".links a { margin: 12px;display: inline-block;border: 2px solid #E1E1E1;} .blueimp-gallery > .slides { padding: 30px 0;}")
    params.result.addMessage(out)
    return params


def match(j, args, params, tags, tasklet):
    return True

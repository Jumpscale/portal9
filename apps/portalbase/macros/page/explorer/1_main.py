
def main(j, args, params, tags, tasklet):
    import os
    page = args.page
    params.result = page
    page.addCSS(cssContent='''
.elfinder-contextmenu{
    left: 39%;
}
''')
    path = ''
    space = args.paramsExtra.get('explorerspace')
    if space:
        space = j.portal.tools.server.active.getSpace(space)
        path = space.model.path

    if args.tags.tagExists("ppath"):
        path = args.tags.tagGet("ppath").replace("+", ":").replace("___", ":").replace("\\", "/")
        origpath = path
        path = j.dirs.replace_txt_dir_vars(path)
        if not j.sal.fs.exists(path):
            page.addMessage("ERROR:could not find file %s" % path)
        apppath = j.portal.tools.server.active.basepath
        codepath = os.getcwd()
        if path.startswith("/") and (apppath in path or codepath in path):
            page.addMessage('Requested path is not allowed')
            return params

    if args.tags.tagExists("bucket"):
        bucket = args.tags.tagGet("bucket").lower()

        if bucket not in j.portal.tools.server.active.bucketsloader.buckets:
            page.addMessage("Could not find bucket %s" % bucket)
            return params
        bucket = j.portal.tools.server.active.bucketsloader.buckets[bucket]
        path = bucket.model.path.replace("\\", "/")

    if args.tags.tagExists("height"):
        height = int(args.tags.tagGet("height"))
    else:
        height = 500

    if args.tags.tagExists("key"):
        key = args.tags.tagGet("key")
    else:
        key = None

    if args.tags.tagExists("readonly") or args.tags.labelExists("readonly"):
        readonly = True
    else:
        readonly = False

    if args.tags.tagExists("tree") or args.tags.labelExists("tree"):
        tree = True
    else:
        tree = False

    if path == "$$path":
        params.page.addMessage("Could not find path to display explorer for")
        return params

    page.addExplorer(path, dockey=key, height=height, readonly=readonly, tree=tree)

    return params


def match(j, args, params, tags, tasklet):
    return True

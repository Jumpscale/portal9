import os


def main(j, args, params, tags, tasklet):
    params.result = page = args.page

    portal = j.portal.tools.server.active
    contentdir = args.paramsExtra.get('contentdir')
    space_path = args.paramsExtra.get('space_path')
    space_type = args.paramsExtra.get('space_type')

    if contentdir and space_path:
        portal.spacesloader = j.portal.tools.portalloaders.loaderfactory.getSpacesLoader()

        if os.path.exists(space_path):
            page.addMessage('***ERROR***: The space path "{}" already exists'.format(space_path))
            return params

        if not os.path.exists(contentdir):
            page.addMessage('***ERROR***: The content dir "{}" does not exist'.format(contentdir))
            return params

        os.makedirs(os.path.join(space_path, '.space'))
        os.symlink(space_path, os.path.join(contentdir, os.path.basename(space_path)))

        header = '##' if space_type == 'md' else 'h2.'
        with open(os.path.join(space_path, 'Home.%s' % space_type), 'w') as f:
            f.write('@usedefault\n\n%s Welcome to the new space\nThis space lives in `%s`' % (header, space_path))

        portal.spacesloader.scan(portal.contentdirs)
        spacename = j.sal.fs.getBaseName(space_path).lower()
        portal.spacesloader.id2object[spacename].createDefaults(space_path)
        portal.spacesloader.id2object[spacename].createTemplate(space_path, templatetype=space_type)

        page.addMessage(
            'Created successfully. Click <a href="/{}/">here</a> to go to the new portal'.format(os.path.basename(space_path)))

    else:
        contentdirs = ''.join('<option value="{0}">{0}</option>'.format(d) for d in portal.contentdirs)

        page.addMessage('''
            <form class="form-horizontal" method="get" action="/system/createspace">
                <fieldset>
                    <div class="control-group">
                        <label class="control-label" for="space_path">Path to space</label>
                        <div class="controls">
                            <input name="space_path" type="text" placeholder="" class="input-xxlarge width-40" required="" value="/opt/code/github/jumpscale/www_<my_space>">
                        </div>
                    </div>
                    <div class="control-group margin-bottom-large">
                        <label class="control-label" for="contentdir">Content Directory</label>
                        <div class="controls" name="contentdir">
                            <select name="contentdir" id="contentdir" class="input-xxlarge width-40">
                            {0}
                            </select>
                        </div>
                    </div>
                    <div class="control-group margin-bottom-large">
                        <label class="control-label" for="space_type">Space type</label>
                        <div class="controls" name="space_type">
                            <select name="space_type" id="space_type" class="input-xxlarge width-40">
                                <option value="md">Markdown</option>
                                <option value="wiki">Portal Wiki</option>
                            </select>
                        </div>
                    </div>
                    <div class="control-group">
                        <div class="controls">
                            <button class="btn btn-primary">Create</button>
                        </div>
                    </div>

                </fieldset>
            </form>'''.format(contentdirs))

    return params


def match(j, args, params, tags, tasklet):
    return True

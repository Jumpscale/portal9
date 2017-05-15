import os


def main(j, args, params, tags, tasklet):
    params.result = page = args.page

    page_space = args.paramsExtra.get('page_space')
    page_name = args.paramsExtra.get('page_name')
    page_type = args.paramsExtra.get('page_type')

    # Creating a new page
    if page_name and page_space:
        space = j.portal.tools.server.active.getSpace(page_space)
        if not page_name:
            page.addMessage("ERROR: page name must be specified")
            return

        space = j.portal.tools.server.active.getSpace(page_space)
        j.sal.fs.createDir(os.path.join(space.model.path, page_name))
        j.sal.fs.writeFile(os.path.join(space.model.path, page_name, page_name + '.%s' % page_type), '')

        # Reload spaces to discover the new page
        # TODO: find an efficient way of doing this
        j.portal.tools.server.active.loadSpaces()

        # Redirect to edit the new page
        page.addMessage(
            "<script>window.open('/system/edit?edit_space={0}&edit_page={1}', '_self', '');</script>".format(page_space, page_name))
    elif page_name is None and page_space is not None:

        page.addMessage('''
            <form class="form-horizontal" method="get" action="/system/create">
                <fieldset>
                <div class="control-group">
                <input type="hidden" name="page_space" value="$$space">
                </div>
                <div class="control-group">
                  <label class="control-label" for="page_name">Name</label>
                  <div class="controls">
                    <input id="page" name="page_name" type="text" placeholder="" class="input-xlarge margin-bottom-large width-40" required="">
                  </div>
                </div>

                <div class="control-group margin-bottom-large">
                    <label class="control-label" for="page_type">Page type</label>
                    <div class="controls" name="page_type">
                        <select name="page_type" id="page_type" class="input-xxlarge width-40">
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
            </form>
            '''.replace("$$space", page_space))
    else:

        spaces = sorted(s for s in j.portal.tools.server.active.getSpaces())
        spaces = ''.join('<option value="{0}">{0}</option>'.format(space) for space in spaces)
        page.addMessage('''
            <form class="form-horizontal" method="get" action="/system/create">
                <fieldset>
                <div class="control-group">
                  <label class="control-label" for="selectbasic">Select space...</label>
                  <div class="controls">
                    <select id="space" name="space" class="input-xlarge">
                      {0}
                    </select>
                  </div>
                </div>

                <div class="control-group">
                  <label class="control-label" for="name">Name</label>
                  <div class="controls">
                    <input id="page" name="page" type="text" placeholder="" class="input-xlarge margin-bottom-large width-40" required="">
                  </div>
                </div>

                <div class="control-group">
                  <div class="controls">
                    <button class="btn btn-primary">Create</button>
                  </div>
                </div>

                <div class="control-group margin-bottom-large">
                    <label class="control-label" for="page_type">Page type</label>
                    <div class="controls" name="page_type">
                        <select name="page_type" id="page_type" class="input-xxlarge width-40">
                            <option value="md">Markdown</option>
                            <option value="wiki">Portal Wiki</option>
                        </select>
                    </div>
                </div>

                </fieldset>
            </form>
            '''.format(spaces))

    return params


def match(j, args, params, tags, tasklet):
    return True

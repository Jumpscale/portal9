from JumpScale.portal.docgenerator.popup import Popup


def main(j, args, params, tags, tasklet):

    params.result = page = args.page
    groupid = args.getTag('id')
    group = j.data.models_system.Group.get(groupid)
    if not group:
        params.result = ('group with id %s not found' % groupid, args.doc)
        return params

    popup = Popup(id='group_edit', header='Change Group', clearForm=False,
                  submit_url='/restmachine/system/usermanager/editGroup')

    options = list()
    popup.addText('Enter domain', 'domain', value=group.domain)
    popup.addText('Enter description', 'description', value=group.description)
    for user in j.data.models_system.User.find({}):
        available = user['id'] in [u['id'] for u in j.data.models_system.User.find({'groups': group['name']})]
        options.append((user['name'], user['name'], available))

    popup.addCheckboxes('Select Users', 'users', options)
    popup.addHiddenField('name', group.name)
    popup.write_html(page)

    return params

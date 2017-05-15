from JumpScale9Portal.portal.docgenerator.popup import Popup


def main(j, args, params, tags, tasklet):

    params.result = page = args.page
    userid = args.getTag('id')
    user = j.data.models.system.User.get(userid)
    if not user:
        params.result = ('User with id %s not found' % userid, args.doc)
        return params

    popup = Popup(id='user_edit', header='Change User', submit_url='/restmachine/system/usermanager/editUser')

    options = list()
    popup.addText('Enter emails (comma seperated)', 'emails', value=', '.join(user.emails))
    popup.addHiddenField('domain', user.domain)
    popup.addText('Enter Password (leave empty to unchange)', 'password', type='password')
    for group in j.data.models.system.Group.find({}):
        available = group['name'] in user.groups
        options.append((group['name'], group['name'], available))

    popup.addCheckboxes('Select Groups', 'groups', options)
    popup.addHiddenField('username', user.name)
    popup.write_html(page)

    return params

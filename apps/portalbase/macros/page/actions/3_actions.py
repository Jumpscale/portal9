def main(j, args, params, tags, tasklet):
    page = args.page
    from JumpScale9Portal.portal.docgenerator.popup import Popup
    import yaml

    def _showexample():
        page.addMessage("""Actions must be in yaml form.
eg:
- display: Start
  action: /restmachine/cloudbroker/machine/start
  input:
  - reason
  - spacename
  - name: accesstype
    type: dropdown
    label: ACL
    values:
     - label: Admin
       value: ARCXDU
     - label: Write
       value: RCX
     - label: Read
       value: R

  data:
   machineId: $$id
   accountName: $$accountname

- display: Stop
  action: /restmachine/cloudbroker/machine/stop?machineId=$$id&reason=ops&accountName=$$accountname&spaceName=$$spacename
}}
""")
        params.result = page
        return params

    macrostr = args.macrostr.strip()
    content = "\n".join(macrostr.split("\n")[1:-1])

    if not content:
        return _showexample()

    actionoptions = [('Choose Action', '#')]
    actions = yaml.load(content, Loader=yaml.loader.BaseLoader)

    if actions == content:
        return _showexample()

    if not isinstance(actions, list):
        actions = [actions]

    for actiondata in actions:
        actionurl = actiondata['action']
        display = actiondata['display']
        inputs = actiondata.get('input', '')
        navigateback = j.data.text.getBool(actiondata.get('navigateback', False))
        reload = j.data.text.getBool(actiondata.get('reload', True))
        hide = j.data.text.getBool(actiondata.get('hide', False))
        data = actiondata.get('data', {})
        showresponse = j.data.text.getBool(actiondata.get('showresponse', False))
        hideon = actiondata.get('hideon', [])
        if hideon:
            hideon_input = actiondata.get('hideonInput', '')
            if hideon_input in hideon:
                continue

        if actionurl.startswith("#"):
            actionoptions.append((display, actionurl[1:]))
            continue
        else:
            actionid = "action-%s" % display.replace(' ', '')
            if not hide:
                actionoptions.append((display, actionid))

        popup = Popup(
            id=actionid,
            header="Confirm Action %s" %
            display,
            submit_url=actionurl,
            navigateback=navigateback,
            reload_on_success=reload,
            showresponse=showresponse)
        if inputs:
            for var in inputs:
                if isinstance(var, str):
                    popup.addText(var, var)
                else:
                    if var['type'] in ('dropdown', 'radio'):
                        label = var['label']
                        name = var['name']
                        options = list()
                        for value in var['values']:
                            options.append((value['label'], value['value']))
                        if var['type'] == 'dropdown':
                            popup.addDropdown(label, name, options)
                        elif var['type'] == 'radio':
                            popup.addRadio(label, name, options)
                    elif var['type'] in ('text', 'password', 'number'):
                        label = var['label']
                        name = var['name']
                        default = var.get('default', '')
                        required = var.get('required', False)
                        popup.addText(label, name, type=var['type'], value=default, required=required)
                    elif var['type'] == 'hidden':
                        popup.addHiddenField(var['name'], var['value'])

        for name, value in list(data.items()):
            popup.addHiddenField(name, value)
        popup.write_html(page)

    if len(actionoptions) > 1:
        id = page.addComboBox(actionoptions)
        page.addJS(None, """
            $(document).ready(function() {
                $("#%(id)s").change(function () {
                     var actionid = $("#%(id)s").val();
                     $("#%(id)s").val('#');
                     if (actionid != '#'){
                        $('#'+actionid).modal('show');
                     }
                });
            });
            """ % ({'id': id}))
    params.result = page

    return params


def match(j, args, params, tags, tasklet):
    return True

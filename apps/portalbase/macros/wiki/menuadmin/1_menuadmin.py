import jinja2
from collections import OrderedDict


def main(j, args, params, tags, tasklet):
    jinja = jinja2.Environment(variable_start_string="${", variable_end_string="}")
    cfg = j.application.instanceconfig
    params.merge(args)
    doc = params.doc

    macrostr = params.macrostr
    macrostr = macrostr.split('\n')

    navigationmenu = None
    adminmenu = None
    megamenu = OrderedDict()

    pages = macrostr[1:-1]

    if j.portal.tools.server.active.isAdminFromCTX(params.requestContext):
        adminmenu = """
{{menudropdown: name:Administration
New Page:/system/create?page_space=$$space
Edit Page:/system/edit?edit_space=$$space&edit_page=$$page&$$querystr
Create Space:/system/createspace
--------------
Files:/system/files?explorerspace=$$space
Access:/system/OverviewAccess?space=$$space
Reload Space:javascript:$.ajax({'url': '/system/ReloadSpace?name=$$space'}).done(function(){location.reload()});void(0);
ReloadAll:javascript:reloadAll();void 0;
}}
"""

    result = ''
    for menu in [navigationmenu, adminmenu]:
        if menu:
            result += menu

    result += '''
    {{htmlhead:
    <script type="text/javascript" src="/jslib/old/adminmenu/adminmenu.js"></script>
    }}
    '''

    params.result = result

    params.result = (params.result, doc)

    return params


def match(j, args, params, tags, tasklet):
    return True


def main(j, args, params, tags, tasklet):
    import json
    import yaml
    page = args.page

    macrostr = args.macrostr.strip()
    content = "\n".join(macrostr.split("\n")[1:-1])
    try:
        gogs_data = yaml.load(content)
    except yaml.error.YAMLError:
        page.addMessage('<h3> **ERROR : Incorrect YAML format , please adjust. </h3>')
        params.result = page
        return params

    if not isinstance(gogs_data, list):
        gogs_data = [gogs_data]

    page.addCSS("/jslib/jqwidgets/styles/jqx.base.css")
    page.addJS("/jslib/jqwidgets/jquery-1.11.1.min.js")
    page.addJS("/jslib/jqwidgets/jqxcore.js")
    page.addJS("/jslib/jqwidgets/jqxsortable.js")
    page.addJS("/jslib/jqwidgets/jqxkanban.js")
    page.addJS("/jslib/jqwidgets/jqxsplitter.js")
    page.addJS("/jslib/jqwidgets/jqxdata.js")

    # { id: "1161", state: "new", label: "Make a new Dashboard", tags: "dashboard", hex: "#36c7d0", resourceId: 3 }
    issues = list()

    for gogs_issue in gogs_data:
        if gogs_issue['priority'] == 'critical':
            gogs_issue['hex'] = "#9e0e23"
        elif gogs_issue['priority'] == 'major':
            gogs_issue['hex'] = "#d87987"
        elif gogs_issue['priority'] == 'normal':
            gogs_issue['hex'] = "#3085ad"
        else:
            gogs_issue['hex'] = "#8b8f91"

        gogs_issue['text'] = 'repo: ' + gogs_issue.get('repo', '') + '</br>' + gogs_issue['content']
        gogs_issue['resourceId'] = gogs_issue['assignees']
        issues.append(gogs_issue)

    def createUserData(user):
        user = user.dictFiltered
        data = {'id': user['key'], 'name': user['name']}
        return data

    user_collection = j.tools.issuemanager.getUserCollectionFromDB()
    users = list(map(createUserData, user_collection.find()))
    users.append({'id': 0,
                  'name': "not assigned",
                  'common': 'true'})
    issues = json.dumps(issues)

    if not json.loads(issues):
        page.addMessage('No issues to show in kanban')

    script = j.portal.server.active.templates.render('system/kanban/script.js', issues=issues, users=users)
    css = j.portal.server.active.templates.render('system/kanban/style.css')
    page.addCSS(cssContent=css)

    kanban = """
    <div id="kanban1"></div>
    """

    legend = """
    <div id="legend">
        <ul style="list-style: none">
            <li style="float: left; margin-right: 10px;"><span'></span> <b>Issues Priorities:</b></li>
            <li style="float: left; margin-right: 10px;"><span style='border: 1px solid #ccc; float: left; width: 12px; height: 12px; margin: 2px; background-color:#9e0e23;'></span> Critical</li>
            <li style="float: left; margin-right: 10px;"><span style='border: 1px solid #ccc; float: left; width: 12px; height: 12px; margin: 2px; background-color:#d87987;'></span> Major</li>
            <li style="float: left; margin-right: 10px;"><span style='border: 1px solid #ccc; float: left; width: 12px; height: 12px; margin: 2px; background-color:#3085ad;'></span> Normal</li>
            <li style="float: left; margin-right: 10px;"><span style='border: 1px solid #ccc; float: left; width: 12px; height: 12px; margin: 2px; background-color:#8b8f91;'></span> Minor/Other</li>
        </ul>
    </div>
    </br>
    """

    page.addJS(jsContent=script)
    page.addHTML(legend)
    page.addHTML(kanban)

    page.addBootstrap()

    params.result = page
    return params


def match(j, args, params, tags, tasklet):
    return True

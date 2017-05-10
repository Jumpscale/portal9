def main(j, args, params, tags, tasklet):
    page = args.page
    modifier = j.portal.tools.html.getPageModifierGridDataTables(page)

    macrostr = args.macrostr.strip().strip('{{').strip('}}')
    tags = j.data.tags.getObject(macrostr, keepcase=True)
    tags = tags.getDict()
    tags.pop(args.macro)

    user_collection = j.tools.issuemanager.getUserCollectionFromDB()
    users = {user.key: user.dbobj.name for user in user_collection.find()}

    if tags.get('assignees') == '$$assignees':
        tags.pop('assignees')

    loggedin = tags.pop('loggedin', False)
    if loggedin:
        user = j.portal.server.active.getUserFromCTX(args.requestContext)
        tags['assignees'] = user

    if 'assignees' in tags:
        match = user_collection.find(name=tags['assignees'])
        user = match[0].key if match else tags['assignees']
        tags['assignees'] = user


    def _formatdata(issues):
        aaData = list()
        for issue in issues:
            issue = issue.dictFiltered
            itemdata = ['<a href=%s> %s </a>' % (issue['gitHostRefs'][0]['url'], issue['title'])]
            itemdata.append(issue['repo'])
            itemdata.append(', '.join([users.get(key, 'no assignees') for key in issue['assignees']]))

            if issue['priority'] == 'critical':
                priority = "<color style='color:#9e0e23'>CRITICAL</color>"
            elif issue['priority'] == 'major':
                priority = "<color style='color:#d87987'>MAJOR</color>"
            elif issue['priority'] == 'normal':
                priority = "<color style='color:#3085ad'>NORMAL</color>"
            else:
                priority = "<color style='color:#8b8f91'>%s</color>" % issue['priority'].upper()
            itemdata.append(priority)

            if issue['state'] in ['closed', 'resolved', 'wontfix']:
                state = "<red style='color:red'> {} </red>".format(issue['state'])
            elif issue['state'] in 'new':
                state = "<green style='color:green'> new </green>"
            else:
                state = "<blue style='color:blue'> {} </blue>".format(issue['state'])
            itemdata.append(state)

            itemdata.append(j.data.time.epoch2HRDateTime(issue['creationTime']))

            aaData.append(itemdata)
        return aaData


    fieldnames = ["Title", "Repo", "Assignees", "Priority", "State", "Creation Time"]

    issue_collection = j.tools.issuemanager.getIssueCollectionFromDB()
    data = _formatdata(issue_collection.find(**tags))

    tableid = modifier.addTableFromData(data, fieldnames)
    modifier.addSearchOptions('#%s' % tableid)

    params.result = page

    return params


def match(j, args, params, tags, tasklet):
    return True

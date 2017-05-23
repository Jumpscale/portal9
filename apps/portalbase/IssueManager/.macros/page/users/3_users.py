def main(j, args, params, tags, tasklet):
    page = args.page
    modifier = j.portal.tools.html.htmlfactory.getPageModifierGridDataTables(page)

    macrostr = args.macrostr.strip().strip('{{').strip('}}')
    tags = j.data.tags.getObject(macrostr, keepcase=True)
    tags = tags.getDict()
    tags.pop(args.macro)


    def _formatdata(users):
        aaData = list()
        for user in users:
            user = user.dictFiltered
            itemdata = ['<a href="%s">%s</a>' % (user['gitHostRefs'][0]['url'], user['name'])]
            itemdata.append(user.get('fullname', ''))
            itemdata.append('<a href="/issuemanager/Kanban?assignees=%s">issues</a>' % user['name'])

            aaData.append(itemdata)
        return aaData


    fieldnames = ["Name", "Full Name", "Issues"]

    user_collection = j.tools.issuemanager.getUserCollectionFromDB()
    data = _formatdata(user_collection.find(**tags))

    tableid = modifier.addTableFromData(data, fieldnames)
    modifier.addSearchOptions('#%s' % tableid)

    params.result = page

    return params


def match(j, args, params, tags, tasklet):
    return True

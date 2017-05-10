
def main(j, args, params, tags, tasklet):
    doc = args.doc

    macrostr = args.macrostr.strip().strip('{{').strip('}}')
    tags = j.data.tags.getObject(macrostr, keepcase=True)
    tags = tags.getDict()
    tags.pop(args.macro)

    groupon = tags.pop('groupon', 'assignees')
    data_collection = dict()

    schema = j.tools.issuemanager.getIssueSchema()
    issue_fileds = schema.schema.fields.keys()
    if groupon not in issue_fileds:
        args.doc.applyTemplate({'data_collection': "Issues cannot be grouped on \"%s\"" % groupon})
        params.result = (args.doc, args.doc)
        return params


    issues = j.tools.issuemanager.getIssueCollectionFromDB()
    users = j.tools.issuemanager.getUserCollectionFromDB()

    if 'assignees' in tags:
        userid = users.find(name=tags['assignees'])
        if userid:
            userid = userid[0].key
            tags['assignees'] = userid

    user_to_id = {user.key: user.dbobj.name for user in users.find()}

    for issue in issues.find(**tags):
        if groupon == 'assignees':
            assignees = issue.dbobj.assignees or 'No assignees'
            for assignee in assignees: # list
                assignee = user_to_id.get(assignee, 'no assignees')
                data_collection.setdefault(assignee, {'resolved': [], 'closed': [], 'wontfix': [], 'inprogress': [], 'question':[], 'new':[]})

                issue_dict = issue.to_dict()
                data_collection[assignee][issue_dict['state']].append(issue_dict)
        else:
            data = str(getattr(issue.dbobj, groupon)) or 'no %s' % groupon
            data_collection.setdefault(data, {'resolved': [], 'closed': [], 'wontfix': [], 'inprogress': [], 'question':[], 'new':[]})
            issue = issue.to_dict()
            data_collection[data][issue['state']].append(issue)

    out = "{{report:\n%s \n}}" % j.data.serializer.yaml.dumps(data_collection)
    params.result = (out, args.doc)

    return params


def match(j, args, params, tags, tasklet):
    return True

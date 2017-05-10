
def main(j, args, params, tags, tasklet):
    from collections import OrderedDict
    doc = args.doc

    macrostr = args.macrostr.strip().strip('{{').strip('}}')
    tags = j.data.tags.getObject(macrostr, keepcase=True)
    tags = tags.getDict()
    tags.pop(args.macro)

    groupon = tags.pop('groupon', 'creationTime')
    ranges = tags.pop('ranges', '')
    ranges = ranges.split(',')

    data_collection = OrderedDict()

    schema = j.tools.issuemanager.getIssueSchema()
    issue_fileds = schema.schema.fields.keys()
    if groupon not in issue_fileds:
        args.doc.applyTemplate({'data_collection': "Issues cannot be grouped on \"%s\"" % groupon})
        params.result = (args.doc, args.doc)
        return params

    if groupon not in ['creationTime', 'modTime']:
        args.doc.applyTemplate({'data_collection': "Issues with time cannot be grouped on \"%s\". Can only be grouped on creationTime or modTime. Please use issue_reports macro instead" % groupon})
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

    filtered_issues = OrderedDict()

    def epoch(val):
        if val != '0' and not val.startswith('-'):
            val = "-{}".format(val)
        return j.data.time.getEpochAgo(val)

    slices = [j.data.time.epoch]
    slices.extend([epoch(item) for item in ranges])
    slices.append(0)

    for idx, span in enumerate(slices[:-1]):

        tags[groupon] = [slices[idx + 1], span]

        range_from = ranges[idx - 1] if idx != 0 else 'now'
        range_to = ranges[idx] if slices[idx+1] != 0 else 'the beginning of time'

        filtered_issues['%s -- %s' % (range_from, range_to)] = issues.find(**tags)

    for span, issues in filtered_issues.items():
        for issue in issues:
            data_collection.setdefault(span, {'resolved': [], 'closed': [], 'wontfix': [], 'inprogress': [], 'question':[], 'new':[]})
            issue = issue.to_dict()
            issue['modTime'] = j.data.time.epoch2HRDateTime(issue['modTime'])
            data_collection[span][issue['state']].append(issue)

    out = "{{report:\n%s \n}}" % j.data.serializer.yaml.dumps(data_collection)
    params.result = (out, args.doc)

    return params


def match(j, args, params, tags, tasklet):
    return True

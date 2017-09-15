def main(j, args, params, tags, tasklet):
    page = args.page

    filters = dict()
    fieldids = ['timestamp', 'user', 'call', 'statuscode']
    for tag, val in args.tags.tags.items():
        if tag in fieldids:
            val = args.getTag(tag)
            filters[tag] = val
        else:
            val = args.getTag(tag)
            filters["tags"] = {"$regex": ("%s|(?=.*%s:%s)" % (filters["tags"]['$regex'], tag, val))} if "tags" in filters else {"$regex":"(?=.*%s:%s)" % (tag, val)}

    modifier = j.portal.tools.html.htmlfactory.getPageModifierGridDataTables(page)

    def makeTime(row, field):
        time = modifier.makeTime(row, field)
        link = "[%s|/system/audit?id=%s]" % (time, row.id)
        return link

    fields = [
        {'name': 'Time',
         'type': 'date',
         'id': 'timestamp',
         'value': makeTime},
        {'name': 'User',
         'id': 'user',
         'value': 'user'},
        {'name': 'Call',
         'id': 'call',
         'value': 'call'},
        {'name': 'Response Time',
         'id': 'responsetime',
         'type': 'int',
         'filterable': False,
         'value': '%(responsetime).3f seconds'},
        {'name': 'Status Code',
         'id': 'status_code',
         'type': 'int',
         'value': 'status_code'},
    ]
    tableid = modifier.addTableFromModel('system', 'Audit', fields, filters)
    modifier.addSearchOptions('#%s' % tableid)
    modifier.addSorting('#%s' % tableid, 1, 'desc')

    params.result = page
    return params

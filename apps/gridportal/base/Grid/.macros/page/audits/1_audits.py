import datetime

def main(j, args, params, tags, tasklet):
    page = args.page

    filters = dict()
    fieldids = ['timestamp', 'user', 'call', 'status_code']
    for tag, val in args.tags.tags.items():
        if tag in fieldids:
            val = args.getTag(tag)
            filters[tag] = val

    modifier = j.portal.tools.html.getPageModifierGridDataTables(page)

    def makeTime(row, field):
        time = modifier.makeTime(row, field)
        link = "[%s|audit?id=%s]" % (time, row['id'])
        return link

    fieldnames = ['Time', 'User', 'Call', 'Status Code']
    fieldvalues = [makeTime, 'user', 'call', 'status_code']
    tableid = modifier.addTableForModel('system', 'audit', fieldids, fieldnames, fieldvalues, filters)
    modifier.addSearchOptions('#%s' % tableid)
    modifier.addSorting('#%s' % tableid, 0, 'desc')

    params.result = page
    return params


def match(j, args, params, tags, tasklet):
    return True

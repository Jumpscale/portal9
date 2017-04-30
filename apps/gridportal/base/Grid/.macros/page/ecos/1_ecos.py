import datetime

def main(j, args, params, tags, tasklet):
    page = args.page
    modifier = j.portal.tools.html.getPageModifierGridDataTables(page)

    filters = dict()
    for tag, val in args.tags.tags.items():
        val = args.getTag(tag)
        if tag == 'from' and val:
            filters['from_'] = {'name': 'lasttime', 'value': j.data.time.getEpochAgo(val), 'eq': 'gte'}
        elif tag == 'to' and val:
            filters['to'] = {'name': 'lasttime', 'value': j.data.time.getEpochAgo(val), 'eq': 'lte'}
        elif val:
            if j.data.types.int.checkString(val):
                val = j.data.types.int.fromString(val)
            filters[tag] = val
    fieldnames = ['Time', 'Grid ID', 'Node ID', 'App Name', 'Error Message', 'Type', 'Level', 'Occurences', 'Job ID']

    def errormessage(row, field):
        if row[field]:
            return "<xmp>%s</xmp>" % row[field]

    def makeTime(row, field):
        time = modifier.makeTime(row, field) 
        return '[%s|error condition?id=%s]' % (time, row['id'])

    def makeJob(row, field):
        jid = row[field]
        if not jid:
            return 'N/A'
        return '[Details|job?id=%s]' % (jid)

    def level(row, field):
        value = row[field]
        return "%s (%s)" % (j.errorconditionhandler.getLevelName(value), value)

    def appName(row, field):
        return row[field].split(':')[-1]

    nidstr = '[%(nid)s|grid node?nid=%(nid)s&gid=%(gid)s]'

    fieldids = ["lasttime", "gid", "nid", "appname", "errormessage", 'type', 'level', 'occurrences', "jid"]
    fieldvalues = [makeTime, 'gid', nidstr, appName, errormessage, 'type', level, 'occurrences', makeJob]
    tableid = modifier.addTableForModel('system', 'errorcondition', fieldids, fieldnames, fieldvalues, filters)
    modifier.addSearchOptions('#%s' % tableid)
    modifier.addSorting('#%s' % tableid, 0, 'desc')


    params.result = page

    return params


def match(j, args, params, tags, tasklet):
    return True

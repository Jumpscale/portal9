import datetime

def main(j, args, params, tags, tasklet):
    page = args.page
    modifier = j.portal.tools.html.getPageModifierGridDataTables(page)

    filters = dict()
    for tag, val in args.tags.tags.items():
        val = args.getTag(tag)
        if tag == 'from' and val:
            filters['epoch'] = {'$gte': j.data.time.getEpochAgo(val)}
        elif tag == 'to' and val:
            filters['epoch'] = {'$lte': j.data.time.getEpochAgo(val)}
        elif tag in ('gid', 'nid') and val:
            filters[tag] = int(val)
        elif val:
            filters[tag] = val

    fieldnames = ['Start Time', 'App Name', 'Category', 'Message', 'Level', 'Process ID', 'Node ID', 'Job ID']

    def makeTime(row, field):
        time = modifier.makeTime(row, field)
        return '[%s|log?id=%s]' % (time, row['id'])

    def cleanUp(row, field):
        if row[field]:
            return j.portal.tools.html.escape(row[field])

    def pidStr(row, field):
        if row[field]:
            return '[%(pid)s|/grid/process?id=%(pid)s]' % row
        else:
            return ''


    nidstr = '[%(nid)s|/grid/grid node?nid=%(nid)s&gid=%(gid)s]'
    jidstr = '[%(jid)s|/grid/job?id=%(jid)s]'
    fieldids = ['epoch', 'appname', 'category', 'message', 'level', 'pid', 'nid', 'jid']
    fieldvalues = [makeTime, 'appname', 'category', cleanUp, 'level', pidStr, nidstr, jidstr]
    tableid = modifier.addTableForModel('system', 'log', fieldids, fieldnames, fieldvalues, filters)
    modifier.addSearchOptions('#%s' % tableid)
    modifier.addSorting('#%s' % tableid, 0, 'desc')


    params.result = page

    return params


def match(j, args, params, tags, tasklet):
    return True

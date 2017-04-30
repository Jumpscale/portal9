import datetime

def main(j, args, params, tags, tasklet):

    page = args.page
    modifier = j.portal.tools.html.getPageModifierGridDataTables(page)
    nid = args.getTag('nid')

    filters = dict()
    if nid:
        filters['nid'] = int(nid)
    filters['active'] = True

    fieldids = ["sname", "nid", "aysname", "aysdomain", "epochstart"]
    fieldnames = ['Name', 'Node', 'Process Name', 'Process Domain', 'Start']
    def pidFormat(row, field):
        name = row['sname'] or row['pname']
        return '[%s|/grid/process?id=%s&name=%s]' % (name, row['id'], name)

    nidstr = '[%(nid)s|/grid/grid node?nid=%(nid)s&%(gid)s]'
    fieldvalues = [pidFormat, nidstr, 'aysname', 'aysdomain', modifier.makeTime]
    tableid = modifier.addTableForModel('system', 'process', fieldids, fieldnames, fieldvalues, filters)
    modifier.addSearchOptions('#%s' % tableid)
    params.result = page
    return params


def match(j, args, params, tags, tasklet):
    return True

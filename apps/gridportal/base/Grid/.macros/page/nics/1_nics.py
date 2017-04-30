import datetime

def main(j, args, params, tags, tasklet):
    page = args.page
    modifier = j.portal.tools.html.getPageModifierGridDataTables(page)

    filters = dict()
    for tag, val in args.tags.tags.items():
        val = args.getTag(tag)
        if tag == 'from' and val:
            filters['lastcheck'] = {'$gte': j.data.time.getEpochAgo(val)}
        elif tag == 'to' and val:
            filters['lastcheck'] = {'$lte': j.data.time.getEpochAgo(val)}
        elif val:
            if j.data.types.int.checkString(val):
                val = j.data.types.int.fromString(val)
            filters[tag] = val
    fieldnames = ['Name', 'IP Address', 'Mac Address', 'Last Checked']

    nicstr = '[%(name)s|nic?id=%(id)s&name=%(name)s&nid=%(nid)s]'
    fieldids = ['name', 'ipaddr', 'mac', 'lastcheck']
    fieldvalues = [nicstr,'ipaddr','mac',modifier.makeTime]
    tableid = modifier.addTableForModel('system', 'nic', fieldids, fieldnames, fieldvalues, filters)
    modifier.addSearchOptions('#%s' % tableid)
    modifier.addSorting('#%s' % tableid, 0, 'desc')


    params.result = page

    return params


def match(j, args, params, tags, tasklet):
    return True

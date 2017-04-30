
def main(j, args, params, tags, tasklet):
    page = args.page
    modifier = j.portal.tools.html.getPageModifierGridDataTables(page)
    ecofilter = args.getTag('eco')
    filters = None
    if ecofilter:
        filters = {'errorconditions':ecofilter}

    def makeDetails(row, field):
        data = modifier.makeTime(row, field)
        return '<a href=alert?id=%s>%s</a>' % (row['id'], data)

    
    fieldnames = ('Last Time', 'Description', 'Raise Time','Close Time', 'State', 'Username')
    fieldids = ['lasttime', 'description', 'inittime', 'closetime', 'state', 'username']
    fieldvalues = (makeDetails, 'description', modifier.makeTime, modifier.makeTime, 'state', 'username')

    tableid = modifier.addTableForModel('system', 'alert', fieldids, fieldnames, fieldvalues, filters)

    modifier.addSearchOptions('#%s' % tableid)
    modifier.addSorting('#%s' % tableid, 0, 'desc')

    params.result = page
    return params

def match(j, args, params, tags, tasklet):
    return True

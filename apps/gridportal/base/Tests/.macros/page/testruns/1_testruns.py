import datetime

def main(j, args, params, tags, tasklet):

    page = args.page
    filters = dict()

    modifier = j.portal.tools.html.getPageModifierGridDataTables(page)

    def makeLink(row, field):
        return '[%s|/tests/testrun?id=%s]' % (row['name'], row['id'])

    fieldnames = ['Name', 'Starttime', 'Endtime', 'State', 'Categories', 'License', 'Organization', 'Description']
    fieldvalues = [makeLink, modifier.makeTime, modifier.makeTime, 'state', 'categories', 'license', 'organization', 'description']
    fieldids = ['name', 'starttime', 'endtime', 'state', 'categories', 'license', 'organization', 'description']
    tableid = modifier.addTableForModel('system', 'test', fieldids, fieldnames, fieldvalues, filters)
    modifier.addSearchOptions('#%s' % tableid)

    params.result = page
    return params


def match(j, args, params, tags, tasklet):
    return True


def main(j, args, params, tags, tasklet):
    page = args.page
    modifier = j.portal.tools.html.getPageModifierGridDataTables(page)

    fieldnames = ['Grid ID', 'Name', 'IP Address', 'Roles']
    filters = dict()
    for tag, val in args.tags.tags.items():
        if tag in ('gid', ) and val and not val.startswith("$$"):
            filters['gid'] = int(val)
    if args.getTag('roles'):
        filters['roles'] = args.getTag('roles')

    namelink = '[%(name)s|/grid/Grid Node?id=%(id)s&gid=%(gid)s&nid=%(nid)s]'

    fieldvalues = ['gid', namelink,'ipaddr', 'roles']
    fieldids = ['gid', 'name', 'ipaddr', 'roles']
    tableid = modifier.addTableForModel('system', 'node', fieldids, fieldnames, fieldvalues, filters)
    modifier.addSearchOptions('#%s' % tableid)
    params.result = page

    return params


def match(j, args, params, tags, tasklet):
    return True

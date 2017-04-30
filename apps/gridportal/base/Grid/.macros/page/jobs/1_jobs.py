def main(j, args, params, tags, tasklet):
    page = args.page
    nid = args.getTag("nid")
    if not nid and args.tags.tagExists('nid'):
        page.addMessage('Missing node id param "nid"')
        params.result = page
        return params

    filters = dict()
    for tag, val in args.tags.tags.items():
        val = args.getTag(tag)
        if not val:
            continue
        if tag == 'from' and val:
            filters['starttime'] = {'$gte': j.data.time.getEpochAgo(val)}
        elif tag == 'jsname':
            filters['cmd'] = val
        elif tag in ('nid', 'gid') and val:
            filters[tag] = int(val)
        elif tag == 'filter':
            filter = j.data.serializer.json.loads(val or 'null')
            filters.update(filter)
        elif val:
            filters[tag] = val

    modifier = j.portal.tools.html.getPageModifierGridDataTables(page)
    def makeLink(row, field):
        row['starttime'] = row['starttime'] / 1000
        time = modifier.makeTime(row, field)
        return '[%s|/grid/job?id=%s]'  % (time, row['id'])

    def makeArgs(row, field):
        args = row[field]

        value = '{name} {args}'.format(
            name=args.get('name', ''),
            args=', '.join(args.get('args', [])),
        )

        return value

    def makeRoles(row, field):
        roles = row[field]
        return ', '.join(roles)

    fieldnames = ['Time Start', 'Command', 'Arguments', 'Data', 'Gid', 'Nid', 'Roles']
    fieldvalues = [makeLink, 'cmd', makeArgs, 'data', 'gid', 'nid', makeRoles]
    fieldids = ['starttime', 'cmd', 'args', 'data', 'gid', 'nid', 'roles']

    tableid = modifier.addTableForModel('system', 'command', fieldids, fieldnames, fieldvalues, nativequery=filters)
    modifier.addSearchOptions('#%s' % tableid)
    modifier.addSorting('#%s' % tableid, 0, 'desc')

    params.result = page
    return params


def match(j, args, params, tags, tasklet):
    return True

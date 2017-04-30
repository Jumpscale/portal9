def main(j, args, params, tags, tasklet):
    page = args.page
    modifier = j.portal.tools.html.getPageModifierGridDataTables(page)

    filters = dict()
    for tag, val in args.tags.tags.items():
        val = args.getTag(tag)
        if val:
            if val.isdigit():
                filters[tag] = int(val)
            else:
                filters[tag] = val

    def _getDiskUsage(disk, field):
        diskfree = disk[field]
        disksize = disk['size']
        if not disksize or not diskfree:
            diskusage = 'N/A'
        else:
            diskusage = '%s%%' % (int(100.0 * diskfree / disksize))
        return diskusage

    def _diskSize(disk, field):
        if disk.size:
             return "%.2f %siB" % j.data.units.bytes.converToBestUnit(disk.size, 'M')
        else:
            return "0"

    fieldnames = ["Path", "Size", "Mount Point", "SSD", "Free", "Mounted"]
    path = '[%(path)s|/grid/disk?id=%(id)s&nid=%(nid)s&gid=%(gid)s]'
    fieldids = ['path', 'size', 'mountpoint', 'ssd', 'free', 'mounted']
    fieldvalues = [path, _diskSize, 'mountpoint', 'ssd', _getDiskUsage, 'mounted']
    tableid = modifier.addTableForModel('system', 'disk', fieldids, fieldnames, fieldvalues, filters)
    modifier.addSearchOptions('#%s' % tableid)

    params.result = page

    return params


def match(j, args, params, tags, tasklet):
    return True

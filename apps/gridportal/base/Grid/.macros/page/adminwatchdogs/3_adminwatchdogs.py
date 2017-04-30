def main(j, args, params, tags, tasklet):
    def _formatdata(watchdogs):
        aaData = list()
        for name, watchdog in watchdogs.items():
            itemdata = list()
            link = '<a href=adminwatchdog?name=%s>Details</a>' % name if watchdog['state'] == 'CRITICAL' else ''
            node = '<a href=grid node?nid=%s>%s</a>' % (watchdog['nid'], watchdog['nid'])
            grid = '<a href=grid?id=%s>%s</a>' % (watchdog['gid'], watchdog['gid'])
            epochHR = j.data.time.epoch2HRDateTime(watchdog['epoch']) if watchdog['epoch'] else 'N/A'
            epochEsc = j.data.time.epoch2HRDateTime(watchdog['escalationepoch']) if watchdog['escalationepoch'] else 'N/A'
            if watchdog['state']:
                color = 'green' if watchdog['state'] == 'OK' else ('red' if watchdog['state'] == 'CRITICAL' else 'orange')
                state =  '<font color="%s">%s</font>' % (color, watchdog['state'])
            else:
                state = 'N/A'
            for field in [watchdog['category'], state, epochHR, epochEsc, watchdog['escalationstate'], grid, node, watchdog['ecoguid'], link]:
                itemdata.append(str(field))
            aaData.append(itemdata)
        return aaData

    cl = j.clients.redis.getGeventRedisClient("localhost", 7770)

    if not j.application.config.exists("grid.watchdog.secret") or j.application.config.get("grid.watchdog.secret") == "":
        page = args.page
        page.addMessage('* no grid configured for watchdog: hrd:grid.watchdog.secret')
        params.result = page
        return params


    watchdogevents = cl.hgetall('watchdogevents:%s' % j.application.config.get("grid.watchdog.secret"))
    watchdogs = dict([(watchdogevents[i], j.data.serializer.json.loads(watchdogevents[i+1])) for i, _ in enumerate(watchdogevents) if i % 2 == 0])

    tabledata = _formatdata(watchdogs)


    page = args.page
    modifier = j.portal.tools.html.getPageModifierGridDataTables(page)

    fieldnames = ('Category', 'State', 'Raise Time', 'Escalation Time', 
                  'Escalation State', 'Grid ID', 'Node ID', 'ECO ID', 'Link to Watchdog')
    tableid = modifier.addTableFromData(tabledata, fieldnames)

    modifier.addSearchOptions('#%s' % tableid)
    modifier.addSorting('#%s' % tableid, 0, 'desc')

    params.result = page
    return params


def match(j, args, params, tags, tasklet):
    return True

def main(j, args, params, tags, tasklet):
    def _formatdata(nodes):
        # data = [node for idx, node in enumerate(nodes) if idx%2 == 1]
        aaData = list()
        for node in nodes:
            node = j.data.serializer.json.loads(node)
            itemdata = list()
            for field in ['gridname', 'name', 'enabled', 'ip', 'roles', 'lastcheck', 'remark']:
                value = node[field]
                if field == 'lastcheck':
                    value = j.data.time.epoch2HRDateTime(value) if value else 'N/A'
                elif field == 'roles':
                    value = ', '.join(value)
                elif field == 'name':
                    value = '<a href=adminnode?gridname=%s&name=%s>%s</a>' % (node['gridname'], value, value)
                itemdata.append(str(value))
            aaData.append(itemdata)
        return aaData

    cl = j.clients.redis.getGeventRedisClient("localhost", 7770)

    if not j.application.config.exists("grid.watchdog.secret") or j.application.config.get("grid.watchdog.secret") == "":
        page = args.page
        page.addMessage('* no grid configured for watchdog: hrd:grid.watchdog.secret')
        params.result = page
        return params



    key = "%s:admin:nodes" % j.application.config.get("grid.watchdog.secret")
    hosts=[item.split(":")[-1] for item in cl.keys(key+"*")]

    allnodes = list()
    for host in hosts:
        nodes = cl.hgetall('%s:%s' % (key, host))
        allnodes.extend([node for idx, node in enumerate(nodes) if idx%2 == 1])
    
    resultdata = _formatdata(allnodes)

    page = args.page
    modifier = j.portal.tools.html.getPageModifierGridDataTables(page)

    fieldnames = ('Grid Name', 'Name', 'Enabled', 'IP', 'Roles', 'Last Checked', 'Remark')
    #'cuapi', 'actionsDone', 'passwd', 'args', 'enable', 'error', 'result', 'host', basepath
    tableid = modifier.addTableFromData(resultdata, fieldnames)

    modifier.addSearchOptions('#%s' % tableid)
    modifier.addSorting('#%s' % tableid, 0, 'asc')

    params.result = page
    return params


def match(j, args, params, tags, tasklet):
    return True

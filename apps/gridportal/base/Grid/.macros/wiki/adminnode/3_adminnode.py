def main(j, args, params, tags, tasklet):
    params.merge(args)
    doc = params.doc

    gridname = args.getTag('gridname')
    name = args.getTag('name')

    for paramname, param in {'gridname':gridname, 'name':name}.items():
        if not param:
            out = 'Missing alert param "%s"' % paramname
            params.result = (out, args.doc)
            return params            

    cl = j.clients.redis.getGeventRedisClient("localhost", 7770)

    if not j.application.config.exists("grid.watchdog.secret") or j.application.config.get("grid.watchdog.secret") == "":
        page = args.page
        page.addMessage('* no grid configured for watchdog: hrd:grid.watchdog.secret')
        params.result = page
        return params


    node = cl.hget('%s:admin:nodes:%s' % (j.application.config.get("grid.watchdog.secret"), gridname), name)

    out = list()
    properties = [('Grid Name', 'gridname'), ('Name', 'name'), ('Enabled', 'enabled'),
                  ('IP', 'ip'), ('Roles', 'roles'), ('Last Checked', 'lastcheck'), 
                  ('Remark', 'remark'), 
                  ('Password', 'passwd'),  ('Enable', 'enable'), 
                  ('Host', 'host')]

    node = j.data.serializer.json.loads(node)
    for printable, field in properties:
        v = node[field]
        if isinstance(v, list):
            v = ', '.join(v)
        elif field in ['lastcheck']:
            v = j.data.time.epoch2HRDateTime(v) if v else 'N/A'
        elif field in ['enabled']:
            color = 'green' if v  else 'red' 
            v = '{color:%s}%s{color}' % (color, v)
        out.append("|*%s*|%s|" % (printable, v))

    out = '\n'.join(out)
    params.result = (out, doc)
    return params


def match(j, args, params, tags, tasklet):
    return True

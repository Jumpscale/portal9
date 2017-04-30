def main(j, args, params, tags, tasklet):
    params.merge(args)
    doc = params.doc

    name = args.getTag('name')

    if not name:
        out = 'Missing alert param "name"'
        params.result = (out, args.doc)
        return params            

    cl = j.clients.redis.getGeventRedisClient("localhost", 7770)

    if not j.application.config.exists("grid.watchdog.secret") or j.application.config.get("grid.watchdog.secret") == "":
        page = args.page
        page.addMessage('* no grid configured for watchdog: hrd:grid.watchdog.secret')
        params.result = page
        return params


    jscript = cl.hget('%s:admin:jscripts' % j.application.config.get("grid.watchdog.secret"), name)
    jscript = j.data.serializer.json.loads(jscript)

    out = ['|*JScript Name*|%s|' % name]
    for key, value in jscript.items():
        if key == 'code':
            continue
        out.append("|*%s*|%s|" % (key.capitalize(), value))

    out.append('{{\ncode:\n%s\n}}' % jscript['code'])

    out = '\n'.join(out)
    params.result = (out, doc)
    return params


def match(j, args, params, tags, tasklet):
    return True

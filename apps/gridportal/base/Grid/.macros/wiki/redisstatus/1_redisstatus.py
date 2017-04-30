def main(j, args, params, tags, tasklet):
    doc = args.doc
    nid = args.getTag('nid')
    nidstr = str(nid)
    rediscl = j.clients.redis.getByInstance('system')

    out = list()

    out.append('||Port||Status||Memory Used||')

    rstatus = rediscl.hget('healthcheck:monitoring', 'results')
    errors = rediscl.hget('healthcheck:monitoring', 'errors')
    rstatus = j.data.serializer.json.loads(rstatus) if rstatus else dict()
    errors = j.data.serializer.json.loads(errors) if errors else dict()

    for data in [rstatus, errors]:
        if nidstr in data:
            if 'redis' in data.get(nidstr, dict()):
                rnstatus = data[nidstr].get('redis', dict())
                for stat in rnstatus:
                    if 'state' not in stat:
                        continue
                    state = j.core.grid.healthchecker.getWikiStatus(stat.get('state', 'UNKNOWN'))
                    usage = "%s / %s" % (stat.get('memory_usage', ''), stat.get('memory_max', ''))
                    out.append('|%s|%s|%s|' % (stat.get('port', -1), state, usage))

    out = '\n'.join(out)

    params.result = (out, doc)
    return params


def match(j, args, params, tags, tasklet):
    return True



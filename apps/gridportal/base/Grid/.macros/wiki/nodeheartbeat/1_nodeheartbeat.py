def main(j, args, params, tags, tasklet):
    doc = args.doc
    nid = args.getTag('nid')
    nidstr = str(nid)
    rediscl = j.clients.redis.getByInstance('system')

    out = list()

    workers = rediscl.hget('healthcheck:monitoring', 'results')
    errors = rediscl.hget('healthcheck:monitoring', 'errors')
    workers = j.data.serializer.json.loads(workers) if workers else dict()
    errors = j.data.serializer.json.loads(errors) if errors else dict()

    def render(data, color):
        nodedata = data.get(nidstr, dict())
        wdata = nodedata.get('heartbeat', list())
        for stat in wdata:
            if isinstance(stat, dict):
                msg = stat.get('errormessage', 'UNKNOWN')
            else:
                msg = stat
            out.append("{color:%s}*%s*{color}" % (color,msg))

    render(workers, 'green')
    render(errors, 'red')

    out = '\n'.join(out)
    params.result = (out, doc)
    return params


def match(j, args, params, tags, tasklet):
    return True



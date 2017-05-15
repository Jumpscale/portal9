
def main(j, args, params, tags, tasklet):
    params.merge(args)

    doc = params.doc
    host = j.portal.tools.server.active.dns
    out = "<iframe src='%s' width='%s' height='%s'></iframe>" % (
        '/lib/elasticsearch-head/index.html?base_uri=http://%s:9200' % host, '100%', '800px')

    params.result = (out, doc)

    return params


def match(j, args, params, tags, tasklet):
    return True

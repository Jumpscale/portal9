import datetime

def main(j, args, params, tags, tasklet):

    params.merge(args)
    doc = params.doc
    # tags = params.tags

    passwd = j.application.config.get("grid.master.superadminpasswd")
    osis = j.clients.osis.get(j.application.config.get("grid.master.ip"), passwd=passwd, user='root')
    osis_test = j.clients.osis.getCategory(osis,"system","test")

    tid = args.getTag('id')
    if not tid:
        out = 'Test id needs to be specified, param name:id'
        params.result = out, doc
        return params

    tests = osis_test.simpleSearch({'id': tid})
    if not tests:
        out = 'Could not find test with id %s' % tid
        params.result = out, doc
        return params

    obj = tests[0]
    db = j.servers.kvs.getMemoryStore('cache')
    cachekey = j.base.idgenerator.generateGUID()

    def getData(id_):
        for ttime in ('starttime', 'endtime'):
            if obj[ttime] == 0:
                obj[ttime] = ""
            else:
                obj[ttime] = datetime.datetime.fromtimestamp(obj[ttime]).strftime('%Y-%m-%d %H:%M:%S')

        obj['categories'] = ', '.join(obj["categories"])
        obj['cachekey'] = cachekey
        db.cacheSet(cachekey, obj)
        return obj

    push2doc=j.portal.tools.macrohelper.push2doc
    return push2doc(args, params, getData)

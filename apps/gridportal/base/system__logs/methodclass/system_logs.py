from js9 import j


class system_logs(j.tools.code.classGetBase()):

    def __init__(self):
        self._te = {}
        self.actorname = "logs"
        self.appname = "system"

    def listJobs(self, **args):

        nip = 'localhost'
        if args.get('nip'):
            nip = args.get('nip')
        params = {'ffrom': '', 'to': '', 'nid': '', 'gid': '', 'roles': ''}
        for p in params:
            params[p] = args.get(p)

        if not any(params.values()):
            commands = j.data.models.system.Command.find({})
        else:
            if params['ffrom']:
                ffrom = params.pop('ffrom')
                starting = j.data.time.getEpochAgo(ffrom)
                query = {'starttime': {'$gte': starting}}
            if params['to']:
                to = params.pop('to')
                ending = j.data.time.getEpochAgo(to)
                if query:
                    query['starttime']['$lte'] = ending
                else:
                    query = {'starttime': {'lte': ending}}
            if params['roles']:
                roles = params.pop('roles')
                query['roles'] = roles
            for k, v in params.items():
                if v:
                    query[k] = v

            commands = j.data.models.system.Command.find(query)

        aaData = list()
        fields = ('cmd', 'args', 'roles', 'jobs')
        for item in commands:
            itemdata = list()
            for field in fields:
                itemdata.append(item['_source'].get(field))
            itemargs = j.data.serializer.serializers.json.loads(item['_source'].get('args', {}))
            itemdata.append('<a href=%s>%s</a>' % ('/gridlogs/job?jobid=%s' % item['_id'], itemargs.get('msg', '')))
            result = item['_source'].get('result', '{}')
            result = j.data.serializer.serializers.json.loads(result if result else '{}')
            itemdata.append(result)
            aaData.append(itemdata)
        return {'aaData': aaData}

    def listNodes(self, **args):
        nodes = j.data.models.system.Node.find({})

        aaData = list()
        fields = ('name', 'roles', 'ipaddr', 'machineguid')
        for node in nodes:
            itemdata = list()
            for field in fields:
                itemdata.append(node[field])
            itemdata.append(node['id'])
            ipaddr = node['ipaddr'] if node['ipaddr'] else ''
            itemdata.append('<a href="/grid/grid node?nip=%s">link</a>' % ipaddr)
            aaData.append(itemdata)
        return {'aaData': aaData}

    def listECOs(self, **args):

        nid = 1
        if args.get('nip'):
            nid = args.get('nid')
        query = {"nid": nid}
        ecos = j.data.models.Errorcondition.find(query)

        aaData = list()
        fields = ('appname', 'category', 'lasttime', 'errormessage', 'jid', 'level', 'backtrace', 'nid', 'pid')

        for item in ecos['hits']['hits']:
            itemdata = list()
            for field in fields:
                itemdata.append(item['_source'].get(field))
            aaData.append(itemdata)

        if not aaData:
            aaData = [None, None, None, None, None]
        return {'aaData': aaData}

    def listLogs(self, **args):

        query = 'null'
        if args.get('nid'):
            nid = args.get('nid')
            query = {"nid": nid}

        logs = j.data.models.system.Log.find(query)

        aaData = list()
        fields = ('appname', 'category', 'epoch', 'message', 'level', 'pid')

        for item in logs['hits']['hits']:
            itemdata = list()
            for field in fields:
                itemdata.append(item['_source'].get(field))
            aaData.append(itemdata)
        return {'aaData': aaData}

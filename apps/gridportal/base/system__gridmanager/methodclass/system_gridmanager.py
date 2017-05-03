from js9 import j


def mbToKB(value):
    if not value:
        return value
    return value * 1024


def getInt(val):
    if val is not None:
        return int(val)
    return val


class system_gridmanager(j.tools.code.classGetBase()):
    """
    gateway to grid
    """

    def __init__(self):
        self._te = {}
        self.actorname = "gridmanager"
        self.appname = "system"
        self.clients = {}
        self._nodeMap = dict()
        self.clientsIp = dict()

    def getQuery(self, params):
        query = {}
        for key, value in params.items():
            if 'None' not in str(value):
                query[key] = value
        return query

    def getClient(self, nid, category):
        nid = int(nid)
        if nid not in self.clients:
            if nid not in self._nodeMap:
                self.getNodes()
            if nid not in self._nodeMap:
                raise RuntimeError('Could not get client for node %s!' % nid)
            for ip in self._nodeMap[nid]['ipaddr']:
                if j.sal.nettools.tcpPortConnectionTest(ip, 4446):
                    user = "root"  # j.application.config.get('system.superadmin.login')
                    self.clients[nid] = j.servers.geventws.getClient(
                        ip, 4446, org="myorg", user=user, passwd='fake', category=category)
                    self.clientsIp[nid] = ip
                    return self.clients[nid]
            raise RuntimeError('Could not get client for node %s!' % nid)

        return self.clients[nid]

    def getNodeSystemStats(self, nid, **kwargs):
        """
        ask the right processmanager on right node to get the information about node system
        param:nid id of node
        result json
        """
        nid = int(nid)
        client = self.getClient(nid, 'stats')

        try:
            stats = client.listStatKeys('n%s.system.' % nid)
        except Exception as e:
            # from IPython import embed
            # print "DEBUG NOW getNodeSystemStats"
            # embed()
            pass

        cpupercent = [stats['n%s.system.cpu.percent' % nid][-1]]
        mempercent = [stats['n%s.system.memory.percent' % nid][-1]]
        netstat = [stats['n%s.system.network.kbytes.recv' % nid][-1], stats['n%s.system.network.kbytes.send' % nid][-1]]

        result = {'cpupercent': [cpupercent, {'series': [{'label': 'CPU PERCENTAGE'}]}],
                  'mempercent': [mempercent, {'series': [{'label': 'MEMORY PERCENTAGE'}]}],
                  'netstat': [netstat, {'series': [{'label': 'KBytes Recieved'}, {'label': 'KBytes Sent'}]}]}
        return result

    def getNodes(self, id=None, gid=None, nid=None, name=None, roles=None, ipaddr=None, macaddr=None,
                 active=None, peer_stats=None, peer_log=None, peer_backup=None, lastcheckFrom=None, lastcheckTo=None, **kwargs):
        """
        param:id str,,find based on id
        param:gid int,,find nodes for specified grid
        param:name str,,match on text in name
        param:roles str,,match on comma separated list of roles (subsets also ok e.g. kvm.  would match all roles starting with kvm.)
        param:ipaddr str,,comma separated list of ip addr to match against
        param:macaddr str,,comma separated list of mac addr to match against
        param:active bool,,True,is the node still active
        param:peer_stats int,,id of node which has stats for this node
        param:peer_log int,,id of node which has logs (e.g. transactionlogs) for this node
        param:peer_backup int,,id of node which has backups for this node
        param:lastcheckFrom str,-1h,-4d;-4w;-4m;-1h;-1s  d=day w=week m=month s=sec  find nodes with lastcheckFrom  (-4d means 4 days ago)
        param:lastcheckTo str,-1h,-4d;-4w;-4m;-1h;-1s  d=day w=week m=month s=sec  find nodes with lastcheckTo  (-4d means 4 days ago)
        result:list(list)
        """
        if id:
            results = j.data.models_system.Node.get(id)
        else:
            lastcheckFrom = self._getEpoch(lastcheckFrom)
            lastcheckTo = self._getEpoch(lastcheckTo)
            params = {'gid': getInt(gid),
                      'nid': getInt(nid),
                      'name': name,
                      'active': active,
                      'lastcheck': {'$gte': lastcheckFrom},
                      'lastcheck': {'$lte': lastcheckTo},
                      'peer_stats': peer_stats,
                      'peer_log': peer_log,
                      'peer_backup': peer_backup,
                      }
            params = self.getQuery(params)
            results = j.data.models_system.Node.find(params)

        def myfilter(node):
            self._nodeMap[node['id']] = node
            if roles and not set(roles).issubset(set(node['roles'])):
                return False
            if ipaddr and ipaddr not in node['ipaddr']:
                return False
            if macaddr and macaddr not in node['netaddr']:
                return False
            return True

        return list(filter(myfilter, results))

    def getProcessStats(self, nid, domain="", name="", **kwargs):
        """
        ask the right processmanager on right node to get the information
        param:nid id of node
        param:domain optional domain name for process
        param:name optional name for process
        result json
        """
        if domain == "*":
            domain = ""
        if name == "*":
            name = ""
        client = self.getClient(nid)
        return client.monitorProcess(domain=domain, name=name)

    def _showUnavailable(self, width, height, message="STATS UNAVAILABLE"):
        import PIL.Image as Image
        import PIL.ImageDraw as ImageDraw
        import io

        size = (int(width), int(height))
        im = Image.new('RGB', size, 'white')
        draw = ImageDraw.Draw(im)
        red = (255, 0, 0)
        text_pos = (size[0] / 2, size[1] / 2)
        text = message
        draw.text(text_pos, text, fill=red)

        del draw
        output = io.StringIO()
        im.save(output, 'PNG')
        del im
        response = output.getvalue()
        output.close()
        return response

    def getStatImage(self, statKey, title=None, aliases={}, width=500, height=250, **kwargs):
        """
        @param statkey e.g. n1.disk.mbytes.read.sda1.last
        """
        import urllib.request
        import urllib.parse
        import urllib.error
        query = list()
        ctx = kwargs['ctx']
        ctx.start_response('200', (('content-type', 'image/png'),))
        statKey = statKey.strip()

        for target in statKey.split(','):

            if target in aliases:
                target = "alias(%s, '%s')" % (target, aliases[target])
            query.append(('target', target))
        if title:
            query.append(('title', title))

        query.append(('height', height))
        query.append(('width', width))
        query.append(('lineWidth', '2'))
        query.append(('graphOnly', 'false'))
        query.append(('hidexAxes', 'false'))
        query.append(('hidexGrid', 'false'))
        query.append(('areaMode', 'none'))
        query.append(('tz', 'CET'))

        params = kwargs.copy()
        params.pop('ctx')
        for key, value in params.items():
            query.append((key, value))

        querystr = urllib.parse.urlencode(query)
        url = "http://127.0.0.1:8081/render?%s" % (querystr)
        r = requests.get(url)
        try:
            result = r.send()
        except Exception:
            return self._showUnavailable(width, height, "GRAPHITE UNAVAILABLE")
        return result.content

    def getProcessesActive(self, nid, name, domain, **kwargs):
        """
        ask the right processmanager on right node to get the info
        output all relevant info (no stat info for that we have getProcessStats)
        param:nid id of node (if not specified goes to all nodes and aggregates)
        param:name optional name for process name (part of process name)
        param:domain optional name for process domain (part of process domain)
        result json
        """
        client = self.getClient(nid)
        return client.getProcessesActive(domain, name)

    def getJob(self, includeloginfo, includechildren, id=None, **kwargs):
        """
        gets relevant info of job (also logs)
        can be used toreal time return job info
        param:id obliged id of job
        param:includeloginfo if true fetch all logs of job & return as well
        param:includechildren if true look for jobs which are children & return that info as well
        """
        # TODO include loginfo
        jobs = j.data.models_system.Job.get(id)
        job = jobs[0]
        return {'result': job}

    def getLogs(self, id=None, level=None, category=None, text=None, from_=None,
                to=None, jid=None, nid=None, gid=None, pid=None, tags=None, **kwargs):
        """
        interface to get log information
        param:id find based on id
        param:level level between 1 & 9; all levels underneath are found e.g. level 9 means all levels
        param:category match on multiple categories; are comma separated
        param:text match on text in body
        param:from_ -4d;-4w;-4m;-1h;-1s  d=day w=week m=month s=sec  find logs from date specified  (-4d means 4 days ago)
        param:to -4d;-4w;-4m;-1h;-1s  d=day w=week m=month s=sec  find logs to date specified
        param:jid find logs for specified jobid
        param:nid find logs for specified node
        param:gid find logs for specified grid
        param:pid find logs for specified process (on grid level)
        param:tags comma separted list of tags/labels
        """
        if id:
            return j.data.models_system.Logs.get(id)
        from_ = self._getEpoch(from_)
        to = self._getEpoch(to)
        params = {'level': {'$lte': level},
                  'category': category,
                  'message': text,
                  'epoch': {'$gte': from_},
                  'epoch': {'$lte': to},
                  'jid': jid,
                  'nid': getInt(nid),
                  'gid': getInt(gid),
                  'pid': pid,
                  'tags': tags,
                  }
        params = self.getQuery(params)
        return j.data.models_system.Log.find(params)

    def getJobs(self, id=None, from_=None, to=None, nid=None, gid=None, parent=None, roles=None, state=None,
                organization=None, name=None, description=None, category=None, source=None, **kwargs):
        """
        interface to get job information
        param:from_ -4d;-4w;-4m;-1h;-1s  d=day w=week m=month s=sec  find jobs from date specified  (-4d means 4 days ago)
        param:to -4d;-4w;-4m;-1h;-1s  d=day w=week m=month s=sec  find jobs to date specified
        param:nid find jobs for specified node
        param:gid find jobs for specified grid
        param:parent find jobs which are children of specified parent
        param:roles match on comma separated list of roles (subsets also ok e.g. kvm.  would match all roles starting with kvm.)
        param:state OK;ERROR;...
        param:jsorganization
        param:jsname
        param:description any description when asked for the job
        param:category category in dot notation
        param:source who asked for the job is free text
        """
        if id:
            return
        from_ = self._getEpoch(from_)
        to = self._getEpoch(to)
        params = {'starttime': {'$gte': from_},
                  'starttime': {'$lte': to},
                  'nid': getInt(nid),
                  'gid': getInt(gid),
                  'description': description,
                  'category': category,
                  'source': source,
                  'parent': parent,
                  'state': state,
                  'category': organization,
                  'cmd': name}
        return
        # return j.data.models_system.Job.find(params)

    def getErrorconditions(self, id=None, level=None, descr=None, descrpub=None, from_=None, to=None,
                           nid=None, gid=None, category=None, tags=None, type=None, jid=None, **kwargs):
        """
        interface to get errorcondition information (eco)
        param:id find based on id
        param:level level between 1 & 3; all levels underneath are found e.g. level 3 means all levels
        param:descr match on text in descr
        param:descrpub match on text in descrpub
        param:from_ -4d;-4w;-4m;-1h;-1s  d=day w=week m=month s=sec  find ecos from date specified  (-4d means 4 days ago)
        param:to -4d;-4w;-4m;-1h;-1s  d=day w=week m=month s=sec  find ecos to date specified
        param:nid find ecos for specified node
        param:gid find ecos for specified grid
        param:category match on multiple categories; are comma separated
        param:tags comma separted list of tags/labels
        param:type
        param:jid find ecos for specified job
        """
        if id:
            return j.data.models_system.Errorcondition.get(id)

        from_ = self._getEpoch(from_)
        to = self._getEpoch(to)
        params = {'lasttime': {'$gte': from_},
                  'lasttime': {'$lte': to},
                  'nid': getInt(nid),
                  'level': getInt(level),
                  'errormessage': descr,
                  'errormessagePub': descrpub,
                  'category': category,
                  'tags': tags,
                  'type': type,
                  'gid': getInt(gid),
                  'jid': jid}
        params = self.getQuery(params)
        return j.data.models_system.Errorcondition.find(params)

    def getProcesses(self, id=None, name=None, nid=None, gid=None, from_=None, to=None, active=None, aysdomain=None,
                     aysname=None, instance=None, systempid=None, lastcheckFrom=None, lastcheckTo=None, **kwargs):
        """
        list processes, are the grid unique processes (not integrated with processmanager yet)
        param:id find based on id

        param:name match on text in name
        param:nid find logs for specified node
        param:gid find logs for specified grid
        param:aid find logs for specified application type
        param:from_ -4d;-4w;-4m;-1h;-1s  d=day w=week m=month s=sec  find processes from date specified  (-4d means 4 days ago)
        param:to -4d;-4w;-4m;-1h;-1s  d=day w=week m=month s=sec  find processes to date specified
        param:aysdomain str.. AYS domain of process
        param:aysname str.. AYS name of process
        param:instance str.. instance of process
        param:systempid int.. pid on the system of process
        param:lastcheckFrom str,-1h,-4d;-4w;-4m;-1h;-1s  d=day w=week m=month s=sec  find processes with lastcheckFrom  (-4d means 4 days ago)
        param:lastcheckTo str,-1h,-4d;-4w;-4m;-1h;-1s  d=day w=week m=month s=sec  find processes with lastcheckTo  (-4d means 4 days ago)
        result list(list)
        """
        if id:
            return j.data.models_system.Process.get(id)
        from_ = self._getEpoch(from_)
        to = self._getEpoch(to)
        lastcheckFrom = self._getEpoch(lastcheckFrom)
        lastcheckTo = self._getEpoch(lastcheckTo)
        params = {'epochstart': {'$gte': from_},
                  'epochstart': {'$lte': to},
                  'lastcheck': {'$gte': lastcheckFrom},
                  'lastcheck': {'$lte': lastcheckTo},
                  'nid': getInt(nid),
                  'gid': getInt(gid),
                  'active': active,
                  'systempid': systempid,
                  'aysdomain': aysdomain,
                  'aysname': aysname,
                  'instance': instance
                  }
        params = self.getQuery(params)
        return j.data.models_system.Process.find(params)

    def getGrids(self, **kwargs):
        """
        list grids
        result list(list)
        """
        return j.data.models_system.Grid.find({})

    def getJumpscript(self, organization, name, **kwargs):
        """
        calls internally the agentcontroller to fetch detail for 1 jumpscript
        param:organization
        param:name
        """
        # TODO: when categories are supported
        return j.data.models_system.Jumpscript.find({'organization': organization, 'name': name})[0]

    def getJumpscripts(self, organization=None, **kwargs):
        """
        calls internally the agentcontroller
        return: lists the jumpscripts with main fields (organization, name, category, descr)
        param:organization find jumpscripts
        """
        res = {}
        # TODO: when catigories are supported
        for js in j.data.models_system.Jumpscript.find({'organization': organization}):
            key = "%s:%s" % (js["organization"], js["name"])
            if key not in res:
                res[key] = js
            if int(js["id"]) > int(res[key]["id"]):
                res[key] = js

        res2 = []
        for key, val in res.items():
            res2.append(val)

        return res2

    def getAgentControllerActiveJobs(self, **kwargs):
        """
        calls internally the agentcontroller
        list jobs now running on agentcontroller
        """
        acc = j.clients.agentcontroller.getAdvanced()
        return acc.get_all_processes()

    def getAgentControllerSessions(self, roles, nid, active, **kwargs):
        """
        calls internally the agentcontroller
        param:roles match on comma separated list of roles (subsets also ok e.g. kvm.  would match all roles starting with kvm.)
        param:nid find for specified node (on which agents are running which have sessions with the agentcontroller)
        param:active is session active or not
        """

        # sessions = j.clients.agentcontroller.listSessions()
        # def myfilter(session):
        #     if roles and not set(roles).issubset(set(session['roles'])):
        #         return False
        #     if active and not session['activejob']:
        #         return False
        #     # TODO nid?
        #     return True

        # return list(filter(myfilter, sessions))

    def _getEpoch(self, time):
        if not time:
            return time
        if isinstance(time, int):
            return time
        if time.startswith('-'):
            return j.data.time.getEpochAgo(time)
        return j.data.time.getEpochFuture(time)

    def getAudits(self, id=None, user=None, status_code=None, nid=None,
                  gid=None, from_time=None, to_time=None, **kwargs):
        """
        interface to get audit
        param:id find based on id
        param:user find audits for specified user
        param:status_code find audits based on their status code
        param:nid find audits for specified node
        param:gid find audits for specified grid
        param:from_time find audits from date specified when they happened first (-4d means 4 days ago)
        param:to_time find audits to date specified when they happened first
        """
        if id:
            return j.data.models_system.Audit.get(id)
        from_time = self._getEpoch(from_time)
        to_time = self._getEpoch(to_time)
        params = {'timestamp': {'$lte': from_time},
                  'timestamp': {'$gte': to_time},
                  'user': user,
                  'status_code': status_code,
                  'nid': getInt(nid),
                  'gid': getInt(gid)
                  }
        params = self.getQuery(params)
        return j.data.models_system.Audit.find(params)

    def getAlerts(self, id=None, level=None, descr=None, descrpub=None, nid=None, gid=None, category=None, tags=None, state=None, from_inittime=None,
                  to_inittime=None, from_lasttime=None, to_lasttime=None, from_closetime=None, to_closetime=None, nrerrorconditions=None, errorcondition=None, **kwargs):
        """
        interface to get alert (is optionally the result of an eco)
        param:level level between 1 & 3; all levels underneath are found e.g. level 3 means all levels, 1:critical, 2:warning, 3:info
        param:descr match on text in descr
        param:descrpub match on text in descrpub
        param:nid find alerts for specified node
        param:gid find alerts for specified grid
        param:category match on multiple categories; are comma separated
        param:tags comma separted list of tags/labels
        param:state NEW ALERT CLOSED
        param:from_inittime -4d;-4w;-4m;-1h;-1s  d=day w=week m=month s=sec  find alerts from date specified when they happened first (-4d means 4 days ago)
        param:to_inittime -4d;-4w;-4m;-1h;-1s  d=day w=week m=month s=sec  find alerts to date specified when they happened first
        param:from_lasttime -4d;-4w;-4m;-1h;-1s  d=day w=week m=month s=sec  find alerts from date specified when they happened last  (-4d means 4 days ago)
        param:to_lasttime -4d;-4w;-4m;-1h;-1s  d=day w=week m=month s=sec  find alerts to date specified when they happened last
        param:from_closetime -4d;-4w;-4m;-1h;-1s  d=day w=week m=month s=sec  find alerts from date specified when they were closed  (-4d means 4 days ago)
        param:to_closetime -4d;-4w;-4m;-1h;-1s  d=day w=week m=month s=sec  find alerts to date specified when they were closed
        param:nrerrorconditions nr of times errorcondition happened
        param:errorcondition errorcondition(s) which caused this alert
        """
        if id:
            return j.data.models_system.Alert.get(id)
        from_inittime = self._getEpoch(from_inittime)
        to_inittime = self._getEpoch(to_inittime)
        from_lasttime = self._getEpoch(from_lasttime)
        to_lasttime = self._getEpoch(to_lasttime)
        from_closetime = self._getEpoch(from_closetime)
        to_closetime = self._getEpoch(to_closetime)
        params = {'level': {'$lte': level},
                  'inittime': {'$lte': from_inittime},
                  'inittime': {'$gte': to_inittime},
                  'lasttime': {'$lte': from_lasttime},
                  'lasttime': {'$gte': to_lasttime},
                  'closetime': {'$lte': from_closetime},
                  'closetime': {'$gte': to_closetime},
                  'description': descr,
                  'descriptionpub': descrpub,
                  'nid': getInt(nid),
                  'gid': getInt(gid),
                  'category': category,
                  'tags': tags,
                  'state': state,
                  'nrerrorconditions': nrerrorconditions,
                  'errorconditions': errorcondition,
                  }
        params = self.getQuery(params)
        return j.data.models_system.Alert.find(params)

    def getVDisks(self, machineid=None, id=None, gid=None, nid=None, disk_id=None, fs=None, sizeFrom=None, sizeTo=None, freeFrom=None, freeTo=None, sizeondiskFrom=None, sizeondiskTo=None, mounted=None, path=None,
                  description=None, mountpoint=None, role=None, type=None, order=None, devicename=None, backup=None, backuplocation=None, backuptime=None, backupexpiration=None, active=None, lastcheckFrom=None, lastcheckTo=None, **kwargs):
        """
        list found vdisks (virtual disks like qcow2 or sections on fs as used by a container or virtual machine)
        param:machineid to which machine is the vdisk attached
        param:id find based on id
        param:gid find vdisks for specified grid
        param:nid find vdisks for specified node
        param:disk_id find disk which hosts this disk
        param:fs ext4;xfs;...
        param:sizeFrom in MB
        param:sizeTo in MB
        param:freeFrom in MB
        param:freeTo in MB
        param:sizeondiskFrom in MB
        param:sizeondiskTo in MB
        param:mounted is disk mounted
        param:path match on part of path e.g. /dev/sda
        param:description match on part of description
        param:mountpoint match on part of mountpoint
        param:role type e.g. BOOT DATA CACHE
        param:type type e.g. QCOW2 FS
        param:order when more vdisks linked to a vmachine order of linkage
        param:devicename if known device name in vmachine
        param:backup is this a backup image
        param:backuplocation where is backup stored (tag based notation)
        param:backuptime epoch when was backup taken
        param:backupexpiration when does backup needs to expire
        param:active True,is the disk still active
        param:lastcheckFrom str,-1h,-4d;-4w;-4m;-1h;-1s  d=day w=week m=month s=sec  find vdisks with lastcheckFrom  (-4d means 4 days ago)
        param:lastcheckTo str,-1h,-4d;-4w;-4m;-1h;-1s  d=day w=week m=month s=sec  find vdisks with lastcheckTo  (-4d means 4 days ago)
        result list(list)
        """
        if id:
            return j.data.models_system.VDisk.get(id)
        lastcheckFrom = self._getEpoch(lastcheckFrom)
        lastcheckTo = self._getEpoch(lastcheckTo)
        params = {'machineguid': machineid,
                  'gid': getInt(gid),
                  'nid': getInt(nid),
                  'diskid': disk_id,
                  'fs': fs,
                  'size': {'$lte': mbToKB(sizeFrom)},
                  'size': {'$gte': mbToKB(sizeTo)},
                  'free': {'$lte': mbToKB(freeFrom)},
                  'free': {'$gte': mbToKB(freeTo)},
                  'sizeondisk': {'$lte': mbToKB(sizeondiskFrom)},
                  'sizeondisk': {'$gte': mbToKB(sizeondiskTo)},
                  'lastcheck': {'$gte': lastcheckFrom},
                  'lastcheck': {'$lte': lastcheckTo},
                  'mounted': mounted,
                  'path': path,
                  'description': description,
                  'mountpoint': mountpoint,
                  'role': role,
                  'type': type,
                  'order': order,
                  'devicename': devicename,
                  'backup': backup,
                  'backuplocation': backuplocation,
                  'backupexpiration': backupexpiration,
                  'backuptime': backuptime,
                  'active': active,
                  }
        params = self.getQuery(params)
        return j.data.models_system.VDisk.find(params)

    def getMachines(self, id=None, otherid=None, gid=None, nid=None, name=None, description=None, state=None, roles=None,
                    ipaddr=None, macaddr=None, active=None, cpucore=None, mem=None, type=None, lastcheckFrom=None, lastcheckTo=None, **kwargs):
        """
        list found machines
        param:id find based on id
        param:otherid find based on 2nd id
        param:gid find nodes for specified grid
        param:nid find nodes for specified node
        param:name match on text in name
        param:description match on text in name
        param:state STARTED,STOPPED,RUNNING,FROZEN,CONFIGURED,DELETED
        param:roles match on comma separated list of roles (subsets also ok e.g. kvm.  would match all roles starting with kvm.)
        param:ipaddr comma separated list of ip addr to match against
        param:macaddr comma separated list of mac addr to match against
        param:active True,is the machine still active
        param:cpucore find based on nr cpucore
        param:mem find based on mem in MB
        param:type KVM or LXC
        param:lastcheckFrom str,-1h,-4d;-4w;-4m;-1h;-1s  d=day w=week m=month s=sec  find machines with lastcheckFrom  (-4d means 4 days ago)
        param:lastcheckTo str,-1h,-4d;-4w;-4m;-1h;-1s  d=day w=week m=month s=sec  find machines with lastcheckTo  (-4d means 4 days ago)
        result list(list)
        """
        if id:
            return j.data.models_system.Machine.get(id)
        lastcheckFrom = self._getEpoch(lastcheckFrom)
        lastcheckTo = self._getEpoch(lastcheckTo)
        params = {'otherid': otherid,
                  'gid': getInt(gid),
                  'nid': getInt(nid),
                  'lastcheck': {'$gte': lastcheckFrom},
                  'lastcheck': {'$lte': lastcheckTo},
                  'name': name,
                  'description': description,
                  'state': state,
                  'active': active,
                  'cpucore': cpucore,
                  'mem': mem,
                  'type': type, }

        def myfilter(machine):
            if roles and not set(roles).issubset(set(machine['roles'])):
                return False
            if ipaddr and ipaddr not in machine['ipaddr']:
                return False
            if macaddr and macaddr not in machine['netaddr']:
                return False
            return True
        results = j.data.models_system.Machine.find(params)
        return list(filter(myfilter, results))

    def getDisks(self, id=None, gid=None, nid=None, fs=None, sizeFrom=None, sizeTo=None, freeFrom=None,
                 freeTo=None, mounted=None, ssd=None, path=None, model=None, description=None, mountpoint=None,
                 type=None, active=None, lastcheckFrom=None, lastcheckTo=None, **kwargs):
        """
        list found disks (are really partitions)
        param:id find based on id
        param:gid find disks for specified grid
        param:nid find disks for specified node
        param:fs ext4;xfs;...
        param:sizeFrom in MB
        param:sizeTo in MB
        param:freeFrom in MB
        param:freeTo in MB
        param:mounted is disk mounted
        param:ssd is disk an ssd
        param:path match on part of path e.g. /dev/sda
        param:model match on part of model
        param:description match on part of description
        param:mountpoint match on part of mountpoint
        param:type type e.g. BOOT DATA CACHE
        param:active True,is the disk still active
        param:lastcheckFrom str,-1h,-4d;-4w;-4m;-1h;-1s  d=day w=week m=month s=sec  find disks with lastcheckFrom  (-4d means 4 days ago)
        param:lastcheckTo str,-1h,-4d;-4w;-4m;-1h;-1s  d=day w=week m=month s=sec  find disks with lastcheckTo  (-4d means 4 days ago)
        result list(list)
        """
        if id:
            return j.data.models_system.Disk.get(id)
        lastcheckFrom = self._getEpoch(lastcheckFrom)
        lastcheckTo = self._getEpoch(lastcheckTo)
        params = {'gid': getInt(gid),
                  'nid': getInt(nid),
                  'fs': fs,
                  'size': {'$lte': mbToKB(sizeFrom)},
                  'size': {'$gte': mbToKB(sizeTo)},
                  'free': {'$lte': mbToKB(freeFrom)},
                  'free': {'$gte': mbToKB(freeTo)},
                  'lastcheck': {'$gte': lastcheckFrom},
                  'lastcheck': {'$lte': lastcheckTo},
                  'mounted': mounted,
                  'ssd': ssd,
                  'path': path,
                  'model': model,
                  'description': description,
                  'mountpoint': mountpoint,
                  'type': type,
                  'active': active,
                  }
        params = self.getQuery(params)
        return j.data.models_system.Disk.find(params)

    def getNics(self, id=None, gid=None, nid=None, active=None,
                ipaddr=None, lastcheck=None, mac=None, name=None, **kwargs):
        """
        list found disks (are really partitions)
        param:id find based on id
        param:gid find disks for specified grid
        param:nid find disks for specified node
        param:active
        param:ipaddr
        param:lastcheck
        param:mac
        param:name
        result list(list)
        """
        if id:
            return j.data.models_system.Nic.get(id)
        params = {'gid': getInt(gid),
                  'nid': getInt(nid),
                  'lastcheck': lastcheck,
                  'mac': mac,
                  'name': name,
                  'ipaddr': ipaddr,
                  'active': active
                  }
        params = self.getQuery(params)
        return j.data.models_system.Nic.find(params)

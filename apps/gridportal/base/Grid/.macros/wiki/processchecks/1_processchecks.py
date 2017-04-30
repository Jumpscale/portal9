def main(j, args, params, tags, tasklet):
    doc = args.doc
    out = list()

    data = j.core.grid.healthchecker.fetchMonitoringOnAllNodes()
    errors, oldestdate = j.core.grid.healthchecker.getErrorsAndCheckTime(data)
    out.append('Grid was last checked at: {{ts:%s}}' % oldestdate)
    out.append('||Grid ID||Node ID||Node Name||Node Status||Details||')
    rows = list()

    if len(data) > 0:
        for nid, checks in data.items():
            level = 0
            if nid in errors:
                level = -1
                categories = errors.get(nid, [])
                runningstring = '{color:orange}*DEGRADED** (issues in %s){color}' % ', '.join(categories)
            else:
                level = 0
                runningstring = '{color:green}*RUNNING*{color}'
            status = checks.get('JSAgent', [{'state': 'UNKOWN'}])[0]
            if status and status['state'] != 'OK':
                level = -2
                runningstring = '{color:red}*HALTED*{color}'
            gid = j.core.grid.healthchecker.getGID(nid)
            link = '[Details|nodestatus?nid=%s&gid=%s]' % (nid, gid) 
            row = {'level': level, 'gid': gid, 'nid': nid}
            row['message'] = '|%s|[%s|grid node?nid=%s&gid=%s]|%s|%s|%s|' % (gid, nid, nid, gid, j.core.grid.healthchecker.getName(nid), runningstring, link)
            rows.append(row)
    def cmp_to_key(mycmp):
        class K:
            def __init__(self, obj, *args):
                self.obj = obj
            def __lt__(self, other):
                return mycmp(self.obj, other.obj) < 0
            def __gt__(self, other):
                return mycmp(self.obj, other.obj) > 0
            def __eq__(self, other):
                return mycmp(self.obj, other.obj) == 0
        def __le__(self, other):
            return mycmp(self.obj, other.obj) <= 0
        def __ge__(self, other):
            return mycmp(self.obj, other.obj) >= 0
        def __ne__(self, other):
            return mycmp(self.obj, other.obj) != 0
        return K

    def sorter(row1, row2):
        for sortkey in ('level', 'gid', 'nid'):
            if row1[sortkey] != row2[sortkey] or sortkey == 'nid':
                return cmp(row1[sortkey], row2[sortkey] )

    out.extend([x['message'] for x in sorted(rows, key=cmp_to_key(sorter))])
    params.result = ('\n'.join(out), doc)
    return params

def match(j, args, params, tags, tasklet):
    return True

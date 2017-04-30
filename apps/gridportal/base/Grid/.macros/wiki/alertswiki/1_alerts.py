

def main(j, args, params, tags, tasklet):


    params.merge(args)
    doc = params.doc
    tags = params.tags
    
    out = []

    #this makes sure bootstrap datatables functionality is used
    out.append("{{datatables_use}}\n")

    #['category', 'description', 'level', 'inittime', 'tags', 'closetime', 'id', 'state', 'gid', 'nrerrorconditions', 'lasttime', 'descriptionpub', 'errorconditions']


    out='||link||gid||nid||category||date||esc_date||state||value||\n'

    for gguid in j.tools.watchdog.manager.getGGUIDS():
        for alert in j.tools.watchdog.manager.iterateAlerts(gguid=gguid):
            epochHR=j.data.time.epoch2HRDateTime(alert.epoch)
            epochEsc=j.data.time.epoch2HRDateTime(alert.escalationepoch)
            id='[link|/grid/alert?id=%s&nid=%s&category=%s]'%(gguid,alert.nid,alert.category)
            out+="|%s|%s|%s|%s|%s|%s|%s|%s|\n"%(id,alert.gid,alert.nid,alert.category,epochHR,epochEsc,alert.state,alert.value)

 
    params.result = (out, doc)

    return params


def match(j, args, params, tags, tasklet):
    return True

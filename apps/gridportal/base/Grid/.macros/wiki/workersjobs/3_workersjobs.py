def main(j, args, params, tags, tasklet):


    doc = args.doc
    nid = args.getTag('nid')
    node =j.apps.system.gridmanager.getNodes(nid=nid)
    if node:
        node = node[0].to_dict()
    workerscl = j.clients.agentcontroller.getProxy(category="worker")
    jobs = workerscl.getQueuedJobs(queue=None, format='json', _agentid=nid)

    # TODO: does not work ques not implemented in ac2
    #accl = j.clients.agentcontroller.getAdvanced()
    #jobs = accl.?

    doc.applyTemplate({'name': node['name'], 'jobs': jobs})
    params.result = (doc, doc)

    return params

def match(j, args, params, tags, tasklet):
    return True

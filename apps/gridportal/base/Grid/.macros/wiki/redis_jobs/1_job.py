def main(j, args, params, tags, tasklet):

    r=j.clients.redis.get("127.0.0.1",9999)

    keys=r.keys()

    nodeids=[key.split(":")[1] for key in keys if key.find("jobs:")==0]
    nodeids.pop(nodeids.index("last"))

    out=""


    #get jobs per node
    for nodeid in nodeids:
        nodejobKey="jobs:%s"%nodeid
        jobids=r.hkeys(nodejobKey)
        jobids.sort()
        out+="h3. node %s"%nodeid
        out+="||id||category||cmd||start||stop||state||queue||"
        for jobid in jobids:
            out+=getJobLine(jobid)

    #get queue per node
    

    params.result = (out, args.doc)
    return params

def match(j, args, params, tags, tasklet):
    return True

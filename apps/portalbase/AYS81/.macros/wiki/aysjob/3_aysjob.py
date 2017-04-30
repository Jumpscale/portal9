

def main(j, args, params, tags, tasklet):
    job_id = args.getTag('jobid')
    job = j.core.jobcontroller.db.jobs.get(job_id)
    action = j.core.jobcontroller.db.actions.get(job.dbobj.actionKey)

    def printLogs(_logs):
        logs = []
        for log in _logs:
            logs.append(("{epoch} - {category}: {log}".format(
                epoch=j.data.time.epoch2HRDateTime(log.get('epoch')),
                category=log.get('category', ''),
                log=log.get('log', '')
            )))
        logs = '\n'.join(logs)
        return logs

    if job:
        job.printLogs = printLogs(job.dictFiltered.get('logs', []))
        args.doc.applyTemplate({'job': job, 'action': action})
    else:
        args.doc.applyTemplate({'error': 'No job found'})

    params.result = (args.doc, args.doc)
    return params

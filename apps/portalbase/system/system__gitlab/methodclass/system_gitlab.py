from js9 import j


class system_gitlab(j.tools.code.classGetBase()):

    """
    Gitlab SYstem actors

    """

    def updateUserSpace(self, spacename, **args):
        ctx = args['ctx']
        username = ctx.env['beaker.session']['user']
        # Start cloning certain repo in Async manner
        js = j.clients.redisworker.getJumpscriptFromName('jumpscale', 'clonegitlabspace')
        job = j.clients.redisworker.execJumpscript(js.id, js, _sync=False, username=username, spacename=spacename)
        return job.id

    def updateUserSpaces(self, **args):
        # Start cloning All user spaces in Asunc manner
        ctx = args['ctx']
        username = ctx.env['beaker.session']['user']
        js = j.clients.redisworker.getJumpscriptFromName('jumpscale', 'clonegitlabspaces')
        job = j.clients.redisworker.execJumpscript(js.id, js, _sync=False, username=username)
        return job.id

    def checkUpdateUserSpaceJob(self, jobid, **args):
        try:
            job = j.clients.redisworker.getJob(jobid)
            return job['state']
        except KeyError:
            # job expired means finished
            return 'OK'

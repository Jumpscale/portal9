from js9 import j
from . import exceptions
import time
import types


def doAudit(user, path, kwargs, responsetime, statuscode, result, tags):
    client = j.portal.tools.models.system.Audit
    audit = client()
    audit.user = user
    audit.call = path
    audit.status_code = statuscode
    audit.args = j.data.serializer.json.dumps([])  # we dont want to log self
    audit.tags = tags
    auditkwargs = kwargs.copy()
    auditkwargs.pop('ctx', None)
    audit.kwargs = j.data.serializer.json.dumps(auditkwargs)
    try:
        if not isinstance(result, types.GeneratorType):
            audit.result = j.data.serializer.json.dumps(result)
        else:
            audit.result = j.data.serializer.json.dumps('Result of type generator')
    except:
        audit.result = "Result contains binary data"

    audit.responsetime = responsetime
    audit.save()


class AuditMiddleWare(object):

    def __init__(self, app):
        self.app = app

    def __call__(self, env, start_response):
        statinfo = {'status': 200}

        def my_response(status, headers, exc_info=None):
            statinfo['status'] = int(status.split(" ", 1)[0])
            return start_response(status, headers, exc_info)

        start = time.time()
        env['tags'] = ''
        result = self.app(env, my_response)
        responsetime = time.time() - start
        audit = env.get('JS_AUDIT')
        if audit or statinfo['status'] >= 400:
            ctx = env.get('JS_CTX')
            user = env['beaker.session'].get('user', 'Unknown')
            tags = env['tags']
            kwargs = ctx.params.copy() if ctx else {}
            if j.portal.tools.server.active.authentication_method:
                doAudit(user, env['PATH_INFO'], kwargs, responsetime, statinfo['status'], result, tags)
        return result


class auth(object):

    def __init__(self, groups=None, audit=True):
        if isinstance(groups, str):
            groups = [groups]
        if groups is None:
            groups = list()
        self.groups = set(groups)
        self.audit = audit

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            if 'ctx' not in kwargs:
                # call is not performed over rest let it pass
                return func(*args, **kwargs)
            ctx = kwargs['ctx']
            user = ctx.env['beaker.session']['user']
            if self.groups:
                userobj = j.portal.tools.server.active.auth.getUserInfo(user)
                groups = set(userobj.groups)
                if not groups.intersection(self.groups):
                    raise exceptions.Forbidden(
                        'User %s has no access. If you would like to gain access please contact your adminstrator' %
                        user)

            ctx.env['JS_AUDIT'] = self.audit
            return func(*args, **kwargs)
        return wrapper

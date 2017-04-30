from js9 import j
import http.client

codemapping = http.client.responses.copy()
codemapping[419] = 'Authentication Timeout'


class BaseError(BaseException):

    def __init__(self, code, headers, msg, status=None):
        self.code = code
        self.headers = headers
        self.msg = msg
        if status is None:
            status = codemapping.get(code, 'Unkonwn')
        self.status = status


class Error(BaseError):
    CODE = 500

    def __init__(self, msg):
        msg = j.data.serializer.json.dumps(msg)
        BaseError.__init__(self, self.CODE, [('Content-Type', 'application/json')], msg)


class Redirect(BaseError):

    def __init__(self, location):
        headers = [('Location', location)]
        BaseError.__init__(self, 302, headers, "")


class BadRequest(Error):
    CODE = 400


class Unauthorized(Error):
    CODE = 401


class Forbidden(Error):
    CODE = 403


class NotFound(Error):
    CODE = 404


class MethodNotAllowed(Error):
    CODE = 405


class Conflict(Error):
    CODE = 409


class PreconditionFailed(Error):
    CODE = 412


class ServiceUnavailable(Error):
    CODE = 503


class InternalServer(Error):
    CODE = 500

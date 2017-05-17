from js9 import j
import requests
from functools import wraps
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


def catcherrors(debug=False, msg="Error was {}", ):
    def wrapper(method):
        @wraps(method)
        def mymeth(self, *methargs, **methkwargs):
            try:
                res = method(self, *methargs, **methkwargs)
            except requests.exceptions.HTTPError as e:
                if debug:
                    jsonresp = e.response.json()
                    if 'error' in jsonresp:
                        raise BadRequest(msg.format(jsonresp['error']))
                    else:
                        raise BadRequest(msg.format(str(e)))
                else:
                    raise BadRequest(str(e))
            except Exception as e:
                raise BadRequest(str(e))
            else:
                return res
        return mymeth
    return wrapper

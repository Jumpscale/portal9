from js9 import j
from JumpScale.portal.portal import exceptions
from JumpScale.servers.serverbase.Exceptions import RemoteException
import urllib.request
import urllib.parse
import urllib.error
import requests


class PortalRest():

    def __init__(self, webserver):
        self.ws = webserver
        self.logger = j.logger.get("j.portal.tools")

    def validate(self, auth, ctx):
        if ctx.params == "":
            msg = 'No parameters given to actormethod.'
            ctx.start_response('400 Bad Request', [])
            return False, msg
        if auth and ctx.env['beaker.session']['user'] == 'guest':
            msg = 'NO VALID AUTHORIZATION KEY GIVEN, use get param called key (check key probably auth error).'
            ctx.start_response('401 Unauthorized', [])
            return False, msg

        params = self.ws.routes[ctx.path]['params']

        for key, param in params.items():
            if key not in ctx.params:
                if param['optional']:
                    # means is optional
                    ctx.params[key] = param['default']
                else:
                    raise exceptions.BadRequest('Param with name:%s is missing.' % key)
            elif param['type'] == 'int' and not isinstance(ctx.params[key], (int, type(None))):
                try:
                    ctx.params[key] = int(ctx.params[key])
                except ValueError:
                    raise exceptions.BadRequest(
                        'Value of param %s not correct needs to be of type %s' %
                        (key, param['type']))
            elif param['type'] == 'bool' and not isinstance(ctx.params[key], (bool, type(None))):
                try:
                    ctx.params[key] = j.data.types.bool.fromString(ctx.params[key])
                except ValueError:
                    raise exceptions.BadRequest(
                        'Value of param %s not correct needs to be of type %s' %
                        (key, param['type']))

        return True, ""

    def restPathProcessor(self, path):
        """
        Function which parse a path, returning True or False depending on
        successfull parsing, a error message and a dict of parameters.
        When successfull the params dict contains the path elements otherwise it
        contains if provided the actorname  and appname.
        """
        # self.logger.info("Process path %s" % path, 9)
        params = {}
        while path != "" and path[0] == "/":
            path = path[1:]
        while path != "" and path[-1] == "/":
            path = path[:-1]
        if path.strip() == "":
            return (False, "Bad input path was empty. Format of url need to be http://$ipaddr/rest/$appname/$actorname/$actormetho?...", {})
        paths = path.split("/")
        if len(paths) < 3:
            msginfo = "Format of url need to be http://$ipaddr/rest/$appname/$actorname/$actormethod?...\n\n"
            if len(paths) > 0:
                appname = paths[0]
            else:
                appname = ""
                actor = ""
            if len(paths) > 1:
                actor = paths[1]
            else:
                actor = ""
            params["appname"] = appname
            params["actorname"] = actor
            return (False, msginfo, params)
        params["paths"] = paths
        return (True, "", params)

    def restextPathProcessor(self, path):
        self.logger.info("Process path %s" % path, 9)
        params = {}
        while path != "" and path[0] == "/":
            path = path[1:]
        while path != "" and path[-1] == "/":
            path = path[:-1]
        if path.strip() == "":
            return (False, "Bad input path was empty. Format of url need to be http://$ipaddr/restext/$appname/$modelname/$args", {})
        paths = path.split("/")
        if len(paths) < 2:
            msginfo = "Format of url need to be http://$ipaddr/restext/$appname/$modelname/$args...\n\n"
            if len(paths) > 0:
                appname = paths[0]
            else:
                appname = ""
                modelname = ""
            if len(paths) > 1:
                modelname = paths[1]
            else:
                modelname = ""
            params["appname"] = appname
            params["modelname"] = modelname
            return (False, msginfo, params)
        params["paths"] = paths
        return (True, "", params)

    def restRouter(self, env, start_response, path, paths, ctx, ext=False, routekey=None, human=False):
        """
        does validaton & authorization
        returns right route key
        """
        if not routekey:
            routekey = "%s_%s_%s" % (paths[0], paths[1], paths[2])
        # self.logger.info("Execute %s %s" % (env["REMOTE_ADDR"], routekey))
        routes = self.ws.routes
        if routekey not in routes:
            self.activateActor(paths[0], paths[1])
        if routekey not in routes:
            routekey = "GET_%s" % routekey
        if routekey in routes:
            if human:
                ctx.fformat = "human"
            elif("format" not in ctx.params):
                ctx.fformat = routes[routekey]['returnformat']
            else:
                ctx.fformat = ctx.params["format"]
            ctx.path = routekey
            ctx.fullpath = path
            ctx.application = paths[0]
            ctx.actor = paths[1]
            ctx.method = paths[2]
            auth = routes[routekey]['auth']

            resultcode, msg = self.validate(auth, ctx)  # validation & authorization (but user needs to be known)
            if resultcode is False:
                if human:
                    params = {}
                    params["error"] = "Incorrect Request: %s" % msg
                    params["appname"] = ctx.application
                    params["actorname"] = ctx.actor
                    params["method"] = ctx.method
                    page = self.ws.pageprocessor.returnDoc(ctx, start_response, "system",
                                                           "restvalidationerror", extraParams=params)
                    return (False, ctx, [str(page)])
                else:
                    return (False, ctx, msg)
            else:
                return (True, ctx, routekey)
        else:
            msg = "Could not find method, path was %s" % (path)
            appname = paths[0]
            actor = paths[1]
            contentType, data = self.ws.pageprocessor.reformatOutput(ctx, msg, restreturn=not human)
            ctx.start_response("404 Not Found", [('Content-Type', contentType)])
            if human:
                page = self.getServicesInfo(appname, actor)
                return (False, ctx, self.ws.pageprocessor.raiseError(ctx=ctx, msg=msg, msginfo=str(page)))
            else:
                contentType, data = self.ws.pageprocessor.reformatOutput(ctx, msg, restreturn=False)
                return (False, ctx, data)

    def execute_rest_call(self, ctx, routekey, ext=False):
        routes = self.ws.routes
        try:
            method = routes[routekey]['func']
            result = method(ctx=ctx, **ctx.params)
            return (True, result)
        except RemoteException as error:
            if error.eco.get('exceptionclassname') == 'KeyError':
                data = error.eco['data'] or {'categoryname': 'unknown', 'key': '-1'}
                raise exceptions.NotFound("Could not find %(key)s of type %(categoryname)s" % data)
            raise

        except requests.exceptions.ConnectionError as error:
            message = error.args[0]
            raise exceptions.Error(message)
        except Exception as errorObject:
            eco = j.errorhandler.processPythonExceptionObject(errorObject)
            msg = "Execute method %s failed." % (routekey)
            return (False, self.ws.pageprocessor.raiseError(ctx=ctx, msg=msg, errorObject=eco))

    def processor_rest(self, env, start_response, path, human=True, ctx=False):
        """
        orignal rest processor (get statements)
        e.g. http://localhost/restmachine/system/contentmanager/notifySpaceModification?name=www_openvstorage&authkey=1234
        """
        if ctx is False:
            raise RuntimeError("ctx cannot be empty")
        try:
            # self.logger.info("Routing request to %s" % path, 9)

            def respond(contentType, msg):
                # self.logger.info("Responding %s" % msg, 5)
                if contentType:
                    ctx.start_response('200 OK', [('Content-Type', contentType)])
                # print msg
                return msg

            success, msg, params = self.restPathProcessor(path)
            if not success:
                params["error"] = msg
                if human:
                    page = self.ws.pageprocessor.returnDoc(ctx, start_response, "system", "rest",
                                                           extraParams=params)
                    return [str(page)]
                else:
                    httpcode = "404 Not Found"
                    contentType, data = self.ws.pageprocessor.reformatOutput(ctx, msg, restreturn=True)
                    ctx.start_response(httpcode, [('Content-Type', contentType)])
                    return data
            paths = params['paths']

            success, ctx, routekey = self.restRouter(env, start_response, path,
                                                     paths, ctx, human=human)
            if not success:
                # in this case routekey is really the errormsg
                return routekey

            success, result = self.execute_rest_call(ctx, routekey)
            if not success:
                return result

            if human:
                ctx.format = "json"
                params = {}
                params["result"] = result
                return [str(self.ws.pageprocessor.returnDoc(
                    ctx, start_response, "system", "restresult", extraParams=params))]
            else:
                contentType, result = self.ws.pageprocessor.reformatOutput(ctx, result)
                return respond(contentType, result)
        except Exception as errorObject:
            eco = j.errorhandler.processPythonExceptionObject(errorObject)
            if ctx is False:
                print("NO webserver context yet, serious error")
                eco.process()
                print(eco)
            else:
                return self.ws.pageprocessor.raiseError(ctx, errorObject=eco)

    def processor_restext(self, env, start_response, path, human=True, ctx=False):
        """
        rest processer gen 2 (not used by the original get code)
        """
        if ctx is False:
            raise RuntimeError("ctx cannot be empty")
        try:
            self.logger.info("Routing request to %s" % path, 9)

            def respond(contentType, msg):
                if contentType:
                    start_response('200 OK', [('Content-Type', contentType)])
                return msg

            success, message, params = self.restextPathProcessor(path)

            if not success:
                params["error"] = message
                if human:
                    page = self.ws.pageprocessor.returnDoc(ctx, start_response, "system", "rest",
                                                           extraParams=params)
                    return [str(page)]
                else:
                    return self.ws.pageprocessor.raiseError(ctx, message)
            requestmethod = ctx.env['REQUEST_METHOD']
            paths = params['paths']
            appname = paths[0]
            model = paths[1]
            objectid = None
            if len(paths) > 2:
                objectid = int(paths[2])
                ctx.params['id'] = objectid

            osiscl = j.clients.osis.getCategory(self.ws.osis, appname, model)
            osismap = {'GET': ['get', 'list', 'search'], 'POST': [''], 'DELETE': ['delete']}

            if requestmethod == 'GET':
                result = self._handle_get(ctx, osiscl, objectid)
            elif requestmethod in ('POST', 'PUT'):
                result = self._handle_post(ctx, osiscl, objectid)
            elif requestmethod == 'DELETE':
                result = self._handle_delete(ctx, osiscl, objectid)
            else:
                start_response('405 Method not allowed', [('Content-Type', 'text/html')])
                return 'Requested method is not allowed'

            if human:
                ctx.fformat = "json"
                params = {}
                params["result"] = result
                return [str(self.ws.pageprocessor.returnDoc(
                    ctx, start_response, "system", "restresult", extraParams=params))]
            else:
                ctx.fformat = 'jsonraw'
                contentType, result = self.ws.pageprocessor.reformatOutput(ctx, result)
                return respond(contentType, result)
        except Exception as errorObject:
            eco = j.errorhandler.processPythonExceptionObject(errorObject)
            if ctx is False:
                print("NO webserver context yet, serious error")
                eco.process()
                print(eco)
            else:
                return self.ws.pageprocessor.raiseError(ctx, errorObject=eco)

    def _handle_get(self, ctx, osiscl, objectid):
        if objectid:  # get object
            result = osiscl.get(objectid)
            return result.dump()
        else:  # list or search
            if ctx.env['QUERY_STRING']:  # search
                query = self._get_query_string(ctx)
                return osiscl.search(query)[1:]
            else:  # list
                return osiscl.search({})[1:]

    def _handle_delete(self, ctx, osiscl, objectid):
        return osiscl.delete(objectid)

    def _handle_post(self, ctx, osiscl, objectid):
        fields = ctx.params
        if objectid:  # update
            obj = osiscl.get(objectid)
        else:  # new
            obj = osiscl.new()
        if 'id' in fields:
            fields.pop('id')
        for field, value in fields.items():
            setattr(obj, field, value)
        return osiscl.set(obj)

    def _get_query_string(self, ctx):
        fields = dict()
        if ctx.env['QUERY_STRING']:
            queryparts = ctx.env['QUERY_STRING'].split('&')
            for querypart in queryparts:
                querypart = urllib.parse.unquote(querypart)
                field, value = querypart.split('=')
                fields[field] = int(value) if value.isdigit() else value
        return fields

    def activateActor(self, appname, actor):
        if not "%s_%s" % (appname, actor) in list(self.ws.actors.keys()):
            # need to activate
            try:
                result = self.ws.actorsloader.getActor(appname, actor)
            except Exception as e:
                eco = j.errorhandler.processPythonExceptionObject(e)
                eco.process()
                print(eco)
                return False
            if result is None:
                # there was no actor
                return False

import urllib.parse
import collections
import os
import json
import sys
import inspect

from beaker.middleware import SessionMiddleware
from .MacroExecutor import MacroExecutorPage, MacroExecutorWiki, MacroExecutorPreprocess, MacroexecutorMarkDown
from .ErrorHandler import ErrorHandler
from .RequestContext import RequestContext
from .PortalRest import PortalRest
from .MongoEngineBeaker import MongoEngineBeaker
from .MinimalBeaker import MinimalBeaker
from . import exceptions
from .auth import AuditMiddleWare

from JumpScale9Portal.portal.portalloaders.SpaceWatcher import SpaceWatcher
from JumpScale9Portal.portal.html import multipart

from js9 import j
from gevent.pywsgi import WSGIServer
import gevent
import time

import urllib.request
import urllib.parse
import urllib.error
import cgi
from .PortalAuthenticatorGitlab import PortalAuthenticatorGitlab
from .PortalAuthenticatorMinimal import PortalAuthenticatorMinimal
from .PortalAuthenticatorMongoEngine import PortalAuthenticatorMongoEngine
from .PortalTemplate import PortalTemplate
from .PageProcessor import PageProcessor


# from flask.ext.bootstrap import Bootstrap
from werkzeug.wsgi import DispatcherMiddleware
# from flask import render_template


def exhaustgenerator(func):
    def wrapper(self, env, start_response):
        try:
            result = func(self, env, start_response)
        except exceptions.BaseError as e:
            start_response("%s %s" % (e.code, e.status), e.headers)
            return [e.msg.encode('utf-8')]
        if isinstance(result, str):
            return [j.data.text.toStr(result).encode('utf-8')]
        if isinstance(result, bytes):
            return [result]
        elif isinstance(result, collections.Iterable):
            def exhaust():
                for value in result:
                    if not isinstance(value, bytes):
                        value = value.encode('utf-8')
                    yield value
            return exhaust()
        elif not result:
            return [''.encode('utf-8')]
        else:
            return result.encode('utf-8')
    return wrapper


class PortalServer:

    # INIT
    def __init__(self):
        self.cfg = j.application.instanceconfig
        if not isinstance(self.cfg, dict):
            # need to upgrade config
            hrd = self.cfg.getDictFromPrefix('param.cfg')
            production = hrd.get('production', False)
            client_id = hrd.get('client_id', '')
            client_secret = hrd.get('client_secret', '')
            organization = hrd.get('organization', '')
            redirect_address = hrd.get('redirect_url', '')
            if redirect_address:
                redirect_address = redirect_address.split('//')[1].split('/restmachine')[0]

            j.tools.cuisine.local.core.dir_ensure('$TEMPLATEDIR/cfg/portal')
            j.tools.cuisine.local.core.file_copy(j.sal.fs.joinPaths(j.dirs.CODEDIR, 'github/jumpscale/jumpscale_portal8/apps/portalbase/config.yaml'),
                                                 '$TEMPLATEDIR/cfg/portal/config.yaml')
            j.tools.cuisine.local.apps.portal.configure(production=production, client_id=client_id, client_secret=client_secret, organization=organization, redirect_address=redirect_address)
            j.application.instanceconfig = j.data.serializer.yaml.load('%s/portals/main/config.yaml' % (j.dirs.JSCFGDIR))
            self.cfg = j.application.instanceconfig
        self.logger = j.logger.get('j.portal.tools.server')

        self.contentdirs = list()
        self.libpath = j.portal.tools.html.htmlfactory.getHtmllibDir()
        self.started = False
        self.epoch = time.time()
        self.force_oauth_url = None
        self.force_oauth_instance = self.cfg.get('force_oauth_instance', "")
        j.application.debug = self.cfg.get("debug", False)
        j.portal.tools.server.active = self

        self.watchedspaces = []
        self.pageKey2doc = {}
        self.routes = {}
        self.proxies = {}

        self.authentication_method = self.cfg.get("authentication.method")
        session_opts = {
            'session.cookie_expires': False,
            'session.data_dir': '%s' % j.sal.fs.joinPaths(j.dirs.VARDIR, "beakercache")
        }

        # TODO change that to work with ays instance config instead of connection string
        connection = self.cfg.get('mongoengine.connection', {})
        self.port = connection.get('port', None)

        if not self.authentication_method:
            minimalsession = {
                'session.type': 'MinimalBeaker',
                'session.namespace_class': MinimalBeaker,
                'session.namespace_args': {'client': None}
            }
            session_opts.update(minimalsession)
            self.auth = PortalAuthenticatorMinimal()
        else:
            if self.authentication_method == 'gitlab':
                self.auth = PortalAuthenticatorGitlab(instance=self.gitlabinstance)
            else:
                j.portal.tools.models.system.connect2mongo(connection['host'], port=int(connection['port']))

                mongoenginesession = {
                    'session.type': 'MongoEngineBeaker',
                    'session.namespace_class': MongoEngineBeaker,
                    'session.namespace_args': {}
                }
                session_opts.update(mongoenginesession)
                self.auth = PortalAuthenticatorMongoEngine()

        self.pageprocessor = PageProcessor()

        self.loadConfig()

        macros_dir = j.sal.fs.joinPaths(j.sal.fs.getcwd(), 'macros')
        macroPathsPreprocessor = [j.sal.fs.joinPaths(macros_dir, "preprocess")]
        macroPathsWiki = [j.sal.fs.joinPaths(macros_dir, "wiki")]
        macroPathsPage = [j.sal.fs.joinPaths(macros_dir, "page")]
        macroPathsMarkDown = [j.sal.fs.joinPaths(macros_dir, "markdown")]

        self.macroexecutorPreprocessor = MacroExecutorPreprocess(macroPathsPreprocessor)
        self.macroexecutorPage = MacroExecutorPage(macroPathsPage)
        self.macroexecutorMarkDown = MacroexecutorMarkDown(macroPathsMarkDown)
        self.macroexecutorWiki = MacroExecutorWiki(macroPathsWiki)
        self.errorhandler = ErrorHandler()
        templatedirs = [self.portaldir.joinpath('templates'), self.appdir.joinpath('templates')]
        for contentdir in self.contentdirs:
            templatedirs.append(j.sal.fs.joinPaths(contentdir, 'templates'))
        self.templates = PortalTemplate(templatedirs)
        self.bootstrap()

        self._router = SessionMiddleware(AuditMiddleWare(self.router), session_opts)

        self._megarouter = DispatcherMiddleware(self._router)
        self._webserver = WSGIServer((self.listenip, self.port), self._megarouter)

        self.confluence2htmlconvertor = j.portal.tools.docgenerator.docgeneratorfactory.getConfluence2htmlConvertor()
        self.activejobs = list()
        self.jobids2greenlets = dict()

        self.schedule1min = {}
        self.schedule15min = {}
        self.schedule60min = {}

        self.jslibroot = j.sal.fs.joinPaths(j.dirs.JSAPPSDIR, "portals", "jslib")

        #  Load local spaces
        self.rest = PortalRest(self)
        self.loadSpaces()
        # let's roll

    def loadConfig(self):

        def replaceVar(txt):
            txt = txt.replace("\\", "/")
            txt = txt.replace("$HTMLLIBDIR", j.portal.tools.html.htmlfactory.getHtmllibDir())
            txt = txt.replace("$APPSDIR", j.sal.fs.getcwd())
            txt = txt.replace("$APPDIR", j.sal.fs.getcwd())
            txt = txt.replace("\\", "/")
            txt = j.dirs.replaceTxtDirVars(txt)
            return txt

        # INIT FILE
        self.portaldir = j.tools.path.get(j.sal.fs.getcwd())

        self.appdir = j.tools.path.get(replaceVar(self.cfg.get("appdir", self.portaldir)))

        self.getContentDirs()  # contentdirs need to be loaded before we go to other dir of base server

        self.appdir.chdir()

        self.listenip = self.cfg.get('listenip', '0.0.0.0')
        self.port = int(self.cfg.get("port", 82))
        self.addr = self.cfg.get("pubipaddr", '127.0.0.1')
        self.secret = self.cfg.get("secret")
        self.jwtcfg = self.cfg.get("jwt", dict())
        self.admingroups = [item.strip() for item in self.cfg.get("admingroups", []) if item.strip() != ""]

        self.filesroot = j.tools.path.get(replaceVar(self.cfg.get("filesroot")))
        self.filesroot.makedirs_p()
        self.pageprocessor.defaultspace = self.cfg.get('defaultspace', 'welcome')
        self.pageprocessor.defaultpage = self.cfg.get('defaultpage', '')

        self.gitlabinstance = self.cfg.get("gitlab.connection")

        self.getContentDirs()

        # load proxies
        for _, proxy in self.cfg.get('cfg.proxy', {}).items():
            print('loading proxy', proxy)
            self.proxies[proxy['path']] = proxy

    def reset(self):
        self.routes = {}
        self.loadConfig()
        self.bootstrap()
        j.portal.tools.codegentools.codegenerator.resetMemNonSystem()
        j.portal.tools.specparser.specparserfactory.resetMemNonSystem()
        # self.actorsloader.scan(path=self.contentdirs,reset=True) #do we need to load them all
        self.bucketsloader = j.portal.tools.portalloaders.loaderfactory.getBucketsLoader()
        self.loadSpaces()

    def bootstrap(self):
        self.actors = {}  # key is the applicationName_actorname (lowercase)
        self.actorsloader = j.portal.tools.portalloaders.loaderfactory.getActorsLoader()
        self.app_actor_dict = {}
        self.taskletengines = {}
        self.actorsloader.reset()
        # self.actorsloader._generateLoadActor("system", "contentmanager", actorpath="%s/apps/portalbase/system/system__contentmanager/"%j.dirs.JSBASEDIR)
        # self.actorsloader._generateLoadActor("system", "master", actorpath="system/system__master/")
        # self.actorsloader._generateLoadActor("system", "usermanager", actorpath="system/system__usermanager/")
        self.actorsloader.scan(self.contentdirs)

        if self.authentication_method:
            self.actorsloader.getActor("system", "contentmanager")
            self.actorsloader.getActor("system", "usermanager")

    def deleteSpace(self, spacename):
        self.loadSpaces()
        spacename = spacename.lower()
        if spacename in self.spacesloader.spaces:
            space = self.spacesloader.spaces.pop(spacename)
            space.deleteOnDisk()
        else:
            raise RuntimeError("Could not find space %s to delete" % spacename)

    def loadSpaces(self):

        self.bucketsloader = j.portal.tools.portalloaders.loaderfactory.getBucketsLoader()
        self.spacesloader = j.portal.tools.portalloaders.loaderfactory.getSpacesLoader()
        self.bucketsloader.scan(self.contentdirs)

        self.spacesloader.scan(self.contentdirs)

        if self.authentication_method:
            if "system" not in self.spacesloader.spaces:
                raise RuntimeError("could not find system space")

    def getContentDirs(self):
        """
        walk over known content dirs & execute loader on it
        """
        contentdirs = self.cfg.get('contentdirs', '')

        def append(path):
            path = j.tools.path.get(path).normpath()
            if path not in self.contentdirs:
                self.contentdirs.append(path)

        paths = contentdirs.split(",")

        # add own base path
        self.basepath = j.tools.path.get(self.portaldir.joinpath("base"))
        self.basepath.makedirs_p()
        append(self.basepath)

        paths.append(self.basepath)
        paths = list(set(paths))
        for path in paths:
            path = path.strip()
            if path == "" or path[0] == "#":
                continue
            path = path.replace("\\", "/")
            if path.find(":") == -1:
                if path not in self.watchedspaces:
                    SpaceWatcher(path)
            append(path)

        # add base path of parent portal
        if self.authentication_method:
            appdir = self.appdir
            append(appdir.joinpath("wiki"))
            append(appdir.joinpath("system"))

    def unloadActorFromRoutes(self, appname, actorname):
        for key in list(self.routes.keys()):
            appn, actorn, remaining = key.split("_", 2)
            # print appn+" "+appname+" "+actorn+" "+actorname
            if appn == appname and actorn == actorname:
                self.routes.pop(key)

# USER RIGHTS

    def getAccessibleLocalSpacesForGitlabUser(self, gitlabspaces):
        """
        Return Local Spaces (Non Gitlab Spaces) with guest permissions set to READ or higher
        """
        spaces = {}
        localspaces = [x.model.id.lower() for x in list(self.spacesloader.spaces.values()) if x not in gitlabspaces]
        for space in localspaces:
            rights = ''
            spaceobject = self.spacesloader.spaces.get(space)
            for groupuser in ["guest", "guests"]:
                if groupuser in spaceobject.model.acl:
                    r = spaceobject.model.acl[groupuser]
                    if r == "*":
                        rights = "rwa"
                    else:
                        rights = r
            if 'r' in rights or '*' in rights:
                spaces[space] = rights
        return spaces

    def getUserSpaces(self, ctx):
        if not hasattr(ctx, 'env') or "user" not in ctx.env['beaker.session']:
            return []
        username = ctx.env['beaker.session']["user"]
        spaces = self.auth.getUserSpaces(username, spaceloader=self.spacesloader)

        # In case of gitlab, we want to get the local spaces tha user has access to
        if self.authentication_method == 'gitlab':
            spaces += list(self.getAccessibleLocalSpacesForGitlabUser(spaces).keys())

        else:
            result = []
            for s in spaces:
                rights = self.getUserSpaceRights(ctx, s)
                if 'r' in rights[1] or '*' in rights:
                    result.append(s)
            spaces = result
        return list(set(spaces))

    def getUserSpacesObjects(self, ctx):
        """
        Only used in gitlab
        """
        if hasattr(ctx, 'env') and "user" in ctx.env['beaker.session']:
            username = ctx.env['beaker.session']["user"]
            if self.authentication_method == 'gitlab':
                gitlabobjects = self.auth.getUserSpacesObjects(username)
                keys = [x['name'] for x in gitlabobjects]
                for name in self.getAccessibleLocalSpacesForGitlabUser(keys):
                    if username in name and name.replace("%s_" % username, '') in keys:
                        continue
                    gitlabobjects.append({'name': name, 'namespace': {'name': ''}})
                return gitlabobjects

    def getSpaceLinks(self, ctx):
        if self.authentication_method == 'gitlab':
            spaces = {}
            for s in self.getUserSpacesObjects(ctx):
                if s['namespace']['name']:
                    spaces[s['name']] = "%s_%s" % (s['namespace']['name'], s['name'])
                else:
                    spaces[s['name']] = "/%s" % s['name']
        else:
            spaces = {}
            for spaceid in self.getUserSpaces(ctx):
                space = self.getSpace(spaceid, ignore_doc_processor=True)
                if space.model.hidden:
                    continue
                spaces[space.model.name] = "/%s" % spaceid
        return spaces

    def getNonClonedGitlabSpaces(self, ctx):
        """
        Return Gitlab spaces that are not (YET) cloned into local filesystem
        This is helpful to identify non-existing spaces, so that system can disable
        access to them until cloning is finished.

        @param ctx: Context
        """
        if not self.authentication_method == 'gitlab':
            raise RuntimeError("This function only works with gitlab authentication")

        if not hasattr(ctx, 'env') and "user" in ctx.env['beaker.session']:
            return []
        username = ctx.env['beaker.session']["user"]

        clonedspaces = set([s.model.id[s.model.id.index('portal_'):]
                            for s in list(self.spacesloader.spaces.values()) if 'portal_' in s.model.id])
        gitlabspaces = set([s[s.index('portal_'):]
                            for s in self.auth.getUserSpaces(username, spaceloader=self.spacesloader)])
        return gitlabspaces.difference(clonedspaces)

    def getUserSpaceRights(self, ctx, space):
        spaceobject = self.spacesloader.spaces.get(space)

        if hasattr(ctx, 'env') and "user" in ctx.env['beaker.session']:
            username = ctx.env['beaker.session']["user"]
        else:
            return "", ""

        if self.isAdminFromCTX(ctx):
            return username, 'rwa'

        if self.authentication_method == 'gitlab':
            gitlabspaces = self.auth.getUserSpaces(username, spaceloader=self.spacesloader)
            localspaceswithguestaccess = self.getAccessibleLocalSpacesForGitlabUser(gitlabspaces)
            if space in localspaceswithguestaccess:
                return username, localspaceswithguestaccess[space]

        username, rights = self.auth.getUserSpaceRights(username, space, spaceobject=spaceobject)

        return username, rights

    def getUserFromCTX(self, ctx):
        user = ctx.env["beaker.session"].get('user')
        return user or "guest"

    def getGroupsFromCTX(self, ctx):
        user = self.getUserFromCTX(ctx)
        if user:
            groups = self.auth.getGroups(user)
            return [str(item.lower()) for item in groups]
        else:
            return []

    def isAdminFromCTX(self, ctx):
        usergroups = set(self.getGroupsFromCTX(ctx))
        admingroups = set(self.admingroups)
        return bool(admingroups.intersection(usergroups))

    def isLoggedInFromCTX(self, ctx):
        user = self.getUserFromCTX(ctx)
        if user != "" and user != "guest":
            return True
        return False

# router

    def startSession(self, ctx, path):
        session = ctx.env['beaker.session']
        if 'user_login_' in ctx.params and ctx.params.get('user_login_') == 'guest' and self.force_oauth_instance:
            location = '%s?%s' % ('/restmachine/system/oauth/authenticate',
                                  urllib.parse.urlencode({'type': self.force_oauth_instance}))
            raise exceptions.Redirect(location)

        # Already logged in user can't access login page again
        if 'user_logoff_' not in ctx.params and path.endswith(
                'system/login') and 'user' in session and session['user'] != 'guest':
            ctx.start_response('204', [])
            return False, []

        def process_authkey(key):
            # check if authkey is a session
            newsession = session.get_by_id(key)
            if newsession:
                ctx.env['beaker.session'] = newsession
                return True, session
            elif key == self.secret:
                session['user'] = 'admin'
                session.save()
                return True, session
            else:
                username = self.auth.getUserFromKey(key)
                if username != "guest":
                    session['user'] = username
                    session.save()
                    return True, session
                else:
                    raise exceptions.Unauthorized("Invalid authkey given")

        if "authkey" in ctx.params:
            # user is authenticated by a special key
            return process_authkey(ctx.params['authkey'])

        # validate JWT token
        if 'HTTP_AUTHORIZATION' in ctx.env:
            authorization = ctx.env['HTTP_AUTHORIZATION']
            type, _, token = authorization.partition(' ')
            if type.lower() == 'bearer':
                import jose.jwt
                try:
                    payload = jose.jwt.get_unverified_claims(token)
                    headers = jose.jwt.get_unverified_headers(token)
                except jose.JWTError:
                    raise exceptions.Unauthorized("Failed to load JWT")
                issuer = payload.get('iss', 'main')
                payload['iss'] = issuer
                for issuer, publickey in self.jwtcfg.items():
                    try:
                        jose.jws.verify(token, publickey, algorithms=[headers['alg']])
                    except jose.JWSError as e:
                        raise exceptions.Unauthorized("Failed to verify JWT {}".format(e))
                    break
                else:
                    raise exceptions.Unauthorized("Public JWT for issuer {} is not configured".format(issuer))

                session['user'] = '{username}@{iss}'.format(**payload)
                session.save()
            elif type.lower() == 'authkey':
                return process_authkey(token)

        oauth_logout_url = ''
        if "user_logoff_" in ctx.params and "user_login_" not in ctx.params:
            if session.get('user', '') not in ['guest', '']:
                # If user session is oauth session and logout url is provided, redirect user to that URL
                # after deleting session which will invalidate the oauth server session
                # then redirects user back to where he was in portal
                oauth = session.get('oauth')
                oauth_logout_url = ''
                if oauth:
                    oauth_logout_url = oauth.get('logout_url')
                session.delete()
                session = ctx.env['beaker.get_session']()
                ctx.env['beaker.session'] = session
            session['user'] = 'guest'
            session.save()
            if oauth_logout_url:
                backurl = urllib.parse.urljoin(ctx.env['HTTP_REFERER'], ctx.env['PATH_INFO'])
                ctx.start_response('302 Found', [('Location', '%s?%s' % (
                    str(oauth_logout_url), str(urllib.parse.urlencode({'redirect_uri': backurl}))))])
                return False, session
            return True, session

        if "user_login_" in ctx.params:
            # user has filled in his login details, this is response on posted info
            name = ctx.params['user_login_']
            if 'passwd' not in ctx.params:
                secret = ""
            else:
                secret = ctx.params['passwd']
            if self.auth.authenticate(name, secret):
                session['user'] = name
                session['auth_method'] = self.authentication_method

                session.save()
                # user is loging in from login page redirect him to home
                if path.endswith('system/login'):
                    status = '302'
                    headers = [
                        ('Location', "/"),
                    ]
                    ctx.start_response(status, headers)
                    return False, [""]
            else:
                session['user'] = ""
                session.save()
                return False, [self.pageprocessor.returnDoc(
                    ctx, ctx.start_response, "system", "login", extraParams={"path": path})]

        if "user" not in session or session["user"] == "":
            session['user'] = "guest"
            session.save()

        return True, session

    def _escape(self, params):
        """
        Escape html params
        """
        for k, v_list in params.items():
            escaped_vals = []
            for v in v_list:
                escaped_vals.append(j.portal.tools.html.htmlfactory.escape(v))

            params[k] = escaped_vals
        return params

    def _getParamsFromEnv(self, env, ctx, escape=True):
        params = urllib.parse.parse_qs(env["QUERY_STRING"], 1)

        if escape:
            params = self._escape(params)

        def simpleParams(params):
            # HTTP parameters can be repeated multiple times, i.e. in case of using <select multiple>
            # Example: a=1&b=2&a=3
            #
            # urlparse.parse_qs returns a dictionary of names & list of values. Then it's simplified
            # for lists with only a single element, e.g.
            #
            #   {'a': ['1', '3'], 'b': ['2']}
            #
            # simplified to be
            #
            #   {'a': ['1', '3'], 'b': '2'}
            return dict(((j.data.text.toStr(k), [j.data.text.toStr(vi) for vi in v]) if len(v) > 1 else (
                j.data.text.toStr(k), j.data.text.toStr(v[0]))) for k, v in list(params.items()))

        def hasSupportedContentType(contenttype, supportedcontenttypes):
            for supportedcontenttype in supportedcontenttypes:
                if contenttype.find(supportedcontenttype) != -1:
                    return True

        params = simpleParams(params)

        contentype = env.get('CONTENT_TYPE', '')
        pragma = env.get('HTTP_PRAGMA', '')
        if 'stream' not in pragma and env["REQUEST_METHOD"] in ("POST", "PUT") and hasSupportedContentType(
                contentype, ('application/json', 'www-form-urlencoded', 'multipart/form-data', '')):
            if contentype.find("application/json") != -1:
                postData = env["wsgi.input"].read()
                if postData.strip() == b"":
                    return params
                postParams = j.data.serializer.getSerializerType('j').loads(postData)
                if postParams:
                    params.update(postParams)
                return params
            elif contentype.find("www-form-urlencoded") != -1:
                postData = env["wsgi.input"].read()
                if postData.strip() == "":
                    return params
                params.update(dict(urllib.parse.parse_qs(postData, 1)))
                for key, val in params.items():
                    if isinstance(key, str) and isinstance(val, str):
                        continue
                    else:
                        params.pop(key)
                        params.update(simpleParams({key: val}))
                return params
            elif contentype.find("multipart/form-data") != -1 and env.get('HTTP_TRANSFER_ENCODING') != 'chunked':
                forms, files = multipart.parse_form_data(ctx.env)
                params.update(forms)
                for key, value in list(files.items()):
                    params.setdefault(key, dict())[value.filename] = value.file
            elif env.get('HTTP_TRANSFER_ENCODING') == 'chunked':
                from JumpScale9Portal.portal.html.multipart2.multipart import parse_options_header
                content_type, parameters = parse_options_header(env.get('CONTENT_TYPE'))
                boundary = parameters.get(b'boundary')
                inp = env.get('wsgi.input')
                params.update({'FILES': {'data': inp, 'boundary': boundary}})
        return params

    @property
    def requestContext(self):
        currentframe = None
        currentframe = inspect.currentframe()
        backframe = currentframe.f_back
        while backframe is not None:
            for vars in (backframe.f_locals, backframe.f_globals):
                ctx = vars.get('ctx')
                if isinstance(ctx, RequestContext):
                    return ctx
                ctx = vars.get('kwargs', {}).get('ctx')
                if isinstance(ctx, RequestContext):
                    return ctx

            backframe = backframe.f_back

    @exhaustgenerator
    def router(self, environ, start_response):
        path = environ["PATH_INFO"].lstrip("/")
        print(("path:%s" % path))
        pathparts = path.split('/')
        if pathparts[0] == 'wiki':
            pathparts = pathparts[1:]

        if path.find("favicon.ico") != -1:
            return self.pageprocessor.processor_page(environ, start_response, self.filesroot, "favicon.ico", prefix="")

        ctx = RequestContext(application="", actor="", method="", env=environ,
                             start_response=start_response, path=path, params=None)

        rest_prefixes = ['restmachine', 'restextmachine', 'rest', 'restext']
        rest_found = False
        for item in rest_prefixes:
            if path.startswith(item):
                rest_found = True
                break
        ctx.params = {}
        ctx.env['JS_CTX'] = ctx

        for proxypath, proxy in self.proxies.items():
            if path.startswith(proxypath.lstrip('/')):
                return self.pageprocessor.process_proxy(ctx, proxy)

        if rest_found:
            ctx.params = self._getParamsFromEnv(environ, ctx, escape=False)
        else:
            ctx.params = self._getParamsFromEnv(environ, ctx, escape=True)

        self.logger.info("[router]: params are %s" % ctx.params)
        if path.find("jslib/") == 0:
            path = path[6:]
            user = "None"
            # self.pageprocessor.log(ctx, user, path)
            return self.pageprocessor.processor_page(environ, start_response, self.jslibroot, path, prefix="jslib/")

        if path.find("images/") == 0:
            space, image = pathparts[1:3]
            spaceObject = self.getSpace(space)
            image = image.lower()

            if image in spaceObject.docprocessor.images:
                path2 = j.tools.path.get(spaceObject.docprocessor.images[image])

                return self.pageprocessor.processor_page(
                    environ, start_response, path2.dirname(), path2.basename(), prefix="images")
            ctx.start_response('404', [])

        if path.find("files/specs/") == 0:
            path = path[6:]
            user = "None"
            self.pageprocessor.log(ctx, user, path)
            return self.pageprocessor.processor_page(environ, start_response, self.filesroot, path, prefix="files/")

        if path.find(".files") != -1:
            user = "None"
            self.pageprocessor.log(ctx, user, path)
            space = pathparts[0].lower()
            path = "/".join(pathparts[2:])
            sploader = self.spacesloader.getSpaceFromId(space)
            filesroot = j.tools.path.get(sploader.model.path).joinpath(".files")
            return self.pageprocessor.processor_page(environ, start_response, filesroot, path, prefix="")

        if path.find(".static") != -1:
            user = "None"
            self.pageprocessor.log(ctx, user, path)
            space, pagename = self.pageprocessor.path2spacePagename(path)
            space = pathparts[0].lower()
            path = "/".join(pathparts[2:])
            sploader = self.spacesloader.getSpaceFromId(space)
            filesroot = j.tools.path.get(sploader.model.path).joinpath(".static")

            return self.pageprocessor.processor_page(
                environ, start_response, filesroot, path, prefix="", includedocs=True, ctx=ctx, space=space)

        # user is logged in now
        is_session, session = self.startSession(ctx, path)
        if not is_session:
            return session
        user = session['user']

        self.logger.info("[PortalServer] pathparts: %s" % pathparts)
        match = pathparts[0]
        path = ""
        if len(pathparts) > 1:
            path = "/".join(pathparts[1:])

        if match == "restmachine":
            return self.rest.processor_rest(environ, start_response, path, human=False, ctx=ctx)

        elif match == "elfinder":
            return self.pageprocessor.process_elfinder(path, ctx)

        elif match == "restextmachine":
            if not self.authentication_method:
                try:
                    j.clients.osis.getByInstance(self.cfg.get('instance', 'main'))
                except Exception:
                    self.pageprocessor.raiseError(
                        ctx,
                        msg="You have a minimal portal with no OSIS configured",
                        msginfo="",
                        errorObject=None,
                        httpcode="500 Internal Server Error")
            return self.rest.processor_restext(environ, start_response, path, human=False, ctx=ctx)

        elif match == "rest":
            space, pagename = self.pageprocessor.path2spacePagename(path.strip("/"))
            self.pageprocessor.log(ctx, user, path, space, pagename)
            return self.rest.processor_rest(environ, start_response, path, ctx=ctx)

        elif match == "restext":
            space, pagename = self.pageprocessor.path2spacePagename(path.strip("/"))
            self.pageprocessor.log(ctx, user, path, space, pagename)
            return self.rest.processor_restext(environ, start_response, path,
                                               ctx=ctx)
        elif match == "ping":
            status = '200 OK'
            headers = [
                ('Content-Type', "text/html"),
            ]
            start_response(status, headers)
            return ["pong"]

        elif match == "files":
            self.pageprocessor.log(ctx, user, path)
            return self.pageprocessor.processor_page(environ, start_response, self.filesroot, path, prefix="files")

        elif match == "specs":
            return self.pageprocessor.processor_page(environ, start_response, "specs", path, prefix="specs")

        elif match == "appservercode":
            return self.pageprocessor.processor_page(
                environ, start_response, "code", path, prefix="code", webprefix="appservercode")

        elif match == "lib":
            # print self.libpath
            return self.pageprocessor.processor_page(environ, start_response, self.libpath, path, prefix="lib")

        elif match == 'render':
            return self.render(environ, start_response)

        else:
            path = '/'.join(pathparts)
            path = j.portal.tools.html.htmlfactory.escape(path)
            ctx.params["path"] = path
            space, pagename = self.pageprocessor.path2spacePagename(path)
            self.pageprocessor.log(ctx, user, path, space, pagename)
            pagestring = str(self.pageprocessor.returnDoc(ctx, start_response, space, pagename, {}))
            return [pagestring]

    def render(self, environ, start_response):
        path = environ["PATH_INFO"].lstrip("/")
        query_string = environ["QUERY_STRING"].lstrip("/")
        params = cgi.parse_qs(query_string)
        content = params.get('content', [''])[0]
        space = params.get('render_space', None)
        if space:
            space = space[0]
        else:
            start_response('200 OK', [('Content-Type', "text/html")])
            return 'Parameter "space" not supplied'

        doc = params.get('render_doc', None)
        if doc:
            doc = doc[0]
        else:
            start_response('200 OK', [('Content-Type', "text/html")])
            return 'Parameter "doc" not supplied'

        ctx = RequestContext(application="", actor="", method="", env=environ,
                             start_response=start_response, path=path, params=None)
        ctx.params = self._getParamsFromEnv(environ, ctx)
        self.logger.info("[render]: params are %s" % ctx.params)

        doc, _ = self.pageprocessor.getDoc(space, doc, ctx)

        doc = doc.copy()
        doc.source = content
        doc.loadFromSource()
        doc.preprocess()

        content, doc = doc.executeMacrosDynamicWiki(ctx=ctx)

        page = self.confluence2htmlconvertor.convert(
            content,
            doc=doc,
            requestContext=ctx,
            page=self.pageprocessor.getpage(),
            paramsExtra=ctx.params)

        if 'postprocess' not in page.processparameters or page.processparameters['postprocess']:
            page.body = page.body.replace("$$space", space)
            page.body = page.body.replace("$$page", doc.original_name)
            page.body = page.body.replace("$$path", doc.path)
            page.body = page.body.replace("$$querystr", ctx.env['QUERY_STRING'])

        page.body = page.body.replace("$$$menuright", "")

        if "todestruct" in doc.__dict__:
            doc.destructed = True

        start_response('200 OK', [('Content-Type', "text/html")])
        return str(page)

    def addRoute(self, function, appname, actor, method, params, description="", auth=True, returnformat=None, httpmethod='post'):
        """
        @param function is the function which will be called as follows: function(webserver,path,params):
            function can also be a string, then only the string will be returned
            if str=='taskletengine' will directly call the taskletengine e.g. for std method calls from actors
        @appname e.g. system is 1e part of url which is routed http://localhost/appname/actor/method/
        @actor e.g. system is 2nd part of url which is routed http://localhost/appname/actor/method/
        @method e.g. "test" is part of url which is routed e.g. http://localhost/appname/actor/method/
        @auth is for authentication if false then there will be no auth key checked

        example function called

            def test(self,webserver,path,params):
                return 'hello world!!'

            or without the self in the functioncall (when no class method)

            what you return is being send to the browser

        example call: http://localhost:9999/test?key=1234&color=dd&name=dd

        """

        appname = appname.replace("_", ".")
        actor = actor.replace("_", ".")
        method = method.replace("_", ".")
        self.app_actor_dict["%s_%s" % (appname, actor)] = 1

        methoddict = {'get': 'GET', 'set': 'PUT', 'new': 'POST',
                      'delete': 'DELETE', 'find': 'GET', 'list': 'GET',
                      'datatables': 'GET', 'create': 'POST', 'post': 'POST'}
        route = {
            'func': function,
            'params': params,
            'description': description,
            'auth': auth,
            'returnformat': returnformat}
        self.routes["%s_%s_%s_%s" % (methoddict.get(httpmethod, 'POST'), appname, actor, method)] = route

# SCHEDULING

    def _timer(self):
        """
        will remember time every 0.5 sec
        """
        lfmid = 0
        while True:
            self.epoch = int(time.time())
            if lfmid < self.epoch - 200:
                lfmid = self.epoch
                self.fiveMinuteId = j.data.time.get5MinuteId(self.epoch)
                self.hourId = j.data.time.getHourId(self.epoch)
                self.dayId = j.data.time.getDayId(self.epoch)
            gevent.sleep(0.5)

    def _minRepeat(self):
        while True:
            gevent.sleep(5)
            for key in list(self.schedule1min.keys()):
                item, args, kwargs = self.schedule1min[key]
                item(*args, **kwargs)

    def _15minRepeat(self):
        while True:
            gevent.sleep(60 * 15)
            for key in list(self.schedule15min.keys()):
                item, args, kwargs = self.schedule15min[key]
                item(*args, **kwargs)

    def _60minRepeat(self):
        while True:
            gevent.sleep(60 * 60)
            for key in list(self.schedule60min.keys()):
                item, args, kwargs = self.schedule60min[key]
                item(*args, **kwargs)

    def getNow(self):
        return self.epoch

    def addSchedule1MinPeriod(self, name, method, *args, **kwargs):
        self.schedule1min[name] = (method, args, kwargs)

    def addSchedule15MinPeriod(self, name, method, *args, **kwargs):
        self.schedule15min[name] = (method, args, kwargs)

    def addSchedule60MinPeriod(self, name, method, *args, **kwargs):
        self.schedule60min[name] = (method, args, kwargs)

# START-STOP / get spaces/actors/buckets / addgreenlet

    def start(self):
        """
        Start the web server, serving the `routes`. When no `routes` dict is passed, serve a single 'test' route.

        This method will block until an exception stops the server.

        @param routes: routes to serve, will be merged with the already added routes
        @type routes: dict(string, list(callable, dict(string, string), dict(string, string)))
        """

        TIMER = gevent.greenlet.Greenlet(self._timer)
        TIMER.start()

        S1 = gevent.greenlet.Greenlet(self._minRepeat)
        S1.start()

        S2 = gevent.greenlet.Greenlet(self._15minRepeat)
        S2.start()

        S3 = gevent.greenlet.Greenlet(self._60minRepeat)
        S3.start()
        gevent.spawn(self.errorhandler.start)

        j.tools.console.echo("webserver started on port %s" % self.port)
        self._webserver.serve_forever()

    def stop(self):
        self._webserver.stop()

    def getSpaces(self):
        return list(self.spacesloader.id2object.keys())

    def getBuckets(self):
        return list(self.bucketsloader.id2object.keys())

    def getActors(self):
        return list(self.actorsloader.id2object.keys())

    def getSpace(self, name, ignore_doc_processor=False):

        name = name.lower()
        if name not in self.spacesloader.spaces:
            raise RuntimeError("Could not find space %s" % name)
        space = self.spacesloader.spaces[name]
        return space

    def getBucket(self, name):
        if name not in self.bucketsloader.buckets:
            raise RuntimeError("Could not find bucket %s" % name)
        bucket = self.bucketsloader.buckets(name)
        return bucket

    def addGreenlet(self, appName, greenlet):
        """
        """
        greenletObject = greenlet()
        if greenletObject.method == "":
            raise RuntimeError("greenlet class needs to have a method")
        if greenletObject.actor == "":
            raise RuntimeError("greenlet class needs to have a actor")

        greenletObject.server = self
        self.addRoute(function=greenletObject.wscall,
                      appname=appName,
                      actor=greenletObject.actor,
                      method=greenletObject.method,
                      paramvalidation=greenletObject.paramvalidation,
                      paramdescription=greenletObject.paramdescription,
                      paramoptional=greenletObject.paramoptional,
                      description=greenletObject.description, auth=greenletObject.auth)

    def restartInProcess(self, app):
        import fcntl
        args = sys.argv[:]
        args.insert(0, sys.executable)
        apppath = j.sal.fs.joinPaths(j.dirs.JSAPPSDIR, app)
        max_fd = 1024
        for fd in range(3, max_fd):
            try:
                flags = fcntl.fcntl(fd, fcntl.F_GETFD)
            except IOError:
                continue
            fcntl.fcntl(fd, fcntl.F_SETFD, flags | fcntl.FD_CLOEXEC)
        os.chdir(apppath)
        os.execv(sys.executable, args)

    def __str__(self):
        out = ""
        for key, val in list(self.__dict__.items()):
            if key[0] != "_" and key not in ["routes"]:
                out += "%-35s :  %s\n" % (key, val)
        routes = ",".join(list(self.routes.keys()))
        out += "%-35s :  %s\n" % ("routes", routes)
        items = sorted(out.split("\n"))
        out = "portalserver:" + "\n".join(items)
        return out

    __repr__ = __str__

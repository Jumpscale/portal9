from js9 import j

import requests
import mimeparse
import mimetypes
import types
import os
import pprint
from JumpScale.portal.portal import exceptions
import urllib.request
import urllib.parse
import urllib.error


BLOCK_SIZE = 4096

CONTENT_TYPE_JSON = 'application/json'
CONTENT_TYPE_JS = 'application/javascript'
CONTENT_TYPE_YAML = 'application/yaml'
CONTENT_TYPE_PLAIN = 'text/plain'
CONTENT_TYPE_HTML = 'text/html'
CONTENT_TYPE_PNG = 'image/png'


class PageProcessor():

    def __init__(self):
        self.logdir = j.tools.path.get(j.dirs.logDir).joinpath("portal", str(j.portal.server.active.port))
        self.logdir.makedirs_p()

    def getpage(self):
        page = j.portal.tools.docgenerator.pageNewHTML("index.html", htmllibPath="/jslib")
        return page

    def sendpage(self, page, start_response):
        contenttype = "text/html"
        start_response('200 OK', [('Content-Type', contenttype), ])
        return [page.getContent()]

    def getDoc(self, space, name, ctx, params={}):
        session = ctx.env['beaker.session']
        loggedin = session.get('user', '') not in ['guest', '']
        standard_pages = ["login", "error", "accessdenied", "pagenotfound"]
        spacedocgen = None

        print(("GETDOC:%s" % space))
        space = space.lower()
        name = name.lower()

        if not space:
            space = self.defaultspace.lower()
            name = self.defaultpage

        if space not in j.portal.server.active.spacesloader.spaces:
            if space == "system":
                raise RuntimeError("wiki has not loaded system space, cannot continue")
            ctx.params["error"] = "Could not find space %s\n" % space
            print(("could not find space %s" % space))
            space = self.defaultspace or 'system'
            name = "pagenotfound"
        else:
            spaceObject = j.portal.server.active.spacesloader.getLoaderFromId(space)
            spacedocgen = spaceObject.docprocessor

            if name in spacedocgen.name2doc:
                pass
            # One of the standard pages not found in that space, fall back to
            # system space
            elif name in standard_pages:
                space = "system"
                spacedocgen = None
            elif name == "":
                if space in spacedocgen.name2doc:
                    name = space
                elif "home" in spacedocgen.name2doc:
                    name = 'home'
                else:
                    ctx.params["path"] = "space:%s pagename:%s" % (space, name)
                    name = "pagenotfound"
                    spacedocgen = None
            else:
                ctx.params["path"] = "space:%s pagename:%s" % (space, name)
                name = "pagenotfound"
                spacedocgen = None

        username, right = j.portal.server.active.getUserSpaceRights(ctx, space)

        if name in standard_pages:
            if "r" not in right:
                right = "r" + right

        if "r" not in right:
            if j.portal.server.active.force_oauth_instance and not loggedin:
                name = "accessdenied"
            elif not loggedin:
                name = "login"
            else:
                name = "accessdenied"

            if not spaceObject.docprocessor.docExists(name):
                space = 'system'
                spacedocgen = None

        ctx.params["rights"] = right
        print(("# space:%s name:%s user:%s right:%s" %
               (space, name, username, right)))

        params['space'] = space
        params['name'] = name

        if not spacedocgen:
            doc, params = self.getDoc(space, name, ctx, params)
        else:
            doc = spacedocgen.name2doc[name]

        doc.loadFromDisk()

        if name == "pagenotfound":
            ctx.start_response("404 Not found", [('Content-Type', 'text/html')])
        elif name == 'accessdenied':
            ctx.start_response("403 Not authorized", [('Content-Type', 'text/html')])

        return doc, params

    def returnDoc(self, ctx, start_response, space, docname, extraParams={}):
        doc, params = self.getDoc(space, docname, ctx, params=ctx.params)

        if doc.dirty or "reload" in ctx.params:
            doc.loadFromDisk()
            doc.preprocess()

        ctx.params.update(extraParams)

        # doc.applyParams(ctx.params)
        ctx.start_response('200 OK', [('Content-Type', "text/html"), ])
        return doc.getHtmlBody(paramsExtra=extraParams, ctx=ctx)

    def processor_page(self, environ, start_response, wwwroot, path, prefix="",
                       webprefix="", index=False, includedocs=False, ctx=None, space=None):
        def indexignore(item):
            ext = item.split(".")[-1].lower()
            if ext in ["pyc", "pyo", "bak"]:
                return True
            if item[0] == "_":
                return True
            if item[0] == ".":
                return True
            return False

        def formatContent(contenttype, path, template, start_response):
            content = j.tools.path.get(path).text()
            page = self.getpage()
            page.addCodeBlock(content, template, edit=True)
            start_response('200 OK', [('Content-Type', contenttype), ])
            return [str(page)]

        def processHtml(contenttype, path, start_response, ctx, space):
            content = j.tools.path.get(path).text()
            r = r"\[\[.*\]\]"  # TODO: does not seem right to me
            for match in j.tools.code.regex.yieldRegexMatches(r, content):
                docname = match.founditem.replace("[", "").replace("]", "")
                doc, params = self.getDoc(space, docname, ctx, params=ctx.params)

                if doc.name == 'pagenotfound':
                    content = content.replace(match.founditem, "*****CONTENT '%s' NOT FOUND******" % docname)
                else:
                    content2, doc = doc.executeMacrosDynamicWiki(paramsExtra={}, ctx=ctx)

                    page = self.confluence2htmlconvertor.convert(
                        content2, doc=doc, requestContext=ctx, page=self.getpage(), paramsExtra=ctx.params)

                    page.body = page.body.replace("$$space", space)
                    page.body = page.body.replace("$$page", doc.original_name)
                    page.body = page.body.replace("$$path", doc.path)
                    page.body = page.body.replace("$$querystr", ctx.env['QUERY_STRING'])
                    page.body = page.body.replace("$$$menuright", "")

                    content = content.replace(match.founditem, page.body)

            start_response('200 OK', [('Content-Type', "text/html"), ])
            return [content]

        def removePrefixes(path):
            path = path.replace("\\", "/")
            path = path.replace("//", "/")
            path = path.replace("//", "/")
            while len(path) > 0 and path[0] == "/":
                path = path[1:]
            while path.find(webprefix + "/") == 0:
                path = path[len(webprefix) + 1:]
            while path.find(prefix + "/") == 0:
                path = path[len(prefix) + 1:]
            return path

        def send_file(file_path, size):
            # print "sendfile:%s" % path
            f = open(file_path, "rb")
            block = f.read(BLOCK_SIZE * 10)
            BLOCK_SIZE2 = 0
            # print "%s %s" % (file_path,size)
            while BLOCK_SIZE2 < size:
                BLOCK_SIZE2 += len(block)
                # print BLOCK_SIZE2
                # print len(block)
                yield block
                block = f.read(BLOCK_SIZE)
            # print "endfile"

        wwwroot = wwwroot.replace("\\", "/").strip()

        path = removePrefixes(path)

        # print "wwwroot:%s" % wwwroot
        if not wwwroot.replace("/", "") == "":
            pathfull = wwwroot + "/" + path

        else:
            pathfull = path

        contenttype = "text/html"
        content = ""
        headers = list()
        ext = path.split(".")[-1].lower()
        contenttype = mimetypes.guess_type(pathfull)[0] or 'text/html'

        if path == "favicon.ico":
            pathfull = "wiki/System/favicon.ico"
        else:
            if not os.path.abspath(pathfull).startswith(os.path.abspath(wwwroot)):
                raise exceptions.NotFound('Not found')

        pathfull = j.tools.path.get(pathfull)
        if not pathfull.exists():
            if j.tools.path.get(pathfull + '.gz').exists() and 'gzip' in environ.get('HTTP_ACCEPT_ENCODING'):
                pathfull = j.tools.path.get(pathfull + '.gz')
                headers.append(('Vary', 'Accept-Encoding'))
                headers.append(('Content-Encoding', 'gzip'))
            else:
                print("error")
                headers = [('Content-Type', contenttype), ]
                start_response("404 Not found", headers)
                return [("path %s not found" % path)]

        size = pathfull.getsize()

        if ext == "html":
            return processHtml(contenttype, pathfull, start_response, ctx, space)
        elif ext == "wiki":
            contenttype = "text/html"
            # return formatWikiContent(pathfull,start_response)
            return formatContent(contenttype, pathfull, "python", start_response)
        elif ext == "py":
            contenttype = "text/html"
            return formatContent(contenttype, pathfull, "python", start_response)
        elif ext == "spec":
            contenttype = "text/html"
            return formatContent(contenttype, pathfull, "python", start_response)

        # print contenttype

        status = '200 OK'

        headers.append(('Content-Type', contenttype))
        headers.append(("Content-length", str(size)))
        headers.append(("Cache-Control", 'public,max-age=3600'))

        start_response(status, headers)

        if content != "":
            return [content]
        else:
            return send_file(pathfull, size)

    def process_elfinder(self, path, ctx):
        from JumpScale.portal.html import elFinder
        db = j.data.kvs.getRedisCacheLocal()
        rootpath = db.get(path)
        options = {'root': rootpath, 'dotFiles': True}
        con = elFinder.connector(options)
        params = ctx.params.copy()

        if params.get('init') == '1':
            params.pop('target', None)
        status, header, response = con.run(params)
        status = '%s' % status
        headers = [(k, v) for k, v in list(header.items())]
        ctx.start_response(status, headers)
        if 'download' not in params:
            response = j.data.serializer.serializers.getSerializerType('j').dumps(response)
        else:
            response = response.get('content')
        return [response]

    def process_proxy(self, ctx, proxy):
        path = ctx.env['PATH_INFO']
        method = ctx.env['REQUEST_METHOD']
        query = ctx.env['QUERY_STRING']
        headers = {}
        for name, value in ctx.env.items():
            if name.startswith('HTTP_'):
                headers[name[5:].replace('_', '-')] = value
        desturl = proxy['dest'] + path[len(proxy['path']):]
        if query:
            desturl += "?%s" % query
        req = requests.Request(method, desturl, data=ctx.env['wsgi.input'], headers=headers).prepare()
        session = requests.Session()
        resp = session.send(req, stream=True)
        ctx.start_response('%s %s' % (resp.status_code, resp.reason), headers=list(resp.headers.items()))
        for chunk in resp.raw:
            yield chunk

    def path2spacePagename(self, path):

        pagename = ""
        if path.find("?") != -1:
            path = path.split("?")[0]
        while len(path) > 0 and path[-1] == "/":
            path = path[:-1]
        if path.find("/") == -1:
            space = path.strip()
        else:
            splitted = path.split("/")
            space = splitted[0].lower()
            pagename = splitted[-1].lower()

        return space, pagename

    # FORMATTING + logs/raiseerror
    def log(self, ctx, user, path, space="", pagename=""):
        path2 = self.logdir.joinpath("user_%s.log" % user)

        epoch = j.data.time.getTimeEpoch() + 3600 * 6
        hrtime = j.data.time.epoch2HRDateTime(epoch)

        # TODO: fix geoip, also make sure nginx forwards the right info
        if False and self.geoIP is not None:
            ee = self.geoIP.record_by_addr(ctx.env["REMOTE_ADDR"])
            loc = "%s_%s_%s" % (ee["area_code"], ee["city"], ee["region_name"])
        else:
            loc = ""

        msg = "%s|%s|%s|%s|%s|%s|%s\n" % (hrtime, ctx.env["REMOTE_ADDR"], epoch, space, pagename, path, loc)
        j.sal.fs.writeFile(path2, msg, True)

        if space != "":
            msg = "%s|%s|%s|%s|%s|%s|%s\n" % (hrtime, ctx.env["REMOTE_ADDR"], epoch, user, pagename, path, loc)
            pathSpace = self.logdir.joinpath("space_%s.log" % space)
            j.sal.fs.writeFile(pathSpace, msg, True)

    def raiseError(self, ctx, msg="", msginfo="", errorObject=None, httpcode="500 Internal Server Error"):
        """
        """
        if not ctx.checkFormat():
            # error in format
            eco = j.errorconditionhandler.getErrorConditionObject()
            eco.errormessage = "only format supported = human or json, format is put with param &format=..."
            eco.type = "INPUT"
            print("WRONG FORMAT")
        else:
            if errorObject is not None:
                eco = errorObject
            else:
                eco = j.errorconditionhandler.getErrorConditionObject()

        method = ctx.env["PATH_INFO"]
        remoteAddress = ctx.env["REMOTE_ADDR"]
        queryString = ctx.env["QUERY_STRING"]

        eco.caller = remoteAddress
        if msg != "":
            eco.errormessage = msg
        else:
            eco.errormessage = ""
        if msginfo != "":
            eco.errormessage += "\msginfo was:\n%s" % msginfo
        if queryString != "":
            eco.errormessage += "\nquerystr was:%s" % queryString
        if method != "":
            eco.errormessage += "\nmethod was:%s" % method

        eco.process()

        if ctx.fformat == "human" or ctx.fformat == "text":
            if msginfo is not None and msginfo != "":
                msg += "\n<br>%s" % msginfo
            else:
                msg += "\n%s" % eco
                msg = self._text2html(msg)

        else:
            # is json
            # result=[]
            # result["error"]=eco.obj2dict()
            def todict(obj):
                data = {}
                for key, value in list(obj.__dict__.items()):
                    try:
                        data[key] = todict(value)
                    except AttributeError:
                        data[key] = value
                return data
            eco.tb = ""
            eco.frames = []
            msg = j.data.serializer.serializers.getSerializerType('j').dumps(todict(eco))

        ctx.start_response(httpcode, [('Content-Type', 'text/html')])

        j.tools.console.echo(
            "***ERROR***:%s : method %s from ip %s with params %s" %
            (eco, method, remoteAddress, queryString), 2)
        if j.application.debug:
            return msg
        else:
            return "An unexpected error has occurred, please try again later."

    def _text2html(self, text):
        text = text.replace("\n", "<br>")
        # text=text.replace(" ","&nbsp; ")
        return text

    def _text2htmlSerializer(self, content):
        return self._text2html(pprint.pformat(content))

    def _resultjsonSerializer(self, content):
        return j.data.serializer.serializers.getSerializerType('j').dumps({"result": content})

    def _resultyamlSerializer(self, content):
        return j.tools.code.object2yaml({"result": content})

    def getMimeType(self, contenttype, format_types, result=None):
        supported_types = [
            "text/plain", "text/html", "application/yaml", "application/json"]
        CONTENT_TYPES = {
            "text/plain": str,
            "text/html": self._text2htmlSerializer,
            "application/yaml": self._resultyamlSerializer,
            "application/json": j.data.serializer.serializers.getSerializerType('j').dumps
        }

        if not contenttype:
            serializer = format_types["text"]["serializer"]
            return CONTENT_TYPE_HTML, serializer
        elif isinstance(result, types.GeneratorType):
            return 'application/octet-stream', lambda x: x
        else:
            return 'application/json', CONTENT_TYPES['application/json']
            # TODO (*3*)
            mimeType = mimeparse.best_match(supported_types, contenttype)
            serializer = CONTENT_TYPES[mimeType]
            return mimeType, serializer

    def reformatOutput(self, ctx, result, restreturn=False):
        FFORMAT_TYPES = {
            "text": {"content_type": CONTENT_TYPE_HTML, "serializer": self._text2htmlSerializer},
            "html": {"content_type": CONTENT_TYPE_HTML, "serializer": self._text2htmlSerializer},
            "raw": {"content_type": CONTENT_TYPE_PLAIN, "serializer": str},
            "jsonraw": {"content_type": CONTENT_TYPE_JSON, "serializer": j.data.serializer.serializers.getSerializerType('j').dumps},
            "json": {"content_type": CONTENT_TYPE_JSON, "serializer": self._resultjsonSerializer},
            "yaml": {"content_type": CONTENT_TYPE_YAML, "serializer": self._resultyamlSerializer}
        }

        if '_jsonp' in ctx.params:
            result = {'httpStatus': ctx.httpStatus,
                      'httpMessage': ctx.httpMessage, 'body': result}
            return CONTENT_TYPE_JS, "%s(%s);" % (
                ctx.params['_jsonp'], j.data.serializer.serializers.getSerializerType('j').dumps(result))

        if ctx._response_started:
            return None, result

        fformat = ctx.fformat

        if '_png' in ctx.params:
            return CONTENT_TYPE_PNG, result

        if "CONTENT_TYPE" not in ctx.env:
            ctx.env['CONTENT_TYPE'] = CONTENT_TYPE_PLAIN

        if ctx.env['CONTENT_TYPE'].find("form-") != -1:
            ctx.env['CONTENT_TYPE'] = CONTENT_TYPE_PLAIN
        # normally HTTP_ACCEPT defines the return type we should rewrite this
        if fformat:
            # extra format paramter overrides http_accept header
            return FFORMAT_TYPES[fformat]['content_type'], FFORMAT_TYPES[fformat]['serializer'](result)
        else:
            if 'HTTP_ACCEPT' in ctx.env:
                returntype = ctx.env['HTTP_ACCEPT']
            else:
                returntype = ctx.env['CONTENT_TYPE']
            content_type, serializer = self.getMimeType(returntype, FFORMAT_TYPES, result)
            return content_type, serializer(result)

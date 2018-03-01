from js9 import j
import re
import os
import jinja2
import os.path
import copy

jenv = jinja2.Environment(variable_start_string="${", variable_end_string="}")

fs = j.sal.fs


class HeaderTools():

    @staticmethod
    def getHeadnr(line):
        if line.find(".") != -1:
            part1, part2 = line.strip().split(".", 1)
            part1 = part1.lower()
            headingnr = int(part1.replace("h", ""))
            return headingnr, part2
        else:
            return None, line

    @staticmethod
    def findLowestHeading(content):
        lowest = None
        for line in content.split("\n"):
            if re.match(r"\Ah\d+\. ", line, re.IGNORECASE):
                hnr, line = HeaderTools.getHeadnr(line)
                if lowest is None or hnr < lowest:
                    lowest = hnr
        return lowest


def _escape(object, cb):
    if isinstance(object, dict):
        for key, value in object.items():
            if isinstance(key, str):
                object.pop(key)
                object[cb(key)] = value
            object[key] = _escape(value, cb)
    elif isinstance(object, list):
        for idx, value in enumerate(object):
            object[idx] = _escape(value, cb)
    elif isinstance(object, str):
        return cb(object)
    return object


class Doc(object):

    def __init__(self, docpreprocessor):
        self.jenv = jenv
        self.name = ""
        self.appliedparams = dict()
        self.alias = []
        self.pagename = ""
        self.source = ""
        self.requiredargs = []
        self.author = []
        self.products = []
        self.visibility = ["public"]  # std PUBLIC,INTERNAL
        self.visible = True
        self.destructed = False
        self.docContentChanged = False
        self.content = ""
        self.path = ""
        self._mtime = 0
        self.shortpath = ""
        self.md5 = ""
        self.title = ""
        self.tags = ""  # jumpscale tags & labels
        self.type = ""  # def,concept,releasnote,...
        self.contenttype = "C"  # C or RST
        self.parent = ""
        self.generate = True
        self.order = 0
        self.children = []  # list of docs which are the children
        self.images = {}
        self.preprocessor = docpreprocessor
        self.dirty = True  # means document needs to be processed again e.g. macro's
        self.params = []
        self.docparams = {}
        self.defaultPath = ""
        self.usedefault = False
        self.navigation = ""
        self.key = j.data.idgenerator.generateGUID()
        self.htmlHeadersCustom = []  # are extra html elements to be used which do not come from wiki
        self.htmlBodiesCustom = []
        self.processDefs = False
        self.space_path = None
        self.md = False

    def copy(self):
        newdoc = Doc(self.preprocessor)
        newdoc.__dict__ = self.__dict__.copy()
        return newdoc

    def getSpaceName(self):
        return self.preprocessor.spacename

    def getPageKey(self):
        key = j.data.hash.md5_string("%s_%s" % (self.pagename, self.getSpaceName()))
        j.portal.tools.server.active.pageKey2doc[key] = self
        return key

    def checkVisible(self, visibility):
        if "*" in self.visibility:
            self.visible = True
            return
        if visibility == []:
            self.visible = True
            return
        for item in visibility:
            if item in self.visibility:
                self.visible = True
                return
        self.visible = False

    def loadFromDisk(self, preprocess=True):
        # If the page was erased, clear the content
        if not os.path.exists(self.path):
            self.source = ''
            return

        stat = os.stat(self.path)
        if stat.st_mtime > self._mtime:
            self._mtime = stat.st_mtime
            self.source = fs.fileGetTextContents(self.path)

        self.source = self.source.replace("\r\n", "\n")
        self.source = self.source.replace("\n\r", "\n")
        self.source = self.source.replace("\r", "\n")
        self.loadFromSource(preprocess)

    def loadFromSource(self, preprocess=True):
        self.content = self.source
        if "@usedefault" in self.content:
            self.usedefault = True
        elif "@nodefault" in self.content:
            self.usedefault = False
        templates_def = re.findall(r'^@template\s+(.*?)\n', self.content)
        if templates_def:
            template_name = templates_def[0]
        else:
            template_name = None
        if self.md:
            extension = 'md'
        else:
            extension = 'wiki'

        if template_name:
            template_path = fs.joinPaths(self.preprocessor.space_path, ".space", "%s.%s" % (template_name, extension))
            template = fs.fileGetContents(template_path)
            self.content = template.replace('{content}', self.source)
        elif self.defaultPath and self.usedefault:
            extension = fs.getFileExtension(self.path)
            # if extension == 'md':
            #     self.content = self.source
            # else:
            try:
                self.defaultPath = fs.joinPaths(self.preprocessor.space_path, ".space", 'default.%s' % extension)
                default = fs.fileGetTextContents(self.defaultPath)
                self.content = default.replace("{content}", self.source)
            except Exception:
                pass

        if preprocess and self.source.strip() != "":
            # print path3
            j.portal.tools.docpreprocessor.docparser.parseDoc(self)
            self.preprocess()

    def fixMinHeadingLevel(self, minLevel):
        """
        make sure min heading level is followed
        """
        minLevel = int(minLevel)
        minLevelInDoc = 100
        for line in self.content.split("\n"):
            if line.lower().strip()[0:3] in ["h1.", "h2.", "h3.", "h4.", "h5.", "h6.", "h7."]:
                # found title
                level = int(line.split(".")[0].replace("h", ""))
                if level < minLevelInDoc:
                    minLevelInDoc = level
        content = ""
        if minLevelInDoc < minLevel:
            extra = minLevel - minLevelInDoc
            for line in self.content.split("\n"):
                if line.lower().strip()[0:3] in ["h1.", "h2.", "h3.", "h4.", "h5.", "h6.", "h7."]:
                    # found title
                    level = int(line.split(".")[0].replace("h", ""))
                    line = "h%s. %s" % (level + extra, ".".join(line.split(".")[1:]))
                content += "%s\n" % line
            self.content = content

    def _convertToInternalFormat(self):
        if self.contenttype == "RST":
            raise RuntimeError("Cannot convert from RST to Confluence, needs to be implemented")
            self.contenttype = "C"

    def preprocess(self):
        """
        make sure format is confluence
        execute macro's
        fix min heading level
        clean format in preprocessing
        """
        if self.source == "":
            self.loadFromDisk()

        # print "preprocess %s" % self.name
        self._convertToInternalFormat()
        self.findParams()
        self.executeMacrosPreprocess()
        self.clean()
        self.dirty = False

    def getHtmlBody(self, paramsExtra={}, ctx=None):
        if self.source == "":
            self.loadFromDisk()
            self.preprocess()
        if self.dirty or (ctx is not None and "reload" in ctx.params):
            self.loadFromDisk()
            self.preprocess()
        content, doc = self.executeMacrosDynamicWiki(paramsExtra, ctx)

        if self.md:
            convertor = j.portal.tools.docgenerator.docgeneratorfactory.getMarkDown2ConfluenceConvertor()
            content = convertor.convert(content)

        ws = j.portal.tools.server.active
        page = ws.confluence2htmlconvertor.convert(
            content,
            doc=self,
            requestContext=ctx,
            page=ws.pageprocessor.getpage(),
            paramsExtra=ctx.params)
        if 'postprocess' not in page.processparameters or page.processparameters['postprocess']:
            page.body = page.body.replace("$$space", self.getSpaceName())
            page.body = page.body.replace("$$page", self.original_name)
            page.body = page.body.replace("$$path", self.path)
            page.body = page.body.replace("$$querystr", ctx.env['QUERY_STRING'])

        page.body = page.body.replace("$$$menuright", "")
        if "todestruct" in doc.__dict__:
            doc.destructed = True
        return str(page)

    def findParams(self):
        if self.source == "":
            self.loadFromDisk()

        if self.content.strip() == "":
            return

        result = j.data.regex.findAll("\$\$\w*", self.content)  # finds $$...

        result3 = []
        for item in result:  # make unique
            item = item.replace("$$", "")
            if item not in result3:
                result3.append(item.strip().lower())

        result3.sort()
        result3.reverse()  # makes sure we will replace the longest statements first when we fill in the params
        self.params = result3

    def applyParams(self, params, findfresh=False, content=None):
        """
        @param params is dict with as key the name (lowercase)
        """
        isdoccontent = content == self.content
        if findfresh:
            self.findParams()

        if params:
            self.appliedparams.update(params)
        if len(self.params) > 0:
            for param in self.params:
                if param in params:
                    if content is None:
                        content = re.sub("\$\$%s(?!\w)" % param, str(params[param]), self.content)
                    else:
                        content = re.sub("\$\$%s(?!\w)" % param, str(params[param]), content)
        if isdoccontent:
            self.content = content
        return content

    def applyTemplate(self, params, escape=False):
        appliedparams = copy.deepcopy(params)
        if escape:
            ws = j.portal.tools.server.active
            appliedparams = _escape(appliedparams, ws.confluence2htmlconvertor.escape)

        self.appliedparams.update(appliedparams)
        self.content = self.jenv.from_string(self.content).render(**appliedparams)
        self.title = self.jenv.from_string(self.title).render(**params)

    def executeMacrosPreprocess(self):
        if self.source == "":
            self.loadFromDisk()
        self.preprocessor.macroexecutorPreprocessor.execMacrosOnDoc(self)

    def executeMacrosDynamicWiki(self, paramsExtra={}, ctx=None):
        # print "execute dynamic %s" % self.name
        if self.docparams != {}:
            for key in list(self.docparams.keys()):
                paramsExtra[key] = self.docparams[key]

        if "page" not in paramsExtra:
            paramsExtra["page"] = self.original_name

        if "space" not in paramsExtra:
            paramsExtra["space"] = self.getSpaceName()

        self.content = self.content or self.source
        return self.preprocessor.macroexecutorWiki.execMacrosOnContent(
            content=self.content, doc=self, paramsExtra=paramsExtra, ctx=ctx)

    def generate2disk(self, outpath):
        if self.generate and self.visible:
            dirpath = fs.joinPaths(outpath, self.pagename)
            filepath = fs.joinPaths(dirpath, "%s.txt" % self.pagename)
            fs.createDir(dirpath)
            for image in self.images:
                if image in self.preprocessor.images:
                    filename = "%s_%s" % (self.pagename, image)
                self.content = self.content.replace("!%s" % image, "!%s" % filename)
                fs.copyFile(self.preprocessor.images[image], fs.joinPaths(dirpath, filename))
            fs.writeFile(filepath, self.content)
            for doc in self.children:
                doc.generate(dirpath)

    def clean(self, startHeading=None):
        if self.pagename == "":
            self.pagename = self.name
        out = ""
        linenr = 1
        lastLineWasEmpty = False
        lowestHeading = HeaderTools.findLowestHeading(self.content)
        lastLineWasHeading = False
        for line in self.content.split("\n"):
            if line.strip() == "" and linenr == 1:
                continue
            linenr += 1
            if line.strip() == "":
                # if lastLineWasEmpty:
                #     continue
                out += "\n"
                # lastLineWasEmpty = True
                continue
            if lastLineWasHeading and lastLineWasEmpty is False:
                out += "\n"
            lastLineWasHeading = False
            lastLineWasEmpty = False
            # if line.strip()[0]=="#":
            #    continue
            if re.match(r"\Ah\d+\. ", line, re.IGNORECASE):
                lastLineWasHeading = True
                hnr, line2 = HeaderTools.getHeadnr(line)

                if startHeading is not None:
                    hnr = hnr - lowestHeading + startHeading
                line = "h%s.%s" % (hnr, line2)
            out += line + "\n"
        self.content = out

    def __str__(self):
        ss = ""
        ss += "%s\n" % self.name
        ss += "parent:%s\n" % self.parent
        ss += "%s\n" % self.type
        ss += "%s\n" % self.alias
        ss += "%s\n" % self.pagename
        ss += "%s\n" % self.author
        ss += "%s\n" % self.products
        ss += "%s\n" % self.visibility
        ss += "%s\n" % self.path
        ss += "%s\n" % self.shortpath
        ss += "%s\n" % self.md5
        ss += "%s\n" % self.tags
        return ss

    def __repr__(self):
        return self.__str__()


class DocMD(Doc):

    def __init__(self, docpreprocessor):
        Doc.__init__(self, docpreprocessor)
        self.md = True

    # def getHtmlBody(self, paramsExtra={}, ctx=None):
    #     if self.source == "":
    #         self.loadFromDisk()
    #         self.preprocess()
    #     if self.dirty or (ctx != None and "reload" in ctx.params):
    #         self.loadFromDisk()
    #         self.preprocess()
    #     loader = jinja2.FileSystemLoader(self.defaultPath.split('.space')[0])
    #     env = jinja2.Environment(variable_start_string="${", variable_end_string="}", loader=loader)
    #     jinja2html = env.get_or_select_template(self.name).render()
    #     self.content = jinja2html
    #     content, doc = self.executeMacrosDynamicWiki(paramsExtra, ctx)
    #     content, doc = self.executeMarkDownMacro(paramsExtra, ctx)
    #     self.content = content
    #     content, doc = self.executePageMacro(paramsExtra, ctx)
    #     return content

    # def executePageMacro(self, paramsExtra, ctx):
    #     page = j.tools.docgenerator.pageNewHTML('temp')
    # return
    # self.preprocessor.macroexecutorPage.execMacrosOnContent(content=self.content,
    # doc=self, paramsExtra=paramsExtra, ctx=ctx, page=page, markdown=True)

    # def executeMarkDownMacro(self, paramsExtra, ctx):
    #     page = j.tools.docgenerator.pageNewHTML('temp')
    # return
    # self.preprocessor.macroexecutorMarkDown.execMacrosOnContent(content=self.content,
    # doc=self, paramsExtra=paramsExtra, ctx=ctx, page=page)

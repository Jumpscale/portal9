from js9 import j
from JumpScale9Portal.portal.docgenerator.Page import Page
import traceback
import re


class MacroExecutorBase(object):

    def __init__(self, macrodirs=[]):
        self.taskletsgroup = dict()
        self.addMacros(macrodirs, None)

    def addMacros(self, macrodirs, spacename):
        spacename = spacename.lower() if spacename else None
        taskletsgroup = j.tools.taskletengine.getGroup()
        for macrodir in macrodirs:
            if j.sal.fs.exists(macrodir):
                taskletsgroup.addTasklets(macrodir)
        self.taskletsgroup[spacename] = taskletsgroup

    def getMacroCandidates(self, txt):
        txt = '\n%s' % txt
        reg = re.compile("\\n[^#\{]*\{\{[^\}]*\}\}")
        matches = reg.findall(txt)
        matches = ['{{%s' % ''.join(match.split('{{')[1]) for match in matches]
        return matches

    def _getTaskletGroup(self, doc, macrospace, macro):
        # if macrospace specified check there first
        spacename = doc.getSpaceName().lower()
        if macrospace is not None:
            macrospace = macrospace or None
            if macrospace:
                j.portal.tools.server.active.spacesloader.spaces[macrospace].loadDocProcessor()
            if macrospace in self.taskletsgroup and self.taskletsgroup[macrospace].hasGroup(macro):
                return self.taskletsgroup[macrospace]
        # else check in document space
        if spacename in self.taskletsgroup and self.taskletsgroup[spacename].hasGroup(macro):
            return self.taskletsgroup[spacename]
        # last fall back to default macros
        if self.taskletsgroup[macrospace].hasGroup(macro):
            return self.taskletsgroup[macrospace]
        return None

    def parseMacroStr(self, macrostr):
        """
        @param macrostr full string like {{test something more}}
        @return macroname,jumpscaletags
        """
        cmdstr = macrostr.replace("{{", "").replace("}}", "").strip()
        if cmdstr.find("\n") != -1:
            # multiline
            cmdbody = "\n".join(cmdstr.split("\n")[1:])
            cmdstr = cmdstr.split("\n")[0]
        else:
            cmdbody = ""
        if cmdstr.find(" ") > cmdstr.find(":") or (cmdstr.find(" ") == -1 and cmdstr.find(":") != -1):
            macro = cmdstr.split(":")[0].lower()
        elif cmdstr.find(" ") < cmdstr.find(":") or (cmdstr.find(":") == -1 and cmdstr.find(" ") != -1):
            macro = cmdstr.split(" ")[0].lower()
        else:
            macro = cmdstr.lower()

        tags = j.data.tags.getObject(cmdstr)

        if cmdstr.strip().find(macro) == 0:
            cmdstr = cmdstr.strip()[len(macro):]
            while len(cmdstr) > 0 and (cmdstr[0] == " " or cmdstr[0] == ":"):
                cmdstr = cmdstr[1:]

        if cmdbody != "":
            cmdstr = cmdbody

        macroparts = macro.split('.', 1)
        if len(macroparts) == 2:
            space, macro = macroparts
        else:
            space = None

        return space, macro, tags, cmdstr

    def findMacros(self, doc, content=None):
        """
        """
        if content is None:
            content = doc.content
        text = content.strip()
        if text == "":
            return []
        result = []
        for macrostr in self.getMacroCandidates(text):  # make unique
            macrospace, macro, tags, cmd = self.parseMacroStr(macrostr)
            if self._getTaskletGroup(doc, macrospace, macro):
                result.append((macrostr, macrospace, macro, tags, cmd))
        return result


class MacroExecutorPreprocess(MacroExecutorBase):

    def __init__(self, *args, **kwargs):
        self.priority = dict()
        super(MacroExecutorPreprocess, self).__init__(*args, **kwargs)

    def addMacros(self, macrodirs, spacename):
        taskletgroup = j.tools.taskletengine.getGroup()
        self.taskletsgroup[spacename] = taskletgroup
        priority = dict()
        self.priority[spacename] = priority
        for macrodir in macrodirs:
            if not j.sal.fs.exists(path=macrodir):
                continue
            taskletgroup.addTasklets(macrodir)
            cfg = j.sal.fs.joinPaths(macrodir, "prio.cfg")
            if j.sal.fs.exists(cfg):
                lines = j.sal.fs.fileGetContents(cfg).split("\n")
                for line in lines:
                    prio, macroname = line.split(":")
                    priority[macroname] = int(prio)

    def _executeMacroOnDoc(self, macrostr, macrospace, macro, tags, cmdstr, doc, paramsExtra=None):
        """
        find macro's in a doc & execute the macro
        a doc is a document in preprocessor phase
        """
        if not paramsExtra:
            paramsExtra = {}
        taskletgroup = self._getTaskletGroup(doc, macrospace, macro)
        if taskletgroup:
            result2 = taskletgroup.executeV2(
                macro,
                doc=doc,
                tags=tags,
                macro=macro,
                macrostr=macrostr,
                paramsExtra=paramsExtra,
                cmdstr=cmdstr)
            try:
                result, doc = result2
            except:
                taskletPath = taskletgroup.taskletEngines[macro].path
                raise RuntimeError(
                    "Cannot execute macro: %s on doc:%s, tasklet:%s, did not return (result,doc)." %
                    (macrostr, taskletPath, doc))

            if result is not None:
                if not j.data.types.string.check(result):
                    result = "***ERROR***: Could not execute macro %s on %s, did not return content as string (params.result=astring)" % (
                        macro, doc.name)
                doc.content = doc.content.replace(macrostr, result)
        return doc

    def execMacrosOnDoc(self, doc, paramsExtra={}):
        spacename = doc.getSpaceName().lower()

        def macrosorter(entry):
            space = entry[0] or spacename
            return self.priority.get(space, dict()).get(entry[1], 9999)

        macros = self.findMacros(doc)
        while macros:
            for macroitem in macros[:]:
                macrostr, macrospace, macro, tags, cmd = macroitem
                macro = macro.lower().strip()
                # check which macro's are params
                if macro in paramsExtra:
                    doc.content = doc.content.replace(macrostr, paramsExtra[macro])
                    macros.remove(macroitem)
                    continue
                if macro in doc.preprocessor.params:
                    doc.content = doc.content.replace(macrostr, self.params[macro])
                    macros.remove(macroitem)
                    continue
                if macro == "author":
                    doc.content = doc.content.replace(macrostr, ','.join(doc.author))
                    macros.remove(macroitem)
                    continue
                if macro == "docpathshort":
                    doc.content = doc.content.replace(macrostr, doc.shortpath)
                    macros.remove(macroitem)
                    continue
                if macro == "docpath":
                    doc.content = doc.content.replace(macrostr, doc.path)
                    macros.remove(macroitem)
                    continue

            for macroentry in sorted(macros, key=macrosorter):
                doc = self._executeMacroOnDoc(*macroentry, doc=doc)
            macros = self.findMacros(doc)
        return doc


class MacroExecutorPage(MacroExecutorBase):

    def executeMacroAdd2Page(self, macrostr, page, doc=None, requestContext=None, paramsExtra="", markdown=False):
        """
        @param macrostr full string like {{test something more}}
        @param page is htmlpage, rstpage, confluencepage, ...
        find macro's in a page & execute the macro
        a doc is a document in final phase whichere the final result is generated
        """
        if not isinstance(page, Page):
            raise RuntimeError("Page was no page object. Was for macro:%s on doc:%s" % (macrostr, doc.name))

        macrospace, macro, tags, cmdstr = self.parseMacroStr(macrostr)

        # print "execute macro %s on page %s" % (macrostr,page.name)
        # for ease of use add the requestContext params to the main params
        taskletgroup = self._getTaskletGroup(doc, macrospace, macro)

        if taskletgroup:
            if markdown == True:
                from markdown2 import markdown2
                page.body = markdown2.markdown(
                    page.body,
                    extras=[
                        "tables",
                        "nofollow",
                        "cuddled-lists",
                        "markdown-in-html"])
                # markdown format & style fixes
                if '<table>' in page.body:
                    page.body = page.body.replace(
                        '<table>', '<table class="table table-striped table-bordered table-hover">')

            try:
                page = taskletgroup.executeV2(macro, doc=doc, tags=tags, macro=macro, macrostr=macrostr,
                                              paramsExtra=paramsExtra, cmdstr=cmdstr, page=page, requestContext=requestContext)
            except:
                e = traceback.format_exc()
                result = "***ERROR***: Could not execute macro %s on %s, error in macro." % (macro, doc.name)
                if j.application.debug:
                    result += " Error was:\n%s " % (e)
                page.addMessage(j.portal.tools.html.portalhtmlfactory.escape(result))
        else:
            page.addMessage("***error***: could not find macro %s" % macro)

        if not isinstance(page, Page):
            raise RuntimeError(
                "params.page object which came back from macro's does not represent a page. Was for macro:%s on doc:%s" %
                (macro, doc.name))

        page.body = page.body.replace("\{", "{")

        return page

    def executeMacroReturnHTML(self, macrostr, doc=None, requestContext=None, paramsExtra="", pagemirror4jscss=None):
        """
        macrostr is already formatted like {{....}} and only that is returned,
        use executeMacrosInWikiContent instead to process macros in a full text
        """
        page0 = j.portal.tools.server.active.pageprocessor.getpage()
        if pagemirror4jscss is not None:
            page0.pagemirror4jscss = pagemirror4jscss
        page0 = self.executeMacroAdd2Page(macrostr, page0, doc, requestContext, paramsExtra)
        return page0.body

    def execMacrosOnContent(self, content, doc, paramsExtra={}, ctx=None, page=None, markdown=False):

        recursivedepth = 0
        page = j.portal.tools.server.active.pageprocessor.getpage()
        page.body = ""

        def process(content):
            if ctx is not None:
                content = doc.applyParams(ctx.params, findfresh=True, content=content)
            if paramsExtra != {}:
                content = doc.applyParams(paramsExtra, findfresh=True, content=content)
            return content, self.findMacros(doc, content)

        content, macros = process(content)
        while macros:
            recursivedepth += 1
            if recursivedepth > 20:
                content += 'ERROR: recursive error in executing macros'
                return content, doc

            for macroitem in macros:
                macrostr, macrospace, macro, tags, cmdstr = macroitem
                page.body = page.body.replace(macrostr, "", 1)

                if markdown == True:
                    doc.preprocessor.macroexecutorPage.executeMacroAdd2Page(
                        macrostr, page, doc, ctx, paramsExtra, markdown)
                    page.body = page.body.replace('\n', '')
                    from markdown2 import markdown2
                    content = markdown2.markdown(
                        content,
                        extras=[
                            "tables",
                            "nofollow",
                            "cuddled-lists",
                            "markdown-in-html"])
                    # markdown format & style fixes
                    if '<p></p>' in content:
                        content = content.replace('<p></p>', '')
                    if '<table>' in content:
                        content = content.replace(
                            '<table>', '<table class="table table-striped table-bordered table-hover">')

                    content = content.replace(macrostr, page.body, 1)
                    page.body = ""
                else:
                    doc.preprocessor.macroexecutorPage.executeMacroAdd2Page(macrostr, page, doc, ctx, paramsExtra)

            content, macros = process(content)
        content = page.head + content
        return content, doc


class MacroExecutorWiki(MacroExecutorBase):

    def execMacrosOnContent(self, content, doc, paramsExtra={}, ctx=None, page=None):
        recursivedepth = 0

        def process(content):
            if ctx is not None:
                content = doc.applyParams(ctx.params, findfresh=True, content=content)
            if paramsExtra != {}:
                content = doc.applyParams(paramsExtra, findfresh=True, content=content)
            return content, self.findMacros(doc, content)

        content, macros = process(content)
        while macros:
            recursivedepth += 1
            if recursivedepth > 20:
                content += 'ERROR: recursive error in executing macros'
                return content, doc

            for macroitem in macros:
                content, doc = self.executeMacroOnContent(content, macroitem, doc, paramsExtra, ctx=ctx, page=page)

            content, macros = process(content)
        return content, doc

    def executeMacroOnContent(self, content, macroitem, doc, paramsExtra=None, ctx=None, page=None):
        """
        find macro's in a doc & execute the macro
        a doc is a document in preprocessor phase
        """
        macrostr, macrospace, macro, tags, cmdstr = macroitem
        taskletgroup = self._getTaskletGroup(doc, macrospace, macro)
        if taskletgroup:
            try:
                result, doc = taskletgroup.executeV2(groupname=macro, doc=doc, tags=tags, macro=macro, macrostr=macrostr,
                                                     paramsExtra=paramsExtra, cmdstr=cmdstr, requestContext=ctx, content=content, page=page)
            except Exception:
                e = traceback.format_exc()
                if str(e).find("non-sequence") != -1:
                    result = "***ERROR***: Could not execute macro %s on %s, did not return (out,doc)." % (
                        macro, doc.name)
                else:
                    result = "***ERROR***: Could not execute macro %s on %s, error in macro." % (macro, doc.name)
                    if j.application.debug:
                        result += " Error was:\n%s " % (e)
                result = j.portal.tools.html.portalhtmlfactory.escape(result)
            if result == doc:
                # means we did manipulate the doc.content
                doc.content = doc.content.replace(macrostr, "")
                return doc.content, doc

            if result is not None:
                if not j.data.types.string.check(result):
                    result = "***ERROR***: Could not execute macro %s on %s, did not return content as string (params.result=astring)" % (
                        macro, doc.name)
                content = content.replace(macrostr, j.data.text.toStr(result))
        else:
            result = "***ERROR***: Could not execute macro %s on %s, did not find the macro, was a wiki macro." % (
                macro, doc.name)

        content = content.replace(macrostr, j.data.text.toStr(result))

        return content, doc


class MacroexecutorMarkDown(MacroExecutorWiki):

    def execMacrosOnContent(self, content, doc, paramsExtra={}, ctx=None, page=None):
        recursivedepth = 0

        def process(content):
            if ctx is not None:
                content = doc.applyParams(ctx.params, findfresh=True, content=content)
            if paramsExtra != {}:
                content = doc.applyParams(paramsExtra, findfresh=True, content=content)
            return content, self.findMacros(doc, content)

        content, macros = process(content)
        while macros:
            recursivedepth += 1
            if recursivedepth > 20:
                content += 'ERROR: recursive error in executing macros'
                return content, doc

            for macroitem in macros:
                content, doc = self.executeMacroOnContent(content, macroitem, doc, paramsExtra, ctx=ctx, page=page)

            content, macros = process(content)
        return content, doc

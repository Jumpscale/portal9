import re
from js9 import j


class Confluence2RST():

    def processDefs(self, line, doc, page):
        return line
        if not doc.processDefs:
            return line

        # print "processdefs:%s"%line

        def processToken(token):
            if token.find("{") != -1 or token.find("[") != -1 or token.find("]") != -1:
                return token
            # print "tok1:%s"%token
            deff = self.defGet(token)
            if deff is not None:
                # print "founddef"
                token = "[%s|%s]" % (deff.name, deff.pagename)
                # print "tok2:%s"%token
            return token

        token = ""
        lineout = ""
        for char in line:
            if char in [",", ";", ":", " ", ".", "?", "!", "|"]:
                token = processToken(token)
                lineout += "%s%s" % (token, char)
                token = ""
            elif char in ["/", "\\", "]"]:
                lineout += "%s%s" % (token, char)
                token = ""
            else:
                token += char
        lineout += processToken(token)
        lineout = self.findLinks(lineout)
        return lineout

    @staticmethod
    def findLinks(line):
        # r=r"\[[-:|_@#.?\w\s\\=/&]*\]"
        r = r"\[[^\[\]]+\]"  # TODO: does not seem right to me
        if j.tools.code.regex.match(r, line):  # find links
            # print "match %s"% line
            htmlelements = ""
            for match in j.tools.code.regex.yieldRegexMatches(r, line):
                try:
                    # print "link: %s" % match.founditem
                    link_id = link_class = None
                    match2 = match.founditem.replace("[", "").replace("]", "")
                    if match2.find("|") != -1:
                        parts = match2.split("|")
                        descr = parts[0]
                        link = parts[1]
                        if len(parts) >= 3:
                            if parts[2].strip() != "":
                                link_id = (parts[2].split('=')[1]).strip()

                        if len(parts) >= 4:
                            if parts[2].strip() != "":
                                link_id = (parts[2].split('=')[1]).strip()
                                link_class = (parts[3].split('=')[1]).strip()
                        if len(parts) >= 5:
                            htmlelements = parts[4]

                    elif match2.find(":") != -1:
                        descr, link = match2.split(":", 1)[1], match2
                    else:
                        link = match2
                        descr = link
                except Exception as e:
                    return line
                    # if link.find(":") != -1:  # TODO: what was the reason for this, probably have broken something now
                    #     link=link.replace(":","___")
                if link.find(";") != -1:
                    space, pagename = link.split(";", 1)
                    link = "/%s/%s" % (space.lower().strip().strip("/"), pagename.strip().strip("/"))
                # print "match:%s"%match.founditem
                # print "getlink:%s" %page.getLink(descr,link)
                linkDest = "%s <%s>" % (descr, link)
                line = line.replace(match.founditem, linkDest)
        return line

    def processMacro(self, macro, page):

        macro = macro.strip().lstrip("{").strip()
        macro = macro.strip().rstrip("}").strip()

        if macro.find("code:") == 0:
            page.addNewLine()
            macro = macro[5:].strip()
            if macro.startswith('template:'):
                macrolines = macro.splitlines()
                macro = '\n'.join(macrolines[1:])

            page.addCodeBlock(macro)
            page.addNewLine()

        if macro.find("rst:") == 0:
            page.addNewLine()
            macro = macro[4:].strip()
            page.addMessage(macro)

    def convert(self, content, page=None, doc=None, requestContext=None, paramsExtra={}):
        if content.find("@rstignore") != -1:
            return ""

        #styled_text = r'([\w\-:_/= *.\.\/\>\<\\{},|`!]+)'
        styled_text = r'[^{0}\n]*?'

        def limiter(char):
            # Limiters can contain RE special chars, so I escape them here
            limiter_re = ''.join('\\' + c for c in char)

            # This is the RE which is used to replace wiki text formatting with equivalent HTML tag
            return re.compile(r'(\W){0}([^ #{0}]{1}[^ \n{0}]?){0}(\W)'.format(
                limiter_re, styled_text.format(limiter_re)))

        def limiter_replacement(sub):
            # return r'\1<{0}>\2</{0}>\3'.format(sub)
            return r'\1{0}\2{0}\3'.format(sub)

        def substitute_email(match):
            return r'<a href="{0}">{1}</a>'.format(match.group(1), match.group(1).replace('mailto:', '', 1))

        def escape_char(char):
            return char
            # return '&#{0};'.format(ord(char.group(1)))

        substitutions = [
            (r'\\([^\n\r\\])', ""),
            # ('<',           '&lt;'),
            # ('>',           '&gt;'),
            (r'\@LF\b', '\n'),  # This should come after !=
            (r'&[\w #]*;', ""),
            (limiter('`'), limiter_replacement('\'')),
            # (limiter('**'),  limiter_replacement('**')),
            # (limiter('*'),  limiter_replacement('**')),
            (limiter('_'), limiter_replacement('*')),
            (limiter('+'), limiter_replacement('')),
            (limiter('-'), limiter_replacement('')),
            (limiter('??'), limiter_replacement('')),
            (limiter('^'), limiter_replacement('')),
            (limiter('~'), limiter_replacement('')),


            # {color: red}text goes here{color}
            (re.compile(r'\{{color\:(.*?)\}}({0})\{{color\}}'.format(styled_text.format('{}')),
                        flags=re.DOTALL | re.MULTILINE | re.IGNORECASE),
             r'<span style="color:\1">\2</span>'),

            # Links & emails
            #(r'\[(.*?)\]', substitute_email),

            # blockquote
            (r'bq\.\s+(.*?)\n', r'<blockquote>\1</blockquote>\n'),

            # Escape characters by putting \ in front of it, e.g. \*
        ]
        # First, divide the text into macros & non-macros
        blocks = re.split(r'({{.*?}})', content, flags=re.DOTALL)
        for i in range(len(blocks)):
            if blocks[i].startswith('{{'):  # a macro
                continue

            for tag_re, sub_re in substitutions:
                blocks[i] = re.sub(tag_re, sub_re, blocks[i])

        content = ''.join(blocks)

        if page is None:
            page = j.portal.tools.docgenerator.pageNewMD("temp")

        # images=j.sal.fs.listFilesInDir(dirpath,False)
        # images3=[]L
        # for image in images:
            # image2=image.lower()
            # if image2.find(".jpg") != -1 or image2.find(".png") != -1:
            # image2=image2.strip()
            # image2=j.sal.fs.getBaseName(image2.replace("\\","/"))
            # images3.append(image2)

        state = "start"
        macro = ""
        params = ""

        ulAttributes = ''
        for line in content.split("\n"):
            # print line
            # print "IN:%s"%line
            self._lastLine = line
            if state not in ['macro']:
                line = line.strip()

            # \\ on their own line will emit <br>
            if line == r'\\':
                page.addNewLine()
                line = ''
                continue

            if line.strip() == "" and state == "start":
                page.addNewLine()
                line = ''
                continue

            # print "#: %s %s" % (state,line)

            # END TABLE
            if state == "table" and (line[0:1] == "||" or line.find("|") != 0):
                state = "start"
                if params != "":
                    page.addList(trows, theader, classparams=params)
                else:
                    page.addList(trows, theader)
                params = ""

            # PAGEBREAK
            if state == "start" and (line.find("&nbsp;") != -1):  # or line=="":
                page.addNewLine()
                continue

            if state != "macro" and line == "":
                page._checkBlock('', '', '')
                continue

            # SKIP LINES
            if state != "macro" and line[0] == "#":
                continue

            # IMAGE
            regex = r"\![\w\-:_/=*.,|?&][\w\-:_/= *.,|?&]*[\w\-:_/=*.,|?&]\!"
            if (state == "start" or state == "table")and j.tools.code.regex.match(regex, line):
                matches = j.tools.code.regex.findAll(regex, line)
                for match in matches:
                    image = match.replace("!", "")
                    if '|' in image:
                        # Image may have attributes, like
                        #   !image.png|border=1px solid black, margin=1px!
                        # these should be written as CSS properties. The syntax for the macro should follow CSS format
                        #
                        # Result: <img src="image.png" style="border: 1px solid black; margin: 1px" />
                        image, styles = image.split('|', 1)
                        styles = [attr.split('=') for attr in styles.split(',')]
                    else:
                        styles = []
                    if image.startswith('/') or image.startswith('http://'):
                        imagePath = image
                    else:
                        # imagePath = "/images/%s/%s" % (doc.getSpaceName(), image)
                        imagePath = "/images/%s/%s" % ("unknownspace", image)

                    # th=j.data.tags.getObject(tags)
                    # result=th.getValues(width=800,height=600,border=True)
                    #page.addImage(image, image, result["width"], result["height"])
                    #page.addImage(image, imagePath, styles=styles)
                    # line = line.replace(match, self.createImage(image, imagePath, styles=styles))
                    page.addMessage("unsupported image:%s" % imagePath)
                    continue

            if line.find("{center}") > -1:
                continue

            if line.startswith("{toc:"):
                # line="{{toc}}"
                line = ""
                continue

            # 1 line macros
            if (state == "start" or state == "table") and line.find("{{") != -1 and line.find("}}") != -1:
                continue  # not supported for now
                # self.processMacro()
             #    macros = doc.preprocessor.macroexecutorPage.getMacroCandidates(line)
             #    for macro in macros:
             #      raise RuntimeError("macro in table not supported")
             #        # print "## 1linemacro:%s"%macro

             #        # mtayseer: this condition looks wrong!!
             #        if line.find("{{") != 0 or len(macros) > 1:

             #            htmlMacro = doc.preprocessor.macroexecutorPage.executeMacroReturnHTML(macro,
             #                                                                                  doc=doc, requestContext=requestContext, paramsExtra=paramsExtra, pagemirror4jscss=page)
             #            line = line.replace(macro, htmlMacro)
             #        else:
             #            doc.preprocessor.macroexecutorPage.executeMacroAdd2Page(macro, page, doc=doc,
             #                                                                    requestContext=requestContext, paramsExtra=paramsExtra)
             #            line = ""
             #    macro = ""
             #    # print "processed 1 macro line:%s"%line
             #    if line.strip() == "":
             #        continue

            # print "after1linemacrostate:%s %s"%(line,state)

            if state == "start" and line.find("{{") != -1:
                state = "macro"

            if state == "macro":
                macro += "%s\n" % line

            if state == "macro" and line.find("}}") >= 0:
                state = "start"
                # print "macroend:%s"%line
                # macrostr=macro

                # if doc != None:
                #     doc.preprocessor.macroexecutorPage.executeMacroAdd2Page(macro, page, doc=doc, requestContext=requestContext, paramsExtra=paramsExtra)
                #     macro = ""
                #     # params=""
                #     continue
                self.processMacro(macro, page)
                macro = ""
                continue

            if line.strip() == "":
                continue

            # print "linkcheck: %s" % j.tools.code.regex.match("\[[-\\:|_\w\s/]*\]",line)
            # FIND LINKS
            line = self.findLinks(line)

            # HEADING
            header = j.tools.code.regex.getRegexMatch("^h(\d)\. (.+?)$", line)
            if header and state == "start":
                level, line = header.foundSubitems
                level = int(level)
                # line = self.processDefs(line, doc, page)
                page.addHeading(line, level)
                continue

            unorderedItem = j.tools.code.regex.getRegexMatch("^(\*+) (.+?)$", line)
            if state == "start" and unorderedItem:
                stars, line = unorderedItem.foundSubitems
                level = len(stars)
                # line = self.processDefs(line, doc, page)
                page.addBullet(line, level)
                ulAttributes = ''  # ulAttributes is set in the previous iteration of the for-loop. It should be reset _after_ the list is added
                continue

            numberedItem = j.tools.code.regex.getRegexMatch("^\*(#+) (.+?)$", line)
            if state == "start" and numberedItem:
                hashes, line = numberedItem.foundSubitems
                level = len(hashes)
                # line = self.processDefs(line, doc, page)
                page.addBullet(line, level)
                ulAttributes = ''
                continue

            # Read styles for lists
            # The syntax will be like this
            #
            #   *- id=main-menu | class=nav nav-list
            #   * item 1
            #   * item 2
            ulAttributes = j.tools.code.regex.getRegexMatch("^(\*+)- (.+?)$", line)
            if ulAttributes:
                continue
            else:
                ulAttributes = ''

            if state == "start" and j.tools.code.regex.match(".*\|\|.*", line) and len(line.split("||")) == 2:
                # DESCRIPTIONS
                p1, p2 = line.split("||")
                # p2 = self.processDefs(line, doc, page)
                page.addDescr(p1, p2)
                continue

            if state == "start" and (line.find("@divend") == 0 or line.find("@rowend") ==
                                     0 or line.find("@colend") == 0 or line.find("@blockend") == 0):
                # page.addMessage("</div>")
                continue

            if state == "start" and line.find("@block") == 0:
                # divlower(divauto,page,"block")
                arg = line.replace("@block", "").strip()
                # if arg == "":
                #     arg = "container"
                # page.addMessage("<div class=\"%s\">" % arg)
                # page.divlevel.append("block")
                continue

            if state == "start" and line.find("@row") == 0:
                # divlower(divauto,page,"row")
                arg = line.replace("@row", "").strip()
                # if arg == "":
                #     arg = "row-fluid"
                # page.addMessage("<div class=\"%s\">" % arg)
                # page.divlevel.append("row")
                continue

            if state == "start" and line.find("@col") == 0:
                # divlower(divauto,page,"col")
                line = line.replace("@col", "").strip()
                # arg= line.replace("@col", "").strip()
                # page.addMessage("<div class=\"span%s\">" % arg)
                # page.divlevel.append("col")
                continue

            if state == "start" and line.find("@block") == 0:
                line = line.replace("@block", "").strip()
                # arg = line.replace("@block", "").strip()
                # if arg == "":
                #     arg = "container-fluid"
                # page.addMessage("<div class=\"%s\">" % arg)
                # page.divlevel += 1
                continue

            # check params
            if state == "start" and line.find("@params") == 0:
                params = line.replace("@params", "").strip()
                #from JumpScale.core.Shell import ipshell
                # print "DEBUG NOW params, not implemented"
                # ipshell()

            if state == "start" and line.find("||") == 0:
                # beginning of table
                line = self.processDefs(line, doc, page)
                state = "table"
                cols = line.split("||")
                cols = cols[1:-1]
                theader = cols
                trows = []
                continue

            if state == "start" and line.find("|") == 0:
                # beginning of table
                line = self.processDefs(line, doc, page)
                state = "table"
                theader = ""
                trows = []

            if state == "table" and line.find("|") == 0:
                # ADD ROW TO TABLE
                line = self.processDefs(line, doc, page)
                cols = line.split("|")
                trows.append(cols[1:-1])

            # was a regular line so add
            if state != "macro" and state != "table" and line != "":
                if line[0] != "@":
                    line = self.processDefs(line, doc, page)
                    page.addMessage(line)

        if page.body != "":
            # work on the special includes with [[]]
            includes = j.tools.code.regex.findAll("\[\[[\w :;,\.\*\!\?\^\=\'\-/]*\]\]", page.body)
            for item in includes:
                item2 = item.replace("[[", "").replace("]]", "")
                if doc.preprocessor.docExists(item2):
                    doc2 = doc.preprocessor.docGet(item2)
                else:
                    page.body = page.body.replace(
                        item, " ***error*** : COULD NOT FIND DOC %s, could not include." %
                        item2)
                    continue
                page2 = j.portal.tools.docgenerator.pageNewMD("includeInConfluence2Wiki")
                # page2.liblocation = page.liblocation
                page2 = self.convert(doc2.content, page2, doc2)

                page.body = page.body.replace(item, page2.body)

        return page


from js9 import j
from Page import Page
import copy


class PageRST(Page):

    """
    """

    def __init__(self, name, content=""):
        """

        """
        Page.__init__(self, name, content)
        self.body = ""
        self.projectname = ""
        self.logo = ""
        self.login = False
        self.divlevel = []
        self._inBlockType = ""
        self._inBlockClosingStatement = ""
        self._bulletslevel = 0
        self._codeblockid = 0
        self.hasfindmenu = False
        self.padding = True
        self.processparameters = {}
        self.bodyattributes = []

        self.documentReadyFunctions = []

    def addMessage(self, message, blockcheck=False):

        if not self._inBlockType == "paragraph":
            self.addNewLine()
            self._inBlockType = "paragraph"

        message = str(message)
        message = message.strip()
        if message != '':
            message += "\n"
        return self._addMessage(message, blockcheck)

    def _addMessage(self, message, blockcheck=False):
        # if blockcheck:
        #     # print "blockcheck %s" % message
        #     self._checkBlock("", "", "")
        # else:
            # print "no blockcheck %s" % message
        message = str(message)
        message = message.replace("text:u", "")
        message.strip("'")
        message = message.replace("\r", "")

        if message != "":
            self.body = "%s%s" % (self.body, message)
        # print "OUT:%s"%message

    def addParagraph(self, message):
        if not self._inBlockType == "paragraph":
            self.addNewLine()
            self._inBlockType = "paragraph"

        message = message.strip()
        message += "\n\n"
        self.addMessage(message)

    def addBullet(self, message, level=1):

        if not self._inBlockType == "bullet":
            self.addNewLine()
            self._bulletslevel = level
            self._inBlockType = "bullet"

        if level < 1:
            raise RuntimeError("level needs to be between 1 and 6")

        prefix = ""
        for i in range(level - 1):
            prefix += "  "

        if level != self._bulletslevel:
            self.addNewLine()

        out = ""

        first = True
        for line in message.split("\n"):
            line = line.strip()
            if first:
                out += "%s* %s\n" % (prefix, line)
            else:
                out += "  %s\n" % (prefix, line)

        self._addMessage(out, blockcheck=False)

        self._bulletslevel = level

    def _checkBlock(self, ttype, open, close):
        """
        types are : bullet,descr
        """
        return
        # print "checkblock inblock:%s ttype:%s intype:%s" %(self._inBlock,ttype,self._inBlockType)
        if self._inBlock:
            if self._inBlockType != ttype:
                if self._inBlockType in ("bullet", "number"):
                    for i in range(self._bulletslevel):
                        self.addMessage(self._inBlockClosingStatement, blockcheck=False)
                    self._bulletslevel = 0
                else:
                    self.addMessage(self._inBlockClosingStatement, blockcheck=False)
                if open != "":
                    self.addMessage(open, blockcheck=False)
                    self._inBlock = True
                    self._inBlockType = ttype
                    self._inBlockClosingStatement = close
                else:
                    self._inBlock = False
                    self._inBlockType = ""
                    self._inBlockClosingStatement = ""
        else:
            self.addMessage(open, blockcheck=False)
            if ttype != "" and close != "":
                self._inBlock = True
                self._inBlockType = ttype
                self._inBlockClosingStatement = close
        # print "checkblock END: inblock:%s ttype:%s intype:%s" %(self._inBlock,ttype,self._inBlockType)

    def addDescr(self, name, descr):
        self.addMessage("|%s|%s|" % (name, descr))

    def addBullets(self, messages, level=1):
        """
        messages: list of bullets
        """
        for message in messages:
            self.addBullet(message, level)

    def addNewLine(self, nrlines=1):
        for line in range(nrlines):
            self._addMessage("\n")

    def addHeading(self, message, level=1):
        if not self._inBlockType == "heading":
            self.addNewLine()
            self._inBlockType = "heading"

        if message.find("\n") != -1:
            raise RuntimeError("cannot have enter in heading")

        message = str(message)
        if message != '':
            if message[-1] != "\n":
                message += "\n"

        order = "#*=-^\""
        char = order[level - 1]
        line = ""
        for i in range(0, len(message) - 1):
            line += char
        message = "%s%s\n" % (message, line)
        self._addMessage(message)

    def addList(self, rows, headers="", showcolumns=[], columnAliases={},
                classparams="table-condensed table-hover", linkcolumns=[]):
        """
        @param rows [[col1,col2, ...]]  (array of array of column values)
        @param headers [header1, header2, ...]
        @param linkcolumns has pos (starting 0) of columns which should be formatted as links  (in that column format needs to be $description__$link
        """
        self.addMessage("WARNING: UNSUPPORTED DOC, TABLES NOT SUPPORT YET.")
        if not self._inBlockType == "list":
            self.addNewLine()
            self._inBlockType = "list"
        return
        # from IPython import embed
        # print "DEBUG NOW addlist (pagerst)"
        # embed()

        if rows == [[]]:
            return
        if len(rows) == 0:
            return False
        l = len(rows[0])
        if str(headers) != "" and headers is not None:
            if l != len(headers):
                headers = [""] + headers
            if l != len(headers):
                #raise RuntimeError("Cannot process headers, wrong nr of cols")
                print("Cannot process headers, wrong nr of cols")
                self.addMessage("ERROR header wrong nr of cols:%s" % headers)
                headers = []

        c = ""
        if headers != "":
            c += "<thead><tr>\n"
            for item in headers:
                if item == "":
                    item = " "
                c = "%s<th>%s</th>\n" % (c, item)
            c += "</tr></thead>\n"
        rows3 = copy.deepcopy(rows)
        c += "<tbody>\n"
        for row in rows3:
            c += "<tr>\n"
            if row and row[0] in columnAliases:
                row[0] = columnAliases[row[0]]
            colnr = 0
            for col in row:
                if col == "":
                    col = " "
                if colnr in linkcolumns:
                    if len(col.split("__")) != 2:
                        raise RuntimeError(
                            "column which represents a link needs to be of format $descr__$link, here was:%s" %
                            col)
                    c += "<td>%s</td>\n" % self.getLink(col.split("__")[0], col.split("__")[1])
                else:
                    c += "<td>%s</td>\n" % self.getRound(col)
                colnr += 1
            c += "</tr>\n"
        c += "</tbody></table>\n\n"
        self.addMessage(c, True, isElement=True)

    def addDict(self, dictobject, description="", keystoshow=[], aliases={}, roundingDigits=None):
        """
        @params aliases is dict with mapping between name in dict and name to use
        """
        # from IPython import embed
        # print "DEBUG NOW addDict (pagerst)"
        # embed()
        if keystoshow == []:
            keystoshow = list(dictobject.keys())
        self.addMessage(description)
        arr = []
        for item in keystoshow:
            if item in aliases:
                name = aliases[item]
            else:
                name = item
            arr.append([name, dictobject[item]])
        self.addList(arr)
        self.addNewLine()

    def addLink(self, description, link):
        self._addMessage("%s <%s>" % (description, link))

    def addPageBreak(self,):
        self.addNewLine(2)

    def addActionBox(self, actions):
        """
        @actions is array of array, [[$actionname1,$params1],[$actionname2,$params2]]
        """
        pass

    def addCodeBlock(self, code, template="python", path="", edit=True, exitpage=True, spacename='', pagename='', linenr=False,
                     linecolor="#eee", linecolortopbottom="1px solid black", wrap=True, wrapwidth=100):
        """
        """
        # out="::\n"
        if not self._inBlockType == "code":
            self.addNewLine()
            self._inBlockType = "code"

        out = ".. code-block:: python\n\n"
        for line in code.split("\n"):
            out += "  %s\n" % line
        self.addMessage(out)

    def addCodePythonBlock(self, code, title="", removeLeadingTab=True):
        # todo
        if not self._inBlockType == "code":
            self.addNewLine()
            self._inBlockType = "code"

        if removeLeadingTab:
            check = True
            for line in code.split("\n"):
                if not(line.find("    ") == 0 or line.strip() == ""):
                    check = False
            if check == True:
                code2 = code
                code = ""
                for line in code2.split("\n"):
                    code += "%s\n" % line[4:]
        self.addCodeBlock(code)

    def addImage(self, title, imagePath, width=None, height=None, styles=[]):
        """
        @param title alt text of the image
        @param imagePath can be url or local path
        @param width width of the image
        @param height height of the image
        @param styles a list of tuples, containing CSS attributes for the image, e.g. [("background-color", "green), ("border", "1px solid green")]
        """
        # from IPython import embed
        # print "DEBUG NOW add image page2rst"
        # embed()

        width_n_height = ''
        if width:
            width_n_height += ' width="{0}"'.format(width)
        if height:
            width_n_height += ' height="{0}"'.format(height)

        img = "<img src='%s' alt='%s' %s style='clear:both;%s' />" % (
            imagePath, title, width_n_height, PageHTML._format_styles(styles))
        self.addMessage(img, isElement=True)

    def addTableWithContent(self, columnsWidth, colContents):
        """
        @param columnsWidth = Array with each element a nr, when None then HTML does the formatting, otherwise relative to each other
        @param colContents = array with each element HTML code
        """
        # from IPython import embed
        # print "DEBUG NOW addTableWithContent (page2rst)"
        # embed()

        table = "<table><thead><tr>"
        for colWidth, colContent in zip(columnsWidth, colContents):
            if colWidth:
                table += "<th width='%s'>%s</th>" % (colWidth, colContent)
            else:
                table += "<th>%s</th>" % (colContent)
        table += "</tr></head></table>"
        self.addMessage(table, isElement=True)


# all not relevant

    def addLineChart(self, title, rows, headers="", width=800, height=400):
        """
        @param rows [[values, ...],]  first value of the row is the rowname e.g. cost, revenue
        @param headers [] first value is name of the different rowtypes e.g. P&L
        """
        raise RuntimeError("cannot be implemented")

    def addBarChart(self, title, rows, headers="", width=900, height=400,
                    showcolumns=[], columnAliases={}, onclickfunction=''):
        """
        """
        raise RuntimeError("cannot be implemented")

    def addPieChart(self, title, data, legend, width=1000, height=600):
        """
        """
        raise RuntimeError("cannot be implemented")

    def addHTML(self, htmlcode):
        raise RuntimeError("cannot be implemented")
        #import cgi
        #html = "<pre>%s</pre>" % cgi.escape(htmlcode)
        self.addMessage(htmlcode, isElement=False)

    def removeCSS(self, exclude, permanent=False):
        """
        """
        pass

    def addCSS(self, cssLink=None, cssContent=None, exlcude=""):
        """
        """
        pass

    def addJS(self, jsLink=None, jsContent=None, header=True):
        pass

    def addScriptBodyJS(self, jsContent):
        pass

    def addBootstrap(self, jquery=True):
        pass

    def addBodyAttribute(self, attribute):
        pass

    def addHostBasedContent(self):
        pass

    def addDocumentReadyJSfunction(self, function):
        pass

    def addExplorer(self, path="", dockey=None, height=500, width=750, readonly=False, tree=False):
        raise RuntimeError("cannot be implemented")

    def addHTMLHeader(self, header):
        pass

    def addHTMLBody(self, body):
        self.addMessage(body)

    def getContent(self):
        return str(self)

    def __str__(self):
        # make sure we get closures where needed (/div)
        self._checkBlock("DDD", "", "")
        return self.body

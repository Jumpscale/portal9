
from js9 import j
from .Page import Page
import copy
import inspect
import jinja2


class PageHTML(Page):

    """
    the methods add code to the self.body part !!!!!
    """

    def __init__(self, name, content="", htmllibPath=None, online=False, stylesheet=None):
        """
        @param stylesheet if 'local' will get stylesheet from disk, otherwise can specify other stylesheet
        """
        Page.__init__(self, name, content)

        #self.title = "<title>%s</title>\n" % name
        self.title = ""
        self.jenv = jinja2.Environment(variable_start_string="${", variable_end_string="}")
        self.head = ""
        self.tail = []
        self.libs = ""
        #self.body = "<div class='heading'><h1>%s</h1></div>\n" % name
        self.body = ""
        self._timestampsAdded = set()
        self.projectname = ""
        self.logo = ""
        self.favicon = ""
        self.scriptBody = ""
        self.jscsslinks = {}
        self.login = False
        self.divlevel = []
        self._inBlock = False
        self._inBlockType = ""
        self._inBlockClosingStatement = ""
        self._bulletslevel = 0
        self._codeblockid = 0
        self._hasmenu = False
        self._hostbasedmacro = False
        self.hasfindmenu = False
        self.padding = True
        self.pagemirror4jscss = None
        self.processparameters = {}
        self.bodyattributes = []

        if htmllibPath is not None:
            self.liblocation = htmllibPath
        else:
            if online:
                self.liblocation = "https://bitbucket.org/incubaid/jumpscale-core-6.0/raw/default/extensions/core/docgenerator/htmllib"
            else:
                extpath = inspect.getfile(self.__init__)
                extpath = j.sal.fs.getDirName(extpath)
                self.liblocation = j.sal.fs.joinPaths(extpath, "htmllib")

        self._hasCharts = False
        self._hasCodeblock = False
        self._hasSidebar = False
        self.functionsAdded = {}
        self._explorerInstance = 0
        self._lineId = 0
        self.documentReadyFunctions = []

        chartTemplatePath = j.sal.fs.joinPaths(j.sal.fs.getDirName(__file__), "templates", "chart.js")
        self._chartTemplateContent = j.sal.fs.fileGetContents(chartTemplatePath)
        self._chartId = 44

        pieTemplatePath = j.sal.fs.joinPaths(j.sal.fs.getDirName(__file__), "templates", "pie.js")
        self._pieTemplateContent = j.sal.fs.fileGetContents(pieTemplatePath)
        self._pieId = 100

        #lineTemplatePath = j.sal.fs.joinPaths(j.sal.fs.getDirName(__file__),"templates", "line.js")
        #self._lineTemplateContent = j.sal.fs.fileGetContents(lineTemplatePath)
        #self._lineId = 150

        if stylesheet == "local":
            stylesheet = j.sal.fs.joinPaths(j.sal.fs.getDirName(__file__), "style.css")
            if j.sal.fs.exists(stylesheet):
                css = j.sal.fs.fileGetContents(stylesheet)
                self.addCSS("", css)

    def addMessage(self, message, newline=False, isElement=True, blockcheck=True):
        if blockcheck:
            # print "blockcheck %s" % message
            self._checkBlock("", "", "")
        # else:
            # print "no blockcheck %s" % message
        message = str(message)
        message = message.replace("text:u", "")
        message.strip("'")
        message = message.strip()
        message = message.replace("\r", "")
        if message != '' and isElement:
            message = "%s" % message
        elif newline and message != '':
            message = "<p>%s</p><br/>" % message
        elif newline and message == '':
            message = '<br/>'
        elif message == "":
            pass
        else:
            message = "<p>%s</p>" % message

        message = message.replace("&lt;br&gt;", "<br />")

        if message != "":
            self.body = "%s%s\n" % (self.body, message)

    def addParagraph(self, message):
        self.addMessage(message, isElement=False)

    def addFavicon(self, href, type):
        self.favicon = '<link rel="shortcut icon" type="%s" href="%s" />' % (type, href)

    def addBullet(self, message, level=1, bullet_type='bullet', tag='ul', attributes=''):
        self._checkBlock(bullet_type, "", "</{0}>".format(tag))
        if level > self._bulletslevel:
            for i in range(level - self._bulletslevel):
                self.addMessage("<{0} {1}>".format(tag, attributes), blockcheck=False)
            self._bulletslevel = level
        if level < self._bulletslevel:
            for i in range(self._bulletslevel - level):
                self.addMessage("</{0}>".format(tag), blockcheck=False)
            self._bulletslevel = level
        self.addMessage("<li>%s</li>" % message, blockcheck=False)

    def _checkBlock(self, ttype, open, close):
        """
        types are : bullet,descr
        """
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
        self._checkBlock("descr", "<dl class=\"dl-horizontal\">", "</dl>")
        self.addMessage("<dt>%s</dt>\n<dd>%s</dd>" % (name, descr), blockcheck=False)

    def addBullets(self, messages, level=1):
        """
        messages: list of bullets
        """

        # todo: figure a way for nested bullets!!
        bullets = '<ul>'
        for message in messages:
            bullets += '<li>%s</li>' % message
        bullets += '</ul>'
        self.addMessage(bullets, blockcheck=False)

    def addNewLine(self, nrlines=1):
        for line in range(nrlines):
            self.addMessage("", True, isElement=True)

    def addHeading(self, message, level=1):
        message = str(message)

        heading = "<h%s class=\"title\">%s</h%s>" % (level, message, level)
        self.addMessage(heading, isElement=True)

    def addList(self, rows, headers="", showcolumns=[], columnAliases={}, classparams="table-condensed table-hover", linkcolumns=[]):
        """
        @param rows [[col1,col2, ...]]  (array of array of column values)
        @param headers [header1, header2, ...]
        @param linkcolumns has pos (starting 0) of columns which should be formatted as links  (in that column format needs to be $description__$link
        """
        if rows == [[]]:
            return
        if "datatables" in self.functionsAdded:
            classparams += 'cellpadding="0" cellspacing="0" border="0" class="table table-striped table-bordered display dataTable'
            if headers:
                classparams += ' JSdataTable'
        if len(rows) == 0:
            return False
        l = len(rows[0])
        if str(headers) != "" and headers is not None:
            if l != len(headers):
                headers = [""] + headers
            if l != len(headers):
                print("Cannot process headers, wrong nr of cols")
                self.addMessage("ERROR header wrong nr of cols:%s" % headers)
                headers = []

        c = "<table  class='table %s'>\n" % classparams  # the content
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

    @staticmethod
    def getLink(description, link, link_id=None, link_class=None, htmlelements="", newtab=False):
        if link_id:
            link_id = ' id="%s"' % link_id.strip()
        else:
            link_id = ''

        if link_class:
            link_class = ' class="%s"' % link_class.strip()
        else:
            link_class = ''

        if newtab:
            target = 'target="_blank"'
        else:
            target = ''

        anchor = "<a href='%s' %s %s %s %s>%s</a>" % (link.strip(),
                                                      link_id.strip(),
                                                      link_class,
                                                      htmlelements,
                                                      target,
                                                      description)
        return anchor

    def addLink(self, description, link, newtab=False):
        anchor = self.getLink(description, link, newtab=newtab)
        self.addParagraph(anchor)

    def addPageBreak(self,):
        self.addMessage("<hr style='page-break-after: always;'/>")

    def addComboBox(self, items):
        """
        @items is a list of tuples [ ('text to show', 'value'), ]
        """
        import random
        if items:
            id = ('dropdown%s' % random.random()).replace('.', '')
            html = '<select id=%s>\n' % (id)

            for text, value in items:
                html += '<option value="%s">%s</option>\n' % (value, text)
            html += '</select>'
            self.addHTML(html)
            return id
        else:
            return ''

    def addBootstrapCombo(self, title, items, id=None):
        self.addBootstrap()
        html = """
<div class="btn-group" ${id}>
  <button type="button" class="btn btn-default dropdown-toggle" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
      ${title}<span class="caret"></span>
  </button>
  <ul class="dropdown-menu">
    {% for name, action in items %}
    <li><a href="javascript:void(0)" onclick="${action}">${name}</a></li>
    {% endfor %}
  </ul>
</div>
"""
        id = 'id="%s"' % id if id else ''
        html = self.jenv.from_string(html).render(items=items, title=title, id=id)
        self.addHTML(html)

    def addActionBox(self, actions):
        """
        @actions is array of array, [[$actionname1,$params1],[$actionname2,$params2]]
        """
        row = []
        for item in actions:
            action = item[0]
            actiondescr = item[1]
            if actiondescr == "":
                actiondescr = action
            params = item[2]

            if action in self.actions:
                link = self.actions[action]
                link = link.replace("{params}", params)
                row.append(self.getLink(actiondescr, link))
            else:
                raise RuntimeError("Could not find action %s" % action)
        self.addList([row])

    def addCodeBlock(self, code, template="python", path="", edit=True, exitpage=True, spacename='', pagename='', linenr=False,
                     linecolor="#eee", linecolortopbottom="1px solid black", wrap=True, wrapwidth=100, querystr=None, theme='monokai', autorefresh=False, beforesave=None):
        """
        TODO: define types of templates supported
        @template e.g. python
        if path is given and edit=True then file can be editted and a edit button will appear on editor
        """
        # if codeblock no postprocessing(e.g replacing $$space, ...) should be
        # done

        if edit:
            self.processparameters['postprocess'] = False
        self.addJS("%s/old/codemirror/lib/codemirror.js" % self.liblocation)
        self.addCSS("%s/old/codemirror/lib/codemirror.css" % self.liblocation)
        self.addJS("%s/old/codemirror/mode/javascript/javascript.js" % self.liblocation)
        self.addCSS("%s/old/codemirror/theme/%s.css" % (self.liblocation, theme))
        #self.addCSS("%s/codemirror/doc/docs.css"% self.liblocation)
        self.addJS("%s/old/codemirror/mode/%s/%s.js" % (self.liblocation, template, template))
        CSS = """
<style type="text/css">
    .CodeMirror {
        height: auto;
        border: $linecolor;
        border-top: $linecolortopbottom;
        border-bottom: $linecolortopbottom
    }
    .CodeMirror-scroll {
        overflow-y: hidden;
        overflow-x: auto;
    }

</style>
"""
        CSS = CSS.replace("$linecolortopbottom", linecolortopbottom)
        CSS = CSS.replace("$linecolor", linecolor)

        self.head += CSS
        self._codeblockid += 1
        # rows=\"20\"
        TA = "<textarea id=\"code%s\" name=\"code%s\">" % (self._codeblockid, self._codeblockid)
        TA += code
        TA += "</textarea>"
        if path != "" and edit:
            TA += "<button class='btn btn-primary margin-top-large' type=\"submit\" onclick=\"copyText%s();\">Save.</button>" % self._codeblockid
        self.addMessage(TA)

        if path != "" and edit:

            F = """
    <form id="hiddenForm$id" name="hiddenForm$id" method="post" action="/restmachine/system/contentmanager/wikisave">
    <input type="hidden" name="text" id="text" value="">
    <input type="hidden" name="cachekey" id="cachekey" value="$guid">
    </form>
            """
            F = F.replace("$id", str(self._codeblockid))
            guid = j.data.idgenerator.generateGUID()
            content = {'space': spacename, 'path': path, 'page': pagename, 'querystr': querystr}
            j.apps.system.contentmanager.dbmem.set(guid, content, 60)
            F = F.replace("$guid", guid)
            self.addMessage(F)

        # if not self._hasCodeblock:
        if linenr:
            linenr = "true"
        else:
            linenr = "false"
        JS = """
var editor$id = CodeMirror.fromTextArea(document.getElementById("code$id"),
    {
    lineNumbers: $linenr,
    theme: "elegant",
    readOnly: $readonly,
    theme: "$theme",
    autoRefresh: "$autorefresh",
    lineWrapping: $wrap,
    mode: "{template}",
    onCursorActivity: function() {
        editor$id.addLineClass(hlLine, null, null);
        hlLine = editor$id.addLineClass(editor$id.getCursor().line, null, "activeline");
        }
    }
);
var hlLine = editor$id.addLineClass(0, "activeline");

function copyText$id() {
    var text=editor$id.getValue()
    document.hiddenForm$id.text.value = text;
    document.forms["hiddenForm$id"].submit();
    }
"""

        JS = JS.replace("$id", str(self._codeblockid))
        JS = JS.replace("$linenr", linenr)
        JS = JS.replace("$wrap", str(wrap).lower())
        JS = JS.replace("$readonly", str(not edit).lower())
        JS = JS.replace("$theme", theme)
        JS = JS.replace("$autorefresh", str(autorefresh).lower())

        self.addJS(jsContent=JS.replace("{template}", template), header=False)
        self._hasCodeblock = True

    def addCodePythonBlock(self, code, title="", removeLeadingTab=True):
        # todo
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

    def addLineChart(self, title, rows, headers="", width=800, height=400):
        """
        @param rows [[values, ...],]  first value of the row is the rowname e.g. cost, revenue
        @param headers [] first value is name of the different rowtypes e.g. P&L
        """

        legend = list()

        headers2 = []
        prev = ""
        for item in headers:
            if item != prev:
                headers2.append(item)
                prev = item
            else:
                headers2.append("")

        if len(rows) == 0:
            return False
        data = ""
        for row in rows:
            data += str(row[1:]) + ","
            legend.append(row[0])

        data = data[:-1]

        self._addChartJS()
        self._lineId += 1
        lineId = 'line-%s' % (self._lineId)

        if headers == "":
            headers = []

        te = j.tools.code.template_engine_get()
        te.add('lineId', lineId)
        te.add('lineTitle', title)
        te.add('lineData', data)
        te.add('lineHeaders', str(headers2))
        te.add('lineLegend', str(legend))
        te.add('lineWidth', str(width))
        te.add('lineHeight', str(height))

        C = """
    var line = new RGraph.Line("{lineId}", {lineData});

    line.Set('chart.title', '{lineTitle}');
    line.Set('chart.linewidth', 1);
    line.Set('chart.labels', {lineHeaders});
    line.Set('chart.key', {lineLegend});
    line.Set('chart.gutter.left', 90);
    RGraph.Effects.Line.jQuery.Trace(line);

    line.Draw();
        """

        jsContent = te.replace(C)
        lineContainer = "<canvas id='%s' width='%s' height='%s' >[No Canvas Support!]</canvas>" % (
            lineId, width, height)
        self.addMessage(lineContainer, isElement=True, newline=True)

        self.addJS(jsContent=jsContent, header=False)

    def addBarChart(self, title, rows, headers="", width=900, height=400,
                    showcolumns=[], columnAliases={}, onclickfunction=''):
        """
        order is list of items in rows & headers, defines the order and which columns to show
        """
        data = list()
        legend = list()
        newRows = []
        for row in rows:
            if len(row) < 2:
                continue
            newRow = [row[0]] + [int(n) for n in row[1:]]
            newRows.append(newRow)
        rows = newRows

        if len(rows) == 0:
            return False

        if showcolumns != []:
            rows2 = rows
            rows = []
            for row in rows2:
                if row[0] in showcolumns:
                    rows.append(row)

        data = [list(x) for x in zip(*rows)][1:]

        for row in rows:
            if row[0] in columnAliases:
                legend.append(columnAliases[row[0]])
            else:
                legend.append(row[0])

        if str(headers) != "":
            if len(headers) == len(data) + 1:
                headers = headers[1:]
            # headers=[""]+headers
            if len(headers) != len(data):
                #raise RuntimeError("headers has more items then nr columns")
                print("Cannot process headers, wrong nr of cols")
                self.addMessage("ERROR header wrong nr of cols:%s" % headers)
                headers = []

                # headers = [] #Wrong number of headers
        else:
            headers = []

        self._addChartJS()
        self._chartId += 1
        chartId = 'chart-%s' % (self._chartId)

        te = j.tools.code.template_engine_get()
        te.add('chartId', chartId)
        te.add('chartTitle', title)
        te.add('chartData', str(data))
        te.add('chartHeaders', str(headers))  # labels
        te.add('chartLegend', str(legend))
        te.add('chartWidth', str(width))
        te.add('chartHeight', str(height))
        if onclickfunction == '':
            onclickfunction = 'function(){}'
        te.add('onclickfunction', onclickfunction)

        jsContent = te.replace(self._chartTemplateContent)

        self.addScriptBodyJS(jsContent)
        chartContainer = "<canvas id='%s' width='%s' height='%s' >[No Canvas Support!]</canvas>" % (
            chartId, width, height)
        self.addMessage(chartContainer, isElement=True, newline=True)

    def addPieChart(self, title, data, legend, width=1000, height=600, donut=False):
        """
        Add pie chart as the HTML element
        @param data is array of data points
        @param legend [legendDataPoint1, legendDataPoint2, ..]
        """
        self._addChartJS()
        self._pieId += 1
        pieId = 'pie-%s' % (self._pieId)

        te = j.tools.code.template_engine_get()
        te.add('pieId', pieId)
        te.add('pieTitle', title)
        te.add('pieData', str(data))
        te.add('pieLegend', str(legend))

        donut = 'donut' if donut else 'pie'
        te.add('donut', donut)

        jsContent = te.replace(self._pieTemplateContent)

        self.addScriptBodyJS(jsContent)
        pieContainer = "<canvas id='%s' width='%s' height='%s' >[No Canvas Support!]</canvas>" % (pieId, width, height)
        self.addMessage(pieContainer, isElement=True, newline=True)

    @staticmethod
    def _format_styles(styles):
        """
        Return CSS styles, given a list of CSS attributes
        @param styles a list of tuples, of CSS attributes, e.g. [("background-color", "green), ("border", "1px solid green")]

        >>> PageHTML._format_styles([("background-color", "green"), ("border", "1px solid green")])
        'background-color: green; border: 1px solid green'
        """
        try:
            return '; '.join('{0}: {1}'.format(*style) for style in styles)
        except IndexError:
            return ''

    def addImage(self, title, imagePath, width=None, height=None, styles=[]):
        """
        @param title alt text of the image
        @param imagePath can be url or local path
        @param width width of the image
        @param height height of the image
        @param styles a list of tuples, containing CSS attributes for the image, e.g. [("background-color", "green), ("border", "1px solid green")]
        """
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
        table = "<table><thead><tr>"
        for colWidth, colContent in zip(columnsWidth, colContents):
            if colWidth:
                table += "<th width='%s'>%s</th>" % (colWidth, colContent)
            else:
                table += "<th>%s</th>" % (colContent)
        table += "</tr></head></table>"
        self.addMessage(table, isElement=True)

    def addHTML(self, htmlcode):
        #import cgi
        #html = "<pre>%s</pre>" % cgi.escape(htmlcode)
        self.addMessage(htmlcode, isElement=False)

    def removeCSS(self, exclude, permanent=False):
        """
        will walk over header and remove css links
        link need to be full e.g. bootstrap.min.css
        """
        out = ""
        for line in self.head.split("\n"):
            if line.lower().find(exclude) == -1:
                out += "%s\n" % line
        self.head = out
        if permanent:
            key = exclude.strip().lower()
            self.jscsslinks[key] = True

    def addCSS(self, cssLink=None, cssContent=None, exlcude="", media=None):
        """
        """
        if self.pagemirror4jscss is not None:
            self.pagemirror4jscss.addCSS(cssLink, cssContent)
        if cssLink is not None:
            key = cssLink.strip().lower() + (media or '')
            if key in self.jscsslinks:
                return
            self.jscsslinks[key] = True

        mediatag = ""
        if media:
            mediatag = "media='%s'" % media
        if cssContent:
            css = "\n<style type='text/css' %s>%s\n</style>\n" % (mediatag, cssContent)
        else:
            css = "<link  href='%s' type='text/css' rel='stylesheet' %s/>\n" % (cssLink, mediatag)
        self.head += css

    def addTimeStamp(self, classname='jstimestamp'):
        js = """
        $(function() {
            var updateTime = function () {
                $(".%s").each(function() {
                    var $this = $(this);
                    var timestmp = parseFloat($this.data('ts'));
                    if (timestmp > 0)
                        var time = new Date(timestmp * 1000).toLocaleString();
                    else var time = "";
                    $this.html(time);
                });
            };
            updateTime()
            window.updateTime = updateTime;
            $(document).ajaxComplete(updateTime);
        });
        """ % classname
        if classname not in self._timestampsAdded:
            self.addJS(jsContent=js)
            self._timestampsAdded.add(classname)

    def addJS(self, jsLink=None, jsContent=None, header=True):
        if self.pagemirror4jscss is not None:
            self.pagemirror4jscss.addJS(jsLink, jsContent, header)
        if jsLink is not None:
            key = jsLink.strip().lower()
            if key in self.jscsslinks:
                return
            self.jscsslinks[key] = True

        if jsContent:
            js = "<script type='text/javascript'>\n%s</script>\n" % jsContent
        else:
            js = "<script  src='%s' type='text/javascript'></script>\n" % jsLink
            #js = "<script  src='%s' </script>\n" % jsLink
        if header:
            self.head += js
        else:
            if js not in self.tail:
                self.tail.append(js)

    def removeJS(self, jsLink=None, jsContent=None):
        out = ""
        js = ''
        if jsContent:
            js = "<script type='text/javascript'>\n%s</script>\n" % jsContent
        else:
            js = "<script  src='%s' type='text/javascript'></script>\n" % jsLink
        self.head = self.head.replace(js.strip(), '')
        self.body = self.body.replace(js.strip(), '')

    def addScriptBodyJS(self, jsContent):
        self.scriptBody = "%s%s\n" % (self.scriptBody, jsContent)

    def _addChartJS(self):
        if self._hasCharts:
            return

        self.addJS("%s/old/rgraph/RGraph.common.core.js" % self.liblocation)
        self.addJS("%s/old/rgraph/RGraph.bar.js" % self.liblocation)
        self.addJS("%s/old/rgraph/RGraph.pie.js" % self.liblocation)
        self.addJS("%s/old/rgraph/RGraph.line.js" % self.liblocation)
        self.addJS("%s/old/rgraph/RGraph.common.key.js" % self.liblocation)
        self.addJS("%s/old/rgraph/RGraph.common.effects.js" % self.liblocation)
        self.addJS("%s/old/rgraph/RGraph.common.dynamic.js" % self.liblocation)

        self._hasCharts = True

    def addJQuery(self):
        self.addJS('/jslib/jquery/jquery-2.2.1.min.js')
        self.addJS('/jslib/jquery/jquery-migrate-1.2.1.js')
        self.addJS("/jslib/jquery/jquery-ui.min.js")

    def addBootstrap(self, jquery=True):
        if jquery:
            self.addJQuery()

        self.addJS('/jslib/bootstrap/js/bootstrap-3-3-6.min.js')
        self.addCSS('/jslib/bootstrap/css/bootstrap-3-3-6.min.css')

    def addBodyAttribute(self, attribute):
        if attribute not in self.bodyattributes:
            self.bodyattributes.append(attribute)

    def addHostBasedContent(self):
        if self._hostbasedmacro:
            return
        else:
            extracontent = """
    filter_div = function(par) {
         host = window.location.hostname
         if (host == par['hostname'])
         {
              doc = document.getElementById(par['divid'])
              if (doc != null)
              {
                doc.style.visibility = "visible";
                doc.style.display = "inline";
              }
         }
    }
    $(document).ready(function() { tocheck.map(filter_div);})
    """
            self.addJS(jsContent=extracontent)
            self._hostbasedmacro = True

    def addDocumentReadyJSfunction(self, function):
        """
        e.g. $('.dataTable').dataTable();
        """
        if self.pagemirror4jscss is not None:
            self.pagemirror4jscss.addDocumentReadyJSfunction(function)
        if function not in self.documentReadyFunctions:
            self.documentReadyFunctions.append(function)

    def addExplorer(self, path="", dockey=None, height=500, width=750, readonly=False, tree=False):
        self.addJQuery()
        self.addJS("%s/jquery/jquery-ui.min.js" % self.liblocation)
        self.addJS("%s/old/elfinder/jquery-ui.min.js" % self.liblocation)
        self.addCSS("%s/old/jquery-ui.css" % self.liblocation)
        self.addCSS("%s/old/elfinder/css/elfinder.min.css" % self.liblocation)
        self.addCSS("%s/old/elfinder/css/theme.css" % self.liblocation)
        self.addJS("%s/old/elfinder/js/elfinder.min.js" % self.liblocation)
        self.addJS("%s/old/elfinder/js/proxy/elFinderSupportVer1.js" % self.liblocation)
        # codemirror resources
        self.addCSS('%s/old/codemirror/lib/codemirror.css' % self.liblocation)
        self.addCSS('%s/old/codemirror/addon/hint/show-hint.css' % self.liblocation)
        self.addCSS('%s/old/codemirror/theme/elegant.css' % self.liblocation)
        self.addJS('%s/old/codemirror/lib/codemirror.js' % self.liblocation)
        self.addJS('%s/old/codemirror/addon/hint/show-hint.js' % self.liblocation)
        self.addJS('%s/old/codemirror/addon/hint/python-hint.js' % self.liblocation)
        self.addJS('%s/old/codemirror/mode/python/python.js' % self.liblocation)

        if readonly:
            commands = """
	    commands : [
	    'open', 'reload', 'home', 'up', 'back', 'forward', 'getfile',
	    'archive',
	    'resize', 'sort', 'ping'
	    ],"""

            dircmd = "'reload', 'back', 'ping'"
            filecmd = "'open', '|', 'download', 'ping', '|', 'archive',"
        else:
            # customData : {rootpath:'$path'} ,
            commands = """
	    commands : [
	    'quicklook', 'reload', 'home', 'up', 'back', 'forward', 'getfile',
	    'rm', 'duplicate', 'rename', 'mkdir', 'mkfile', 'upload', 'copy',
	    'cut', 'paste','extract', 'archive', 'help',
	    'resize', 'sort', 'edit', 'ping', 'download'
	    ],"""
            dircmd = "'reload', 'back', 'ping', '|', 'upload', 'mkdir', 'mkfile', 'paste'"
            filecmd = "'quicklook', '|', 'download', '|', 'copy', 'cut', 'paste', 'duplicate', '|',\
	                'rm', '|', 'edit', 'ping', 'rename', 'resize', '|', 'archive', 'extract',"

        C = """
<script type="text/javascript" charset="utf-8">
     $(document).ready(function() {
        elFinder.prototype.i18.en.messages['cmdping'] = 'Ping';
        elFinder.prototype._options.commands.push('ping');
        elFinder.prototype.commands.ping = function() {
            // Add command shortcuts
            // this.shortcuts = [{
            //     pattern     : 'ctrl+t'
            // }];

            // return 0 to enable command, -1 to disable
            this.getstate = function(sel) {
                return 0;
            }

            // execute the command business itself
            this.exec = function(hashes) {
                $.each(this.files(hashes), function(i, file) {
                    // here you have refs to files
                });
                $.ajax({
                  url: "/restmachine/system/master/ping"
                })
                  .done(function( data ) {
                    alert(data);
                });
                return;
            }
        }
        CodeMirror.commands.autocomplete = function(cm) {
            CodeMirror.showHint(cm, CodeMirror.hint.python);
        };
        var options=
        {
            defaultView : 'list',
	        url : '/elfinder/$dockey',
	        height : $height,
            width : $width,
            transport : new elFinderSupportVer1(),
	        {commands}
            commandsOptions: {
                edit : {
                editors : [{
                    mimes : ['text/plain', 'text/html', 'text/javascript', 'text/x-python', 'text/x-php', 'text/css', 'text/rtf', 'text/x-ruby', 'text/x-shellscript', 'application/msword'],
                    load : function(textarea) {
                        this.myCodeMirror = CodeMirror.fromTextArea(textarea, {
                            lineNumbers: true,
                            theme: "elegant",
                            mode: "python",
                            indentUnit: 4,
                            extraKeys: {"Ctrl-Space": "autocomplete"},

                            onCursorActivity: function() {
                                editor1.addLineClass(hlLine, null, null);
                                hlLine = editor1.addLineClass(editor1.getCursor().line, null, "activeline");
                        }});
                        this.myCodeMirror.setSize(790, 600);
                    },
                    close : function(textarea, instance) {
                        this.myCodeMirror = null;
                    },
                    save : function(textarea, editor) {
                      textarea.value = this.myCodeMirror.getValue();
                      this.myCodeMirror = null;
                    }
                    } ]
                }
            },
	        ui :[{tree}'path', 'stat'],

            getFileCallback : function(files, fm) {
                 return false;
            },

	        handlers :
            {
	            // extract archive files on upload
                dblclick : function(event, elfinderInstance) {
                    event.preventDefault();
                    elfinderInstance.exec('getfile')
                        .done(function() { elfinderInstance.exec('download'); })
                        .fail(function() { elfinderInstance.exec('open'); });
                },
	            upload : function(event, instance)
	            {
	                var uploadedFiles = event.data.added;
	                var archives = ['application/zip', 'application/x-gzip', 'application/x-tar', 'application/x-bzip2'];
	                for (i in uploadedFiles)
	                {
	                    var file = uploadedFiles[i];
	                    if (jQuery.inArray(file.mime, archives) >= 0)
	                    {
                        instance.exec('extract', file.hash);
                        }
                    }
	            }
	        },
	        contextmenu :
            {
	          // navbarfolder menu
	          //navbar : ['open', '|', 'copy', 'cut', 'paste', 'duplicate', '|', 'rm'],

	          // current directory menu
	          cwd    : [{dircmd}],

	          // current directory file menu
	          files  : [
	                {filecmd}
              ]
	        },
            ui: ['toolbar'],
            uiOptions :
            {
                toolbar : [
		['back', 'forward'],
        ['reload', 'download'],
        ['home', 'up']
	],
            	tree :
                {
                    // expand current root on init
                    openRootOnLoad : true,
                    // auto load current dir parents
                    //syncTree : true
                },
                // navbar options
                navbar : {
                    minWidth : 100,
                    maxWidth : 100
                },
            },
        }

        $('#elfinder{nr}').elfinder(options);
	});
</script>
"""
        # //var elf = $('#elfinder').elfinder(options);
        height = str(height)
        C = C.replace("$height", str(height))
        C = C.replace("$width", str(width))
        C = C.replace("{commands}", commands)
        self._explorerInstance += 1
        C = C.replace("{nr}", str(self._explorerInstance))
        if tree:
            C = C.replace("{tree}", "'places', 'tree',")
        else:
            C = C.replace("{tree}", "")

        C = C.replace("{dircmd}", dircmd)
        C = C.replace("{filecmd}", filecmd)
        if dockey is None:
            dockey = j.data.hash.md5_string(path)
        C = C.replace("$dockey", dockey)
        db = j.data.kvs.getRedisCacheLocal()
        db.set(key=dockey, value=path)

        self.head += C
        self.addBootstrap(jquery=False)
        self.addMessage("<div id=\"elfinder%s\"></div>" % self._explorerInstance)

    # def _generateFromTemplate(self, filePath, params):
        #fd = open(filePath, 'r')
        #contents = fd.read()
        # fd.close()
        #from Cheetah.Template import Template
        #template = Template(contents, params)
        #contents = str(template)
        # return contents
    # def _generateChartFromTemplate(self, params):
        # return self._generateFromTemplate(self._chartTemplate, params)
    # def _generateLineFromTemplate(self, params):
        # return self._generateFromTemplate(self._lineTemplate, params)
    # def _generatePieFromTemplate(self, params):
        # return self._generateFromTemplate(self._pieTemplate, params)
    def _generateChartScript(self):
        js = ""
        if(self._hasCharts):
            js = "<script type='text/javascript'>\n%s\n" % "window.onload = function () {"
            js += self.scriptBody
            js += "\n};\n</script>\n"
        return js

    def addHTMLHeader(self, header):
        self.head += header

    def addHTMLBody(self, body):
        self.body += body

    def addAccordion(self, panels):
        self.addJS('/jslib/codemirror/autorefresh.js', header=False)
        self.addMessage('<div class="panel-group" id="accordion" role="tablist" aria-multiselectable="true">')

        panels.sort(key=lambda x: x['title'])

        for panel_data in panels:
            if panel_data is None:
                continue

            content = panel_data['content']

            for item in ['header_id', 'section_id', 'label_id', 'label_icon', 'label_color']:
                if item not in panel_data:
                    panel_data[item] = j.data.idgenerator.generateXCharID(10)

            self.addMessage("""
            <div class="panel panel-default">
              <div class="panel-heading" role="tab" id="%(header_id)s">
                <h4 class="panel-title">
                  <a data-toggle="collapse" data-parent="#accordion" href="#%(section_id)s" aria-expanded="true" aria-controls="%(section_id)s">%(title)s</a>
            """ % panel_data)

            if 'label_content' in panel_data:
                self.addMessage("""
                <a id=%(label_id)s class="label-archive label label-%(label_color)s glyphicon glyphicon glyphicon-%(label_icon)s pull-right">%(label_content)s</a>
                """ % panel_data)

            self.addMessage("""
                </h4>
              </div>
              <div id="%(section_id)s" class="panel-collapse collapse" role="tabpanel" aria-labelledby="%(header_id)s">
                <div class="panel-body">
                """ % panel_data)

            if panel_data.get('code', False):
                self.addCodeBlock(content, edit=False, exitpage=True, spacename='', pagename='', linenr=True, autorefresh=True)
            else:
                self.addMessage(content)

            self.addMessage("""
                </div> <!-- panel body-->
              </div> <!-- panel collapse-->
            </div> <!-- panel default-->""")

        self.addMessage('</div>')  # close panel-group

    def getContent(self):
        return str(self)

    def __str__(self):
        # make sure we get closures where needed (/div)
        self._checkBlock("DDD", "", "")
        if self.title != "":
            title = "<title>%s</title>\n" % self.title
        else:
            title = ""

        jsHead = title + self.head + self._generateChartScript()

        if (self.login or self._hasmenu) and (self.padding != False):
            jsHead += "\n<style type='text/css'>"
            if self.padding != True and self.padding.find("-") != -1:
                top, bottomn = self.padding.split("-")
                top = int(top.strip())
                bottomn = int(bottomn.strip())
                jsHead += "body {padding-top: %spx; padding-bottom: %spx;}</style> \n" % (top, bottomn)
            else:
                jsHead += "body {padding-top: 60px; padding-bottom: 40px;}</style> \n"

        if self._hasSidebar:
            jsHead += "<style type='text/css'> body.sidebar-nav {padding: 9px 0;} </style> \n"

        # if self.pagemirror4jscss != None:
        #     self.pagemirror4jscss.jsHead+=jsHead
        if self.documentReadyFunctions != []:
            CC = "$(document).ready(function() {\n"
            for f in self.documentReadyFunctions:
                CC += "%s\n" % f
            CC += "} );\n"
            jsHead += "<script type='text/javascript'>" + CC + "</script>"

        docdata = {'head': jsHead,
                   'bodyattrib': ' '.join(self.bodyattributes),
                   'body': self.body,
                   'favicon': self.favicon,
                   'tail': '\n'.join(self.tail)}
        for key, val in docdata.items():
            docdata[key] = j.data.text.toStr(val)
        return '''
<!DOCTYPE html>
<html>
<head>
 <meta charset="UTF-8">
%(favicon)s
%(head)s</head>
<body %(bodyattrib)s>%(body)s
%(tail)s</body>
</html>''' % docdata


from js9 import j
from Page import Page
import copy


class PageConfluence(Page):

    def __init__(self, name, content, parent="Home"):
        Page.__init__(self, name, content, parent)
        self.toc = False

    def addMessage(self, message, newline=False):
        message = message.strip()
        message = message.replace("\r", "")
        message = message.replace("text:u", "")

        if newline:
            message += "\n"
        if message != "":
            self.content = "%s%s\n" % (self.content, message)

    def addTOC(self):
        if self.toc is False:
            self.content += "{div:class=TOCPageNumber}{toc:outline=false|style=none|maxLevel=4|indent=15px}{div}\n"
            self.toc = True

    def addBullet(self, message, level=1):
        bullets = ""
        for i in range(level):
            bullets += "*"
        message = "%s %s" % (bullets, message)
        self.addMessage(message)

    def addNewLine(self, nrlines=1):
        for line in range(nrlines):
            self.addMessage("", True)

    def addPageBreak(self):
        self.content += "{pagebreak}\n"

    def addHeading(self, message, level=1):
        message = "h%s. %s" % (level, message)
        self.addMessage(message, True)

    def addList(self, rows, headers="", showcolumns=[], columnAliases={}):
        """
        @param rows [[col1,col2, ...]]  (array of array of column values)
        @param headers [header1, header2, ...]
        """
        if len(rows) == 0:
            return False
        l = len(rows[0])
        if l != len(headers) and headers != "":
            if len(headers) > l:
                while len(headers) != l:
                    headers.pop(0)

        # TODO: put more checks to check on validity  (id:29)
        if showcolumns != []:
            rows2 = rows
            rows = []
            for row in rows2:
                if row[0] in showcolumns:
                    rows.append(row)
            headers.insert(0, " ")

        c = ""  # the content
        if headers != "":
            for item in headers:
                if item == "":
                    item = " "
                c = "%s||%s" % (c, item)
            c += "||\n"
        rows3 = copy.deepcopy(rows)
        for row in rows3:
            if row[0] in columnAliases:
                row[0] = columnAliases[row[0]]
            for col in row:
                if col == "":
                    col = " "
                c += "|%s" % self.getRound(col)
            c += "|\n"
        self.addMessage(c, True)

    def addDict(self, dictobject, description="", keystoshow=[], aliases={}):
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

    def getLink(self, description, link):
        return "[%s|%s]" % (description, link)

    def addLink(self, description, link):
        msg = self.getLink(description, link)
        self.addBullet(msg)

    def addPageBreak(self,):
        msg = "{pagebreak}"
        self.addMessage(msg)

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

    def addCodeBlock(self, code):
        content = "{code}\n%s\n{code}\n" % code
        self.addMessage(content)

    def addCodePythonBlock(self, code, title="", removeLeadingTab=True):
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

        if title != "":
            content = "{code:language=python|title=%s|theme=Eclipse}\n%s\n{code}\n" % (title, code)
        else:
            content = "{code:language=python|theme=Eclipse}\n%s\n{code}\n" % (code)
        self.addMessage(content)

    def _getArray2Wiki(self, rows, headers="", showcolumns=[], columnAliases={}, round=0, cursymbol=""):
        """
        @param rows [[rowname,col1,col2, ...]]  (array of array of column values with first item the rowname)
        @param headers [header1, header2, ...]
        """
        # TODO: S4 P3 put more checks to check on validity  (id:84)
        # TODO: S4 P3  remove code duplication with addList( (id:85)
        l = len(rows[0])
        if l != len(headers) and headers != "":
            if len(headers) > l:
                while len(headers) != l:
                    headers.pop(0)

        if showcolumns != []:
            rows2 = rows
            rows = []
            for row in rows2:
                if row[0] in showcolumns:
                    rows.append(row)

        c = ""  # the content
        if headers != "":
            for item in headers:
                if item == "":
                    item = " "
                c = "%s||%s" % (c, item)
            c += "||\n"

        rows3 = copy.deepcopy(rows)
        for row in rows3:
            if row[0] in columnAliases:
                row[0] = columnAliases[row[0]]
            for col in row:
                if col == "":
                    col = " "
                if j.data.types.float.check(col):
                    if round == 0:
                        col = "%s%s" % (cursymbol, int(col))
                    else:
                        col = "%s%.2f" % (cursymbol, float(col))
                c += "|%s" % col
            c += "|\n"
        return c

    def addTable(self, rows, columnAliases=None, columnsToShow=None, defaultCellValue=None):
        '''
        Adds a table to the confluence page.

        *Important!*
        When rows is a list of objects, the columnsToShow argument is required. It is used to
        determine which	attributes should be included in the table. But when rows objects are
        of type dictionary, the columnsToShow argument becomes optional. And used to determine
        which columns should be included in the table. The keys of the dictionaries map to the
        table column names.

        *Code sample:*
        rows = list()
        rows.append({'col_1': 'col_1_val', 'col_3': 'col_3_val'})
        rows.append({'col_1': 'col_1_val', 'col_2': 'col_2_val'})
        rows.append({'col_1': 'col_1_val', 'col_2': 'col_2_val', 'col_3': 'col_3_val'})
        rows.append({'col_2': 'col_2_val', 'col_3': 'col_3_val'})

        page = j.tools.wikigenerator.pageNewConfluence('confluence_test_page')
        columnAliases = {'col_1': 'column 1', 'col_3': 'column 3'}
        columnsToShow = ['col_3', 'col_1']
        defaultCellValue = '    /    '
        page.addTable(rows, columnAliases, columnsToShow, defaultCellValue)

        *Generated table macro:*
        ||column 3||column 1||
        |col_3_val|col_1_val|
        |    /    |col_1_val|
        |col_3_val|col_1_val|
        |col_3_val|    /    |

        @param rows: rows of the table
        @type rows: List(Object)

        @param columnAliases: aliases for the column names, defaults to an empty dict
        @type columnAliases: Dict(String)

        @param columnsToShow: columns to show in the page, defaults to a set containing all available columns
        @type columnsToShow: Set(String)

        @defaultCellValue: default value for an empty or non existing row column (cell) , defaults to a string with one space char
        @type defaultCellValue: String
        '''

        firstRow = rows[0]

        if not isinstance(firstRow, dict) and not columnsToShow:
            raise RuntimeError(
                'Invalid columnsToShow, expected a list of strings because rows is not a list of dictionaries')

        columnAliases = columnAliases or dict()
        defaultCellValue = defaultCellValue or ' '

        # determine columns to show
        if not columnsToShow:
            columnsToShow = set()

            for row in rows:
                columns = set(row.keys())
                columnsToShow.union(columns)

        macroLines = list()

        # generate table header
        headerItems = list()

        for column in columnsToShow:
            headerItem = columnAliases.get(column, column)
            headerItems.append(headerItem)

        line = '||%s||' % '||'.join(headerItems)
        macroLines.append(line)

        # generate table rows
        for row in rows:
            cells = list()

            for column in columnsToShow:
                cell = None

                if isinstance(row, dict) and column in row:
                    cell = row.get(column)
                elif hasattr(row, column):
                    cell = getattr(row, column)

                if not cell:
                    cell = defaultCellValue

                cells.append(cell)

            line = '|%s|' % '|'.join(cells)
            macroLines.append(line)

        macro = '\n'.join(macroLines)

        self.addMessage(macro)

    def addLineChart(self, title, rows, headers="", width=800, height=300):
        """
        @param rows [[values, ...],]  first value of the row is the rowname e.g. cost, revenue
        @param headers [] first value is name of the different rowtypes e.g. P&L
        """
        content =\
            """
{chart:title=%s|type=line|legend=true|width=%s|height=%s}
%s
{chart}
""" % (title, width, height, self._getArray2Wiki(rows, headers))
        self.addMessage(content, True)
        self.addNewLine()

    def addBarChart(self, title, rows, headers="", width=800, height=300, showcolumns=[], columnAliases={}):
        """
        order is list of items in rows & headers, defines the order and which columns to show
        """

        content =\
            """
{chart:title=%s|type=bar|legend=true|width=%s|height=%s}
%s
{chart}
""" % (title, width, height, self._getArray2Wiki(rows, headers, showcolumns, columnAliases))
        self.addMessage(content, True)
        self.addNewLine()

    def _getUnderlineString(self, message):
        line = ""
        for i in range(len(message)):
            line = line + "="
        return "%s\n%s" % (message, line)

    def __repr__(self):
        return self.content

    def __str__(self):
        return self.__repr__()

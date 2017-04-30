
from js9 import j


class PageGroup:

    def __init__(self, pages):
        self.pages = pages
        self.actions = {}

    def initActions(self, actions):
        """
        @actions is dict with as key the name of the action, the value is the link with {params} which will be filled in with the remainder of the link
        """
        self.actions = actions
        for key in list(self.pages.keys()):
            self.pages[key].actions = actions

    def getPages(self, types):
        pages = []
        if types == "*":
            for key in list(self.pages.keys()):
                pages.append(self.pages[key])
        for typechar in types:
            if typechar in self.pages:
                pages.append(self.pages[typechar])
        return pages

    def addMessage(self, types, message, newline=False):
        for page in self.getPages(types):
            page.addMessage(message, newline)

    def addBullet(self, types, message, level=1):
        for page in self.getPages(types):
            page.addBullet(message, level)

    def addNewLine(self, types):
        for page in self.getPages(types):
            page.addNewLine()

    def addHeading(self, types, message, level=1):
        for page in self.getPages(types):
            page.addHeading(message, level)

    def addList(self, types, rows, headers="", showcolumns=[], columnAliases={}):
        """
        @param rows [[col1,col2, ...]]  (array of array of column values)
        @param headers [header1, header2, ...]
        """
        for page in self.getPages(types):
            page.addList(rows, headers, showcolumns, columnAliases)

    def addDict(self, types, dictobject, description="", keystoshow=[], aliases={}, roundingDigits=None):
        """
        @params aliases is dict with mapping between name in dict and name to use
        """
        for page in self.getPages(types):
            page.addDict(dictobject, description, keystoshow, aliases, roundingDigits)

    def addLink(self, types, description, link):
        for page in self.getPages(types):
            page.addLink(description, link)

    def addPageBreak(self, types):
        for page in self.getPages(types):
            page.addPageBreak()

    def addActionBox(self, types, actions):
        """
        @actions is array of array, [[$actionname1,$params1],[$actionname2,$params2]]
        """
        for page in self.getPages(types):
            page.addActionBox(actions)

    def addCodeBlock(self, types, code):
        for page in self.getPages(types):
            page.addCodeBlock(code)

    def addCodePythonBlock(self, types, code, title="", removeLeadingTab=True):
        for page in self.getPages(types):
            page.addCodePythonBlock(code, title, removeLeadingTab)

    def addLineChart(self, types, title, rows, headers="", width=800, height=300):
        """
        @param rows [[values, ...],]  first value of the row is the rowname e.g. cost, revenue
        @param headers [] first value is name of the different rowtypes e.g. P&L
        """
        for page in self.getPages(types):
            page.addLineChart(title, rows, headers, width, height)

    def addBarChart(self, types, title, rows, headers="", width=800, height=300, showcolumns=[], columnAliases={}):
        """
        order is list of items in rows & headers, defines the order and which columns to show
        """
        for page in self.getPages(types):
            page.addBarChart(title, rows, headers, width, height, showcolumns, columnAliases)

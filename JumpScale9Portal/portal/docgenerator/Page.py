
from js9 import j


class Page(object):

    def __init__(self, name, content, parent="Home"):
        self.name = name
        if content != "" and content[-1] != "\n":
            content += "\n"
        self.content = content
        self.currentlinenr = len(self.content.split("\n")) + 1
        self.actions = {}
        self.parent = parent

    def getRound(self, value):
        if isinstance(value, int) or isinstance(value, float):
            if not isinstance(value, int):
                if value > 0 and value < 10:
                    valstr = str(round(value, 2))
                elif value < 0 and value > -10:
                    valstr = str(round(value, 2))
                else:
                    valstr = str(int(round(value, 0)))
            else:
                valstr = str(value)
            if valstr.find(".") != -1:
                valstr2 = valstr.split(".")[1]
                valstr = valstr.split(".")[0]
            else:
                valstr2 = ""
            if len(valstr) > 9:
                valstr = valstr[:-9] + "," + valstr[-9:-6] + "," + valstr[-6:-3] + "," + valstr[-3:]
            elif len(valstr) > 6:
                valstr = valstr[:-6] + "," + valstr[-6:-3] + "," + valstr[-3:]
            elif len(valstr) > 3:
                valstr = valstr[:-3] + "," + valstr[-3:]
            if valstr2 != "":
                valstr += "." + valstr2
            return valstr
        else:
            return value

    def addMessage(self, message, newline=False):
        raise NotImplemented()

    def addBullet(self, message, level=1):
        raise NotImplemented()

    def addNewLine(self):
        raise NotImplemented()

    def addHeading(self, message, level=1):
        raise NotImplemented()

    def addList(self, rows, headers="", showcolumns=[], columnAliases={}):
        """
        @param rows [[col1,col2, ...]]  (array of array of column values)
        @param headers [header1, header2, ...]
        """
        raise NotImplemented()

    def addDict(self, dictobject, description="", keystoshow=[], aliases={}, roundingDigits=None):
        """
        @params aliases is dict with mapping between name in dict and name to use
        """
        raise NotImplemented()

    def getLink(self, description, link):
        raise NotImplemented()

    def addLink(self, description, link):
        raise NotImplemented()

    def addPageBreak(self,):
        raise NotImplemented()

    def addActionBox(self, actions):
        """
        @actions is array of array, [[$actionname1,$params1],[$actionname2,$params2]]
        """
        raise NotImplemented()

    def addCodeBlock(self, code):
        raise NotImplemented()

    def addCodePythonBlock(self, code, title="", removeLeadingTab=True):
        raise NotImplemented()

    def _getArray2Wiki(self, rows, headers="", showcolumns=[], columnAliases={}):
        """
        @param rows [[rowname,col1,col2, ...]]  (array of array of column values with first item the rowname)
        @param headers [header1, header2, ...]
        """
        raise NotImplemented()

    def addLineChart(self, title, rows, headers="", width=800, height=300):
        """
        @param rows [[values, ...],]  first value of the row is the rowname e.g. cost, revenue
        @param headers [] first value is name of the different rowtypes e.g. P&L
        """
        raise NotImplemented()

    def addBarChart(self, title, rows, headers="", width=800, height=300,
                    showcolumns=[], columnAliases={}, onclickfunction=''):
        """
        order is list of items in rows & headers, defines the order and which columns to show
        """
        raise NotImplemented()

    def addImage(self, imagePath, width=800, height=300):
        """
        @param imagePath can be url or local path
        """
        raise NotImplemented()

    def _getUnderlineString(self, message):
        raise NotImplemented()

    def __repr__(self):
        return self.content

    def __str__(self):
        return self.__repr__()


from js9 import j
import copy


def extractDetails(remoteException):
    """Extract the details of an xml-rpc exception error message"""
    try:
        details = remoteException.faultString or remoteException.message
        details = details.split(":", 2)[-1].replace("'>", "").lstrip()
    except AttributeError:
        details = str(remoteException)

    return details.replace('\n', '; ')  # just in case the returned error message contains an newline


class WikiClientConfluence:

    def __init__(self, spacename, erasespace=False, erasepages=False):
        self.spacename = spacename
        spaces = j.clients.confluence.listSpaces()
        spacenames = [item.key for item in spaces]
        if spacename in spacenames and erasespace:
            j.clients.confluence.removeSpace(spacename)
        if spacename not in spacenames or erasespace:
            j.clients.confluence.addSpace(spacename, spacename)

        if erasepages and not erasespace:
            self.removeAllPages()

        self.actions = {}

    def removeAllPages(self, exclude=[]):
        """
        remove all pages in space
        """
        pages = j.clients.confluence.listPages(self.spacename)
        pageids = [item.id for item in pages if not (item.title == "Home" or item.title in exclude)]

        for id in pageids:
            j.tools.console.echo("Remove page %s" % id)
            j.clients.confluence.removePage("%s" % id)

    def pageExists(self, pagename):
        try:
            page = j.clients.confluence.findPage(self.spacename, pagename)
            return page
        except Exception as ex:
            if str(ex).find("does not exist") != -1:
                return False
            raise Exception('Unable to find page %s in space %s' % (pagename, self.spacename) +
                            '. Reason %s' % extractDetails(ex))

    def pageDelete(self, pagename):
        page = self.pageExists(pagename)
        if page != False:
            print(("delete page %s" % page.title))
            j.clients.confluence.removePage(page.id)

    def pageContentGet(self, pagename):
        pageid = self.pageExists(pagename)
        if pageid != False:
            page = j.clients.confluence.getPage(pageid)
            return page.content
        else:
            raise RuntimeError("cannot find page with space %s and name %s" % (self.spacename, pagename))

    def createPagetree(self, pagetree):
        """
        @pagetree $toppage/$subpage1/$subpage2/...
        """
        if pagetree is None:
            return None

        def getContent(pagename):
            return "h2. %s\n\n{children}\n" % pagename
        pagetree = pagetree.replace("\\", "/")
        pagetree = pagetree.replace("//", "/")
        if pagetree[0] == "/":
            pagetree = pagetree[1:]
        pagenames = pagetree.split("/")
        if len(pagenames) == 1:
            return pagenames[0]
        if len(pagenames) == 0:
            raise RuntimeError("Cannot create pagetree because pagetree empty")
        if not self.pageExists(pagenames[0]):
            raise RuntimeError(
                "Cannot create createPagetree: %s because could not find parent %s" %
                (pagetree, pagenames[0]))
        parentname = pagenames.pop(0)
        for pagename in pagenames:
            page = self.pageExists(pagename)
            if page is False:
                self.pageContentSet(pagename, getContent(pagename), parent=parentname)
            parentname = pagename
        return pagename

    def pageContentSet(self, pagename, content, parent=None):
        """
        @param parent can be a single name of a home page or a pagetree e.g. $toppage/$subpage1/$subpage2/...
        """
        parentid = None
        parent = self.createPagetree(parent)
        if parent is not None:
            parentpage = self.pageExists(parent)
            if parentpage:
                parentid = parentpage.id
            if parent is not None and parentpage is False:
                raise RuntimeError("Cannot find parent page with name %s" % parent)
        page = self.pageExists(pagename)
        if page != False:
            pageid = page.id
        if page != False and parent != None and page.parent.id != parentid:
            j.tools.console.echo(
                "Warning: page %s is connected to wrong parent %s, should be %s" %
                (pagename, page.parent.id, parentid))
            # print "delete page %s" % page.title
            # self.pageDelete(pagename)
            pageid = False
        if page != False:
            page.content = content
            print(("editpage %s" % page.title))
            result = j.clients.confluence.editPage(page)
        else:
            print(("add page %s" % pagename))
            result = j.clients.confluence.addPage(self.spacename, pagename, parentid, content)

    def pageNew(self, pagename):
        page = Page(pagename, "")
        page.actions = self.actions
        return page

    def pageGet(self, pagename):
        content = self.pageContentGet(pagename)
        page = Page(pagename, content)
        page.actions = self.actions
        return page

    def pageSet(self, page, parent=None):
        """
        @param parent is name of wikipage to use as parent
        """
        return self.pageContentSet(page.name, page.content, parent)

    def generate(self, page, parent=None):
        if parent is None and page.parent is not None:
            parent = page.parent
        if parent == "":
            parent = None
        return self.pageContentSet(page.name, page.content, parent)

    def generatePagegroup(self, pagegroup):
        for key in list(pagegroup.pages.keys()):
            page = pagegroup.pages[key]
            self.pageContentSet(page.name, page.content, page.parent)

    def initActions(self, actions):
        """
        @actions is dict with as key the name of the action, the value is the link with {params} which will be filled in with the remainder of the link
        """
        self.actions = actions

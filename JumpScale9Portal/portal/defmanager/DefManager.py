
from js9 import j


class Def():

    def __init__(self):
        self.pagename = ""
        self.name = ""
        self.content = ""


class DefManager():

    def __init__(self):
        self.__jslocation__ = "j.portal.tools.defmanager"
        self.inited = False
        self.defs = {}
        self.aliases = {}

    def _init(self, doc):
        # walk over all docs in space & look for definitions & process
        for doc in doc.preprocessor.docs:
            if doc.content == "":
                doc.loadFromDisk(preprocess=False)
            aliases = []
            name = ""
            if doc.content.find("@def") != -1:
                # print "FINDDEF:%s"%doc.path
                content = ""
                for line in doc.content.split("\n"):
                    if line.strip() == "" or line.strip()[0] == "#":
                        content += "%s\n" % line
                        continue
                    if line.strip()[0] == "@" and line.find("@def") != -1:
                        # defline
                        name = line.split("@def", 1)[1].strip()
                    elif line.strip()[0] == "@" and line.find("@alias") != -1:
                        # defline
                        aliases = line.split("@alias", 1)[1].strip().split(",")
                    else:
                        content += "%s\n" % line
                doc.content = content
                pagename = j.sal.fs.getBaseName(doc.path).split(".", 1)[0]
                aliases.append(pagename)
                if name == "":
                    name = pagename
                else:
                    aliases.append(name)

                deff = Def()
                deff.name = name
                deff.pagename = pagename
                deff.content = doc.content
                id = name.lower().replace("_", "").replace("-", "").replace(" ", "")
                aliases.append(id)
                # print "ID:%s"%id
                self.defs[id] = deff
                for alias in aliases:
                    alias = alias.lower().replace("_", "").replace("-", "").replace(" ", "")
                    self.aliases[alias] = id

        self.inited = True

    def getDefListWithLinks(self):
        result = []
        keys = sorted(self.aliases.keys())
        res = {}
        aliases = {}
        for alias in keys:
            ddef = self.defGet(alias)
            link = "[%s|%s]" % (ddef.name, ddef.pagename)
            res[ddef.name.lower()] = link
            if ddef.name not in aliases:
                aliases[ddef.name.lower()] = []
            aliases[ddef.name.lower()].append(alias)

        keys = sorted(res.keys())
        for item in keys:
            # if item in aliases[item]:
            #     aliases.pop(item)
            result.append([item, res[item], aliases[item]])

        return result

    def processDefs(self, doc):
        doc.processDefs = True
        if self.inited is False:
            self._init(doc)
        return doc

    def defExists(self, name):
        return token in self.aliases

    def defGet(self, name):
        name = name.lower().replace("_", "").replace("-", "").replace(" ", "")
        if name in self.aliases:
            name = self.aliases[name]
        if name not in self.defs:
            return None
        return self.defs[name]

    def replaceDefWithProperName(self, txt):
        ddef = self.defGet(txt)
        if ddef is None:
            return txt
        else:
            return ddef.name

    def getLink(self, txt):
        ddef = self.defGet(txt)
        if ddef is None:
            return None
        else:
            return "[%s|%s]" % (ddef.name, ddef.pagename)

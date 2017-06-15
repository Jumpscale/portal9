from js9 import j

from JumpScale9Lib.tools.codetools.ClassBase import ClassBase


class Specbase(ClassBase):

    def __init__(self, linenr):
        self.name = ""
        self.description = ""
        self.tags = ""
        self.comment = ""
        self.linenr = linenr

    def addDefaults(self):
        pass

    def getDefaultValue(self, type, value):
        if value.strip() == "" or value.strip() == "None":
            return None
        elif j.data.types.string.check(value):
            value = value.strip("\"")
        if type == 'int' and value:
            return int(value)
        elif type == 'float' and value:
            return float(value)
        elif type == 'bool' and value:
            return j.data.types.bool.fromString(value)
        return value


class SpecEnum(Specbase):

    def __init__(self, name, specpath, linenr):
        Specbase.__init__(self, linenr)
        self.name = name
        self.specpath = specpath
        self.appname = ""
        self.enums = []
        self.actorname = ""

    def _parse(self, parser, content):
        for line in content.split("\n"):
            if line.strip() != "":
                self.enums.append(line.strip())


class Specactor(Specbase):

    def __init__(self, name, descr, tags, specpath, linenr):
        Specbase.__init__(self, linenr)
        self.name = name
        self.description = descr
        self.tags = tags
        self.specpath = specpath
        self.appname = ""
        self.methods = []
        self.type = ""

    def _addItem(self, obj):
        self.methods.append(obj)

    def addDefaults(self):
        pass


class SpecactorMethod(Specbase):

    def __init__(self, linenr):
        Specbase.__init__(self, linenr)
        self.vars = []
        self.result = None

    def _parseFirstLine(self, parser, line):
        self.comment, self.tags, line = parser.getTagsComment(line)
        self.name = line.strip()

    def _parse(self, parser, content):

        content = parser.deIndent(content, self.linenr)
        linenr = self.linenr
        for line in content.split("\n"):
            linenr += 1
            line0 = line
            if line.strip() == "" or line.strip()[0] == "#":
                continue
            if line.find(":") != -1:
                comments, tags, line = parser.getTagsComment(line)
                errormsg = "Syntax error, right syntax var:$name $type,$defaultvalue,$description @tags #remarks"
                try:
                    varname, line = line.split(":", 1)
                except BaseException:
                    return parser.raiseError(errormsg, line0, linenr)
                if varname == "var":

                    if line.find(" ") == -1:
                        return parser.raiseError(errormsg, line0, linenr)
                    else:
                        varname, line = line.split(" ", 1)
                    try:
                        ttype, default, descr = line.split(",", 2)
                    except BaseException:
                        return parser.raiseError(errormsg, line0, linenr)

                    default = self.getDefaultValue(ttype, default)

                    spec = SpecactorMethodVar(
                        varname, descr, tags, linenr, default, ttype)
                    spec.comment = comments
                    self.vars.append(spec)
                elif varname == "result":
                    errormsg = "Syntax error, right syntax result:$type @tags #remarks"
                    if line.find(" ") == -1 and (line.find("@") != -1 or line.find("$") != -1):
                        return parser.raiseError(errormsg, line0, linenr)
                    if line.find(" ") == -1:
                        ttype = line
                    else:
                        ttype, line = line.split(" ", 1)
                    self.result = Specbase(linenr)
                    self.result.type = ttype
                    self.result.comment = comments
                else:
                    return parser.raiseError("Only var & result support on line, syntaxerror.", line0, linenr)


class SpecactorMethodVar(Specbase):

    def __init__(self, name, descr, tags, linenr, default, ttype):
        Specbase.__init__(self, linenr)
        self.name = name
        self.description = descr
        self.tags = tags
        self.defaultvalue = default
        self.ttype = ttype


class SpecModel(Specbase):

    def __init__(self, name, descr, tags, specpath, linenr):
        Specbase.__init__(self, linenr)
        self.name = name
        self.description = descr
        self.tags = tags
        self.specpath = specpath
        self.properties = []
        self.type = ""
        self.actorname = ""
        self.rootobject = False

    def _addItem(self, obj):
        self.properties.append(obj)

    def exists(self, propname):
        for prop in self.properties:
            if str(prop.name) == propname:
                return True
        return False

    def addDefaults(self):
        if self.type == "rootmodel":
            if not self.exists("id"):
                s = SpecModelProperty(0)
                s.type = 'int'
                s.name = 'id'
                s.description = 'Auto generated id @optional'
                self._addItem(s)


class SpecModelProperty(Specbase):

    def __init__(self, linenr):
        Specbase.__init__(self, linenr)
        self.default = None
        self.type = None

    def _parseFirstLine(self, parser, line):
        errormsg = "Syntax error, right syntax prop:$name $type,$defaultvalue,$description @tags #remarks"
        line0 = "prop:%s" % line
        if line.find(" ") == -1:
            return parser.raiseError(errormsg, line0, self.linenr)
        else:
            self.name, line = line.split(" ", 1)
        try:
            self.type, self.default, self.description = line.split(",", 2)
            self.default = self.getDefaultValue(self.type, self.default)
        except BaseException:
            return parser.raiseError(errormsg, line0, self.linenr)

    def _parse(self, parser, content):
        pass


class SpecBlock:
    """
    generic block of specs identified with starting with [...]
    can be multiple types
    """

    def __init__(self, parser, line, linenr, appname, actorname):
        self.appname = appname
        self.actorname = actorname
        self.descr = ""
        self.content = ""
        self.name = ""
        self.comment, self.tags, line = parser.getTagsComment(
            line)  # get @ out of the block
        # if line.find("@") != -1:
        # line=line.split("@")[0]
        # if line.find("#") != -1:
        # line=line.split("#")[0]
        line = line.replace("[", "")
        if line.find("]") == -1:
            return parser.raiseError("each [ on block should finish with ]", line, linenr)
        line = line.replace("]", "").strip()

        splitted = line.split(":")
        splitted = [item.strip().lower() for item in splitted]
        self.type = splitted[0]
        if len(splitted) == 1:
            self.name = ""
        elif len(splitted) == 2:
            self.name = splitted[1]
        else:
            return parser.raiseError(
                "each [...] on block need to be in format [$type:$name] or  [$type], did not find :", line, linenr)

        self.parser = parser
        self.startline = linenr
        self.items = []

    def parse(self):

        self.content = self.parser.deIndent(self.content, self.startline)
        if self.type == "actor":
            ttypeId = "method"
            spec = None
            if len(list(j.portal.tools.specparser.specparserfactory.specs.keys())) > 0 and self.type == "actor":
                key = "%s_%s" % (self.appname, self.actorname)
                if key in j.portal.tools.specparser.specparserfactory.actornames:
                    spec = j.portal.tools.specparser.specparserfactory.getactorSpec(
                        self.appname, self.actorname, False)
            if spec is None:
                spec = Specactor(self.name, self.descr, self.tags,
                                 self.parser.path, self.startline)
                spec.actorname = self.actorname
                spec.appname = self.appname
            if spec.appname not in j.portal.tools.specparser.specparserfactory.app_actornames:
                j.portal.tools.specparser.specparserfactory.app_actornames[self.appname] = []
            if spec.actorname not in j.portal.tools.specparser.specparserfactory.app_actornames[self.appname]:
                j.portal.tools.specparser.specparserfactory.app_actornames[
                    self.appname].append(spec.actorname)
            currentitemClass = SpecactorMethod

        elif self.type == "enumeration":
            ttypeId = "enumeration"
            spec = SpecEnum(self.name, self.parser.path, self.startline)
            spec.actorname = self.actorname
            currentitemClass = None

        elif self.type == "model" or self.type == "rootmodel":
            ttypeId = "prop"
            spec = SpecModel(self.name, self.descr, self.tags,
                             self.parser.path, self.startline)
            spec.actorname = self.actorname
            spec.appname = self.appname
            spec.name = self.name
            if self.type == "rootmodel":
                spec.rootobject = True
            # print "found model %s %s"%(self.name,self.parser.path)
            # print self.content
            # print "###########"
            currentitemClass = SpecModelProperty
        else:
            return self.parser.raiseError(
                "Invalid type '%s' could not find right type of spec doc, only supported model,actor,enum :" %
                self.type, self.content, self.startline)

        # find the items in the block
        linenr = self.startline
        state = "start"
        currentitemContent = ""
        currentitem = None
        if self.type == "enumeration":
            currentitemContent = self.content
            self.content = ""
            currentitem = spec

        for line in self.content.split("\n"):
            linenr += 1
            line = line.rstrip()
            # print "line:%s state:%s" % (line,state)
            if line.strip() == "":
                if currentitem is not None and currentitemContent == "":
                    currentitem.linenr = linenr + 1
                continue
            if state == "description" and line.strip().find("\"\"\"") == 0:
                # end of description
                state = "blockfound"
                currentitem.linenr = linenr + 1
                continue

            if state == "description":
                currentitem.description += "%s\n" % line.strip()

            if (state == "start" or state == "blockfound") and line.strip().find("\"\"\"") == 0:
                # found description
                state = "description"
                continue

            if state == "blockfound" and line.strip().find("@") == 0:
                # found labels tags on right level
                tmp1, currentitem.tags, tmp2 = self.parser.getTagsComment(line)
                currentitem.linenr = linenr + 1
                continue

            if state == "blockfound" and line[0] == " ":
                # we are in block & no block descr
                currentitemContent += "%s\n" % line

            if (state == "start" or state == "blockfound") and line[0] != " " and line.find(":") != -1:
                typeOnLine = line.split(":", 1)[0].strip()
                if ttypeId == typeOnLine:
                    state = "blockfound"
                    if currentitemContent != "":
                        currentitem._parse(self.parser, currentitemContent)
                        currentitemContent = ""
                    currentitem = currentitemClass(linenr)

                    comment, tags, line = self.parser.getTagsComment(line)
                    currentitem._parseFirstLine(
                        self.parser, line.split(":", 1)[1].strip())
                    if comment != "":
                        currentitem.comment = comment
                    if tags != "":
                        currentitem.tags = tags
                    spec._addItem(currentitem)
                    currentitemContent = ""
                else:
                    self.parser.raiseError("Found item %s, only %s supported." % (
                        typeOnLine, ttypeId), line, linenr)

        # are at end of file make sure last item is processed
        if currentitemContent != "":
            currentitem._parse(self.parser, currentitemContent)
        # spec.appname=self.appname
        # spec.actorname=self.actorname
        spec.type = self.type
        spec.addDefaults()

        j.portal.tools.specparser.specparserfactory.addSpec(spec)

    def __str__(self):
        s = "name:%s\n" % self.name
        s += "type:%s\n" % self.type
        s += "descr:%s\n" % self.descr
        s += "tags:%s\n" % self.tags
        s += "content:\n%s\n" % self.content
        return s

    __repr__ = __str__


class SpecDirParser:

    def __init__(self, path, appname, actorname):
        self.appname = appname
        self.actorname = actorname
        self.path = path

        files = j.sal.fs.listFilesInDir(self.path, True, "*.spec")

        def sortFilesFollowingLength(files):
            r = {}
            result = []
            for item in ["actor", "enum", "model"]:
                for p in files:
                    pp = j.sal.fs.getBaseName(p)
                    if pp.find(item) == 0:
                        result.append(p)
                        files.pop(files.index(p))

            for p in files:
                if len(p) not in r:
                    r[len(p)] = []
                r[len(p)].append(p)
            lkeysSorted = sorted(r.keys())
            for lkey in lkeysSorted:
                result = result + r[lkey]
            return result

        files = sortFilesFollowingLength(files)

        self.specblocks = {}
        for path in files:
            if j.sal.fs.getBaseName(path).find("example__") == 0:
                continue
            parser = j.portal.tools.specparser.specparserfactory._getSpecFileParser(
                path, self.appname, self.actorname)

            for key in list(parser.specblocks.keys()):
                block = parser.specblocks[key]
                self.specblocks[block.type + "_" + block.name] = block

    def getSpecBlock(self, type, name):
        key = type + "_" + name
        if key in self.specblocks:
            return self.specblocks[key]
        else:
            return False

    def __str__(self):
        s = "path:%s\n" % self.path
        for key in list(self.specblocks.keys()):
            block = self.specblocks[key]
            s += "%s\n\n" % block

        return s

    __repr__ = __str__


class SpecFileParser:

    def __init__(self, path, appname, actorname):
        """
        find blocks in file
        """
        self.path = path
        self.appname = appname
        self.actorname = actorname
        if self.appname != self.appname.lower().strip():
            emsg = "appname %s for specs should be lowercase & no spaces" % self.appname
            raise j.exceptions.RuntimeError(
                emsg + " {category:spec.nameerror}")
        self.contentin = j.sal.fs.fileGetContents(path)
        self.contentout = ""
        self.specblocks = {}  # key is name
        state = "start"
        # a block starts with [...] and ends with next [] or end of file
        state = "start"
        linenr = 0
        currentblock = None
        # content=self.contentin+"\n***END***\n"
        for line in self.contentin.split("\n"):
            linenr += 1
            line = line.rstrip()
            # remove empty lines
            line = line.replace("\t", "    ")
            if line.strip() == "" or line.strip()[0] == "#":
                if currentblock is not None and currentblock.content == "":
                    currentblock.startline = linenr + 1
                continue
            # remove comments from line
            # if line.find("#")>0:
                # line=line.split("#",1)[0]

            if state == "blockfound" and line[0] == "[":
                # block ended
                state = "start"

            if state == "blockdescription" and line.strip().find("\"\"\"") == 0:
                # end of description
                state = "blockfound"
                self.contentout += "%s\n" % line
                currentblock.startline = linenr + 2
                continue

            if state == "blockdescription":
                currentblock.descr += "%s\n" % line.strip()

            if state == "blockfound" and line.strip().find("\"\"\"") == 0 and currentblock.descr == "":
                # found description
                state = "blockdescription"
                self.contentout += "%s\n" % line
                continue

            # if state=="blockfound" and self._checkIdentation(line,linenr,1,1) and line.strip().find("@") != -1:
                # found labels tags on right level
                # if currentblock is not None:
                # comments,currentblock.tags,tmp=self.getTagsComment(line)
                # currentblock.startline=linenr
                # else:
                #self.raiseError("Cannot find label & tags when there is no specblock opened [...]",line,linenr)
                #self.contentout+="%s\n" % line
                # continue

            if state == "blockfound":
                # we are in block & no block descr
                currentblock.content += "%s\n" % line

            if state == "start" and line[0] == "[":
                state = "blockfound"
                # line2=line
                # if line2.find("#")>0:
                #from JumpScale9Lib.core.Shell import ipshellDebug,ipshell
                # print "DEBUG NOW jjj"
                # ipshell()

                # line2=line.split("#",1)[0]
                currentblock = SpecBlock(
                    self, line, linenr + 1, appname=self.appname, actorname=self.actorname)

                self.specblocks[currentblock.name] = currentblock

            self.contentout += "%s\n" % line

        for key in list(self.specblocks.keys()):
            block = self.specblocks[key]
            block.parse()
            # print block.name

    def getTagsComment(self, line):
        """
        return comment,tags,line
        """
        if line.find("#") != -1:
            comment = line.split("#", 1)[1]
            line = line.split("#", 1)[0]
        else:
            comment = ""
        tags = None
        if line.find("@") != -1:
            tags = line.split("@", 1)[1]
            line = line.split("@", 1)[0]
        if comment.find("@") != -1:
            tags = comment.split("@", 1)[1]
            comment = comment.split("@")[0]

        if comment is not None:
            comment = comment.strip()

        if tags is not None:
            tags = tags.strip()

        return comment, tags, line

    def deIndent(self, content, startline):
        # remove garbage & fix identation
        content2 = ""
        linenr = startline
        for line in content.split("\n"):
            linenr += 1
            if line.strip() == "":
                continue
            else:
                if line.find("    ") != 0:
                    return self.raiseError("identation error.", line, linenr)
                content2 += "%s\n" % line[4:]
        return content2

    def _checkIdentation(self, line, linenr, minLevel=1, maxLevel=1):
        """
        """
        line = line.replace("\t", "    ")
        ok = True
        if(len(line) < maxLevel * 4):
            self.raiseError(
                "line is too small, there should be max identation of %s" % maxLevel, line, linenr)
        for i in range(0, minLevel):
            if line[i * 4:(i + 1) * 4] != "    ":
                ok = False
        if line[maxLevel * 4 + 1] == " ":
            ok = False
        return ok

    def raiseError(self, msg, line="", linenr=0):
        raise j.exceptions.Input("Cannot parse file %s\nError on line:%s\n%s\n%s\n" % (
            self.path, linenr, line, msg), "specparser.input")


class Role(ClassBase):

    def __init__(self, name, actors=[]):
        self.actors = actors
        self.name = name


class PortalSpecParserFactory:

    def __init__(self):
        self.specs = {}
        self.childspecs = {}
        self.appnames = []
        self.actornames = []
        self.app_actornames = {}
        self.modelnames = {}  # key = appname_actorname
        self.roles = {}  # key is appname_rolename
        #self.codepath=j.sal.fs.joinPaths( j.dirs.VARDIR,"actorscode")

    def getEnumerationSpec(self, app, actorname, name, die=True):
        key = "enumeration_%s_%s_%s" % (app, actorname, name)
        if key in self.specs:
            return self.specs[key]
        else:
            if die:
                emsg = "Cannot find enumeration with name %s for app %s" % (
                    name, app)
                raise j.exceptions.RuntimeError(
                    emsg + " {category:specs.enumeration.notfound}")
            else:
                return False

    def getactorSpec(self, app, name, raiseError=True):
        key = "actor_%s_%s_%s" % (app, name, "")
        if key in self.specs:
            return self.specs[key]
        else:
            if raiseError:
                raise j.exceptions.RuntimeError("Cannot find actor with name %s for app %s" % (
                    name, app) + " {category:specs.actor.notfound}")
            else:
                return None

    def getModelSpec(self, app, actorname, name, die=True):
        key = "model_%s_%s_%s" % (app, actorname, name)
        key = key.lower()
        if key in self.specs:
            return self.specs[key]
        else:
            if die:
                emsg = "Cannot find model with name %s for app %s" % (
                    name, app)
                raise j.exceptions.RuntimeError(
                    emsg + " {category:specs.model.notfound}")
            else:
                return False

    def getChildModelSpec(self, app, actorname, name, die=True):
        key = "childmodel_%s_%s_%s" % (app, actorname, name)
        key = key.lower()
        if key in self.childspecs:
            return self.childspecs[key]
        else:
            if die:
                emsg = "Cannot find model with name %s for app %s" % (
                    name, app)
                raise j.exceptions.RuntimeError(
                    emsg + " {category:specs.model.notfound}")
            else:
                return False

    def getModelNames(self, appname, actorname):
        key = "%s_%s" % (appname, actorname)
        if key in j.portal.tools.specparser.specparserfactory.modelnames:
            return self.modelnames[key]
        else:
            return []

    def addSpec(self, spec):
        if spec.name == spec.actorname:
            specname = ""
        else:
            specname = spec.name

        if spec.type == "rootmodel":
            if spec.type == "rootmodel":
                spec.type = "model"
                key = "%s_%s" % (spec.appname, spec.actorname)
                if key not in self.modelnames:
                    self.modelnames[key] = []
                if spec.name not in self.modelnames[key]:
                    self.modelnames[key].append(spec.name)
        elif spec.type == "model":
            k = "%s_%s_%s_%s" % ("childmodel", spec.appname,
                                 spec.actorname, specname)
            self.childspecs[k] = spec

        if spec.type == "actor" and specname != "":
            print(
                "DEBUG NOW addSpec in specparser, cannot have actor with specname != empty")

        key = "%s_%s_%s_%s" % (spec.type, spec.appname,
                               spec.actorname, specname)

        if spec.type != spec.type.lower().strip():
            emsg = "type %s of spec %s should be lowercase & no spaces" % (
                spec.type, key)
            # TODO: P2 the errorcondition handler does not deal with this format to escalate categories
            raise j.exceptions.RuntimeError(emsg + " {category:specs.input}")
        if spec.name != spec.name.lower().strip():
            emsg = "name %s of spec %s should be lowercase & no spaces" % (
                spec.name, key)
            raise j.exceptions.RuntimeError(emsg + " {category:specs.input}")

        if spec.appname not in self.appnames:
            self.appnames.append(spec.appname)

        if spec.actorname == "":
            emsg = "actorname cannot be empty for spec:%s" % (spec.name)
            raise j.exceptions.RuntimeError(emsg + "\n{category:specs.input}")
        if "%s_%s" % (spec.appname, spec.actorname) not in self.actornames:
            self.actornames.append("%s_%s" % (spec.appname, spec.actorname))

        self.specs[key] = spec

    def findSpec(self, query="", appname="", actorname="", specname="", type="", findFromSpec=None, findOnlyOne=True):
        """
        do not specify query with one of the other filter criteria
        @param query is in dot notation e.g. $appname.$actorname.$modelname ... the items in front are optional
        """
        # print "findspec: '%s/%s/%s'"%(appname,actorname,specname)
        # print "query:'%s'"%query
        spec = findFromSpec
        if query != "":
            type = ""
            if query[0] == "E":
                type = "enumeration"
            if query[0] == "M":
                type = "model"
            if query.find("(") != -1 and query.find(")") != -1:
                query = query.split("(", 1)[1]
                query = query.split(")")[0]
            splitted = query.split(".")

            # see if we can find an appname
            appname = ""
            if len(splitted) > 1:
                possibleappname = splitted[0]
                if possibleappname in j.portal.tools.specparser.specparserfactory.appnames:
                    appname = possibleappname
                    splitted = splitted[1:]  # remove the already matched item

            # see if we can find an actor
            actorname = ""
            if len(splitted) > 1:
                possibleactor = splitted[0]
                if possibleactor in j.portal.tools.specparser.specparserfactory.actornames:
                    actorname = possibleactor
                    splitted = splitted[1:]  # remove the already matched item

            query = ".".join(splitted)
            if query.strip() != "." and query.strip() != "":
                specname = query

            if actorname == "" and spec is not None:
                # no specificiation of actor or app so needs to be local to
                # this spec
                actorname = spec.actorname

            if appname == "" and spec is not None:
                # no specificiation of actor or app so needs to be local to
                # this spec
                appname = spec.appname

        result = []

        if actorname == specname:
            specname = ""
        else:
            specname = specname

        if actorname != "" and appname != "" and specname != "" and type != "":
            key = "%s_%s_%s_%s" % (type, appname, actorname, specname)
            if key in j.portal.tools.specparser.specparserfactory.specs:
                result = [j.portal.tools.specparser.specparserfactory.specs[key]]
        else:
            # not enough specified need to walk over all
            for key in list(j.portal.tools.specparser.specparserfactory.specs.keys()):
                spec = j.portal.tools.specparser.specparserfactory.specs[key]
                found = True
                if actorname != "" and spec.actorname != actorname:
                    found = False
                if appname != "" and spec.appname != appname:
                    found = False
                if specname != "" and spec.name != specname:
                    found = False
                if type != "" and spec.type != type:
                    found = False
                if found:
                    result.append(spec)

        # print 'actorname:%s'%actorname

        if len(result) == 0:
            if spec is not None:
                emsg = "Could not find spec with query:%s appname:%s actorname:%s name:%s (spec info: '%s'_'%s'_'%s')" % (
                    query, appname, actorname, specname, spec.name, spec.specpath, spec.linenr)
            else:
                emsg = "Could not find spec with query:'%s' appname:'%s' actorname:'%s' name:'%s' " % \
                    (query, appname, actorname, specname)
            raise j.exceptions.RuntimeError(
                emsg + " {category:specs.finderror}")

        if findOnlyOne:
            if len(result) != 1:
                if spec is not None:
                    emsg = "Found more than 1 spec for search query:%s appname:%s actorname:%s name:%s (spec info: %s_%s_%s)" % (
                        query, appname, actorname, specname, spec.name, spec.specpath, spec.linenr)
                else:
                    emsg = "Found more than 1 spec for search query:%s appname:%s actorname:%s name:%s " % \
                        (query, appname, actorname, specname)
                raise j.exceptions.RuntimeError(
                    emsg + " {category:specs.finderror}")
            else:
                result = result[0]

        return result

    def _getSpecFileParser(self, path, appname, actorname):
        return SpecFileParser(path, appname, actorname)

    def init(self):
        self.__init__()

    def removeSpecsForactor(self, appname, actorname):
        appname = appname.lower()
        actorname = actorname.lower()
        if appname in self.appnames:
            i = self.appnames.index(appname)
            self.appnames.pop(i)
        key = "%s_%s" % (appname, actorname)
        if key in self.actornames:
            # found actor remove the specs
            for key2 in list(self.specs.keys()):
                type, app, item, remaining = key2.split("_", 3)
                if app == appname and item.find(actorname) == 0:
                    print(("remove specs %s from memory" % key))
                    self.specs.pop(key2)
            i = self.actornames.index(key)
            self.actornames.pop(i)

    def resetMemNonSystem(self):
        self.appnames = ["system"]
        for key2 in list(self.specs.keys()):
            type, app, item, remaining = key2.split("_", 3)
            if app != "system":
                self.specs.pop(key2)
        for key in self.actornames:
            appname, actorname = key.split("_", 1)
            if appname != "system":
                i = self.actornames.index(key)
                self.actornames.pop(i)

    def parseSpecs(self, specpath, appname, actorname):
        """
        @param specpath if empty will look for path specs in current dir
        """
        if not j.sal.fs.exists(specpath):
            raise j.exceptions.RuntimeError(
                "Cannot find specs on path %s" % specpath)

        SpecDirParser(specpath, appname, actorname=actorname)
        # generate specs for model actors
        # smg=SpecModelactorsGenerator(appname,actorname,specpath)
        # smg.generate()

        # parse again to include the just generated specs
        # SpecDirParser(specpath,appname,actorname=actorname)

    def getSpecFromTypeStr(self, appname, actorname, typestr):
        """
        @param typestr e.g list(machine.status)
        @return $returntype,$spec  $returntype=list,dict,object,enum (list & dict can be of primitive types or objects (NOT enums))
        """
        if typestr in ["int", "str", "float", "bool"]:
            return None, None
        elif typestr.find("list") == 0 or typestr.find("dict") == 0:
            if typestr.find("list") == 0:
                returntype = "list"
            else:
                returntype = "dict"
            typestr = typestr.split("(")[1]
            typestr = typestr.split(")")[0]
            # print "typestr:%s" % typestr
        else:
            returntype = "object"

        if typestr in ["int", "str", "float", "bool", "list", "dict"]:
            spec = typestr
        else:
            result = self.getEnumerationSpec(
                appname, actorname, typestr, die=False)
            if result is False:
                result = self.getModelSpec(
                    appname, actorname, typestr, die=False)
            if result is False:
                if returntype not in ["list", "dict"]:
                    returntype = "enum"
            if result is False:
                raise j.exceptions.RuntimeError(
                    "Cannot find spec for app:%s, actor:%s, with typestr:%s" % (appname, actorname, typestr))
            else:
                spec = result
        return returntype, spec

        #raise j.exceptions.RuntimeError("Could not find type:%s in getSpecFromTypeStr" % type)

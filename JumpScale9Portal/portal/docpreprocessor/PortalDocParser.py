from js9 import j
import re


class PortalDocParser():

    def parseDoc(self, doc):
        content = doc.content
        # TODO: this is badly written can be done by some easy regex, is not performing like this
        content, doc.name = self._findItem(content, "@@name")
        content, aliasstr = self._findItem(content, "@@alias")
        doc.alias = [item.lower().strip() for item in aliasstr.split(",")]
        content, authorstr = self._findItem(content, "@@author")
        doc.author = [item.lower().strip() for item in authorstr.split(",")]
        content, doc.type = self._findItem(content, "@@type")
        content, doc.pagename = self._findItem(content, "@@pagename")
        content, doc.title = self._findItem(content, "@@title", removecolon=False)
        content, requiredargs = self._findItem(content, "@@requiredargs")
        doc.requiredargs = requiredargs.split()
        if doc.title == "":
            doc.title = j.sal.fs.getBaseName(doc.path).replace(".wiki", "")
        content, order = self._findItem(content, "@@order")
        if order != "":
            doc.order = int(order)
        content, prodstr = self._findItem(content, "@@product")
        doc.products = [item.lower().strip() for item in prodstr.split(",")]
        content, visibility = self._findItem(content, "@@visibility")
        if visibility != "":
            doc.visibility = [item.lower().strip() for item in visibility.split(",")]
        doc.name = doc.name.lower()
        if doc.name == "":
            doc.name = j.sal.fs.getBaseName(doc.shortpath).replace(".wiki", "").lower().strip()
        if doc.pagename == "":
            doc.pagename = doc.name
        content, parent = self._findItem(content, "@@parent")
        if parent.strip() != "":
            doc.parent = parent
        content, generate = self._findItem(content, "@@generate")
        if generate == "0":
            doc.generate = False

        content, tags = self._findItem(content, item="@@", maxitems=100, removecolon=False)
        tags2 = ""
        for tag in tags:
            if tag.find(":") != -1:
                items = tag.split(":")
                tags2 += " %s:%s" % (items[0].strip(), items[1].strip())
        doc.tags = tags2.strip()

    def _findItem(self, text, item="@owner", maxitems=1, removecolon=True, lower=True):
        result = []

        def process(arg, line):
            line = re.sub(item.lower(), "", line, flags=re.IGNORECASE)
            if line.find("##") == 0:
                line = ""
            if line.find("##") != -1:
                line = line.split("##")[0]
            if removecolon:
                line = line.replace(":", "").strip()
            else:
                line = line.strip()
            result.append(line)
            return False
        text2 = j.tools.code.regex.replaceLines(process, arg="", text=text, includes=["%s.*" % item], excludes='')
        if len(result) > maxitems:
            self.errorTrap("Error in text to parse, found more entities:%s than %s" % (item, maxitems))
        if maxitems == 1:
            if len(result) > 0:
                result = result[0]
            else:
                result = ""
        return text2, result,

    def _findLine(self, text, item="@owner"):
        for line in text.split("\n"):
            if line.strip().lower().find(item) == 0:
                return line
        return ""

    def _findId(self, text, path):
        result = j.tools.code.regex.findAll("\(\(.*: *\d* *\)\)", text)

        if len(result) > 1:
            raise RuntimeError("Found 2 id's in %s" % path)
        if len(result) == 1:
            result = result[0].split(":")[1]
            result = result.split(")")[0]
        else:
            result = ""
        if result.strip() == "":
            result = 0
        else:
            try:
                result = int(result)
            except Exception as e:
                raise RuntimeError("Could not parse if, error:%s. \nPath = %s" % (e, path))

        return text, result

    def _parseTimeInfo(self, timestring, modelobj, defaults=[8, 16, 8, 4, 8]):
        # print "timestring: %s" % timestring
        timeItems = timestring.split("/")
        modelobj.time_architecture = defaults[0]
        modelobj.time_coding = defaults[1]
        modelobj.time_integration = defaults[2]
        modelobj.time_doc = defaults[3]
        modelobj.time_testing = defaults[4]
        modelobj.timestr = timestring
        modelobj.time = 0
        for item in timeItems:
            if item != "":
                if item.lower()[0] == "a":
                    modelobj.time_architecture = int(item.lower().replace("a", ""))
                    modelobj.time += modelobj.time_architecture
                if item.lower()[0] == "c":
                    modelobj.time_coding = int(item.lower().replace("c", ""))
                    modelobj.time += modelobj.time_coding
                if item.lower()[0] == "i":
                    modelobj.time_integration = int(item.lower().replace("i", ""))
                    modelobj.time += modelobj.time_integration
                if item.lower()[0] == "d":
                    modelobj.time_doc = int(item.lower().replace("d", ""))
                    modelobj.time += modelobj.time_doc
                if item.lower()[0] == "t":
                    modelobj.time_testing = int(item.lower().replace("t", ""))
                    modelobj.time += modelobj.time_testing

    def _parseTaskInfo(self, storyTaskModelObject, info):
        for item in info.split(" "):
            if item != "":
                if item.lower()[0] == "s":
                    # story
                    storyTaskModelObject.storyid = int(item.lower().replace("s", ""))
                elif item.lower()[0] == "p":
                    # priority
                    storyTaskModelObject.priority = int(item.lower().replace("p", ""))
                elif item.lower()[0] == "m":
                    # sprint
                    storyTaskModelObject.sprintid = int(item.lower().replace("m", ""))

    def _parseStoryInfo(self, storyTaskModelObject, info):
        for item in info.split(" "):
            if item != "":
                if item.lower()[0] == "s":
                    # story
                    storyTaskModelObject.id = int(item.lower().replace("s", ""))
                elif item.lower()[0] == "p":
                    # priority
                    storyTaskModelObject.priority = int(item.lower().replace("p", ""))
                elif item.lower()[0] == "m":
                    # sprint
                    storyTaskModelObject.sprintid = int(item.lower().replace("m", ""))

    def _parseTaskQuestionRemark(self, text):
        """
        @return [infotext,timetext,user,group,descr]
        """
        keys = ["P", "p", "S", "s", "M", "m"]
        timeitem = ""
        infoitems = ""
        descr = ""
        state = "start"
        user = ""
        group = ""
        # print "parse task: %s" % text
        text = text.replace("  ", " ")
        text = text.replace("  ", " ")
        if text.strip() == "":
            return ["", "", "", "", ""]
        for item in text.strip().split(" "):
            # print "item:  %s" % item
            if state == "endofmeta":
                descr += item + " "
            if state == "start":
                if item[0] in keys:
                    try:
                        int(item[1:])
                        infoitems += item + " "
                    except:
                        descr += item + " "
                        state = "endofmeta"
                elif item[0:2].lower() == "t:":
                    timeitem = item[2:]
                    if not re.match(r"[aAcCiIdDtT/\d:]*\Z", timeitem):
                        descr += item + " "
                        state = "endofmeta"
                        timeitem = ""
                        #raise RuntimeError("Time item match failed for text %s" % text)
                elif item.find(":") != -1:
                    # found user or group
                    if not j.tools.code.regex.match("\w*:\w*", item):
                        descr += item + " "
                        state = "endofmeta"
                    elif user == "":
                        splitted = item.split(":")
                        user = splitted[0]
                        group = splitted[1]
                        # TODO: P2 user & group can be comma separated build support for it in below coFde
                        if self.getUserMainId(group) != False:
                            # probably user & group reversed
                            group2 = user
                            user = group
                            group = group2
                        if self.getUserMainId(user) != False:
                            user = self.getUserMainId(user)  # to get aliasesin order
                else:
                    descr += item + " "
                    state = "endofmeta"
        return [infoitems, timeitem, user, group, descr]

    def _getStoryName(self, info):
        out = ""
        for item in info.split(" "):
            if not(item.lower()[0] == "s" or item.lower()[0] == "p" or item.lower()[0] == "m"):
                out += " %s" % item
        return out.strip()

    def _strToArrayInt(self, items):
        if items == "":
            return []
        result = ""
        for item in items.split(","):
            try:
                result.append(int(item))
            except:
                raise RuntimeError("Cannot convert str to array, item was %s" % item)
        return result

    def _strToInt(self, item):
        if item == "":
            return 0
        try:
            result = int(item)
        except:
            raise RuntimeError("Cannot convert str to int, item was %s" % item)
        return result

    def _normalizeDescr(self, text):
        text = text.lower()
        splitat = ["{", "(", "[", "#", "%", "$", "'"]
        for tosplit in splitat:
            if len(text.split(tosplit)) > 0:
                text = text.split(tosplit)[0]
        text = text.replace(",", "")
        text = text.replace(":", "")
        text = text.replace(";", "")
        text = text.replace("  ", " ")
        if text != "" and text[-1] == " ":
            text = text[:-1]
        text = text.replace("-", "")
        text = text.replace("_", "")
        return text

    def shortenDescr(self, text, maxnrchars=60):
        return j.tools.code.textToTitle(text, maxnrchars)

    def _getLinesAround(self, path, tofind, nrabove, nrbelow):
        text = j.sal.fs.fileGetContents(path)
        nr = 0
        lines = text.split("\n")
        for line in lines:
            if line.find(tofind) != -1:
                if nr - nrabove < 0:
                    nrstart = 0
                else:
                    nrstart = nr - nrabove
                if nr + nrabove > len(lines):
                    nrstop = len(lines)
                else:
                    nrstop = nr + nrabove
                return "\n".join(lines[nrstart:nrstop])
            nr += 1
        return ""

    def addUniqueId(self, line, fullPath, ttype="sprint"):
        line, id1 = self._findId(line, fullPath)
        if id1 == 0:
            # create unique id and put it in the file
            id1 = j.base.idpreprocessor.generateIncrID("%sid" % ttype, self.service)
            # tfe=j.tools.code.getTextFileEditor(fullPath)
            #tfe.addItemToFoundLineOnlyOnce(line," ((%s:%s))"%(ttype,id1),"\(id *: *\d* *\)",reset=True)
            tfe = j.tools.code.getTextFileEditor(fullPath)
            tfe.addItemToFoundLineOnlyOnce(line, " ((%s:%s))" % (ttype, id1), "\(+.*: *\d* *\)+", reset=self.reset)
        return id1

    def _findTasks(self, text, path, fullPath):
        # TODO: S2 do same for remarks & questions
        def findTodoVariants(line):
            variants = ["@todo:", "@todo :", "@todo"]
            for variant in variants:
                if line.strip().find(variant) == 0:
                    return variant
        if text.lower().find("@todo") != -1:
            lines = j.tools.code.regex.findAll("@todo.*", text)
            for line in lines:
                self.addUniqueId(line, fullPath, ttype="todo")
                line, id1 = self._findId(line, fullPath)
                todostatement = findTodoVariants(line)
                line1 = line.replace(todostatement, "")
                infotext, timetext, user, group, descr = self._parseTaskQuestionRemark(line1)

                obj = self.projectInfoObject.tasks.addTask(id=id1, descr=descr.strip())
                obj.model.storyid = 0
                obj.model.users = user
                obj.model.group = group
                obj.model.path = fullPath
                obj.model.context = self._getLinesAround(fullPath, line, 10, 20)

                obj.model.descrshort = self.shortenDescr(descr)
                # print "infotext:%s" % infotext
                self._parseTaskInfo(obj.model, infotext)
                self._parseTimeInfo(timetext, obj.model, defaults=[0, 1, 0, 1, 0])
                if obj.model.storyid == 0:
                    obj.model.storyid = 999  # 999 is the unsorted story card

    def errorTrap(self, msg):
        if msg not in self._errors:
            self._errors.append(msg)
            j.tools.console.echo("ERROR: %s" % msg)

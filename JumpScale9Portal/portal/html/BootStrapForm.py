import copy
from js9 import j


class BootStrapForm:

    def __init__(self, page):
        self.page = page

    # def getFormForModel(self,appname,actorname,modelname,guid):
    #     from JumpScale.core.Shell import ipshellDebug,ipshell
    #     print "DEBUG NOW getFormForModel"
    #     ipshell()

    def getForm(self, name="", actor=None):
        """
        actor is required if you want to remember position of e.g. a specific object property to a form name

        how to use:
        actor=j.apps.system.usermanager

        user=actor.model_user_new()
        user.name="removeme"
        guid=actor.model_user_set(user)

        modifier=j.portal.tools.html.getPageModifierBootstrapForm(page)
        form=modifier.getForm(actor=actor)
        form.addTextInput("name",reference=form.getReference(user,"name"),default="",help="")
        # form.addTextInput("name",reference=form.getReference(user,"name"),default="",help="")
        params.page=modifier.addForm(form)

        """
        return Form(name, actor)

    def addForm(self, form, postBackUrl=""):
        """
        actor is required if you want to remember position of e.g. a specific object property to a form name

        if postBackUrl=="" then will be /wiki/model_$appname_$actorname/$modelname/set
        the post is done by using all args & the caching key (under cachekey)
        get params will be:
         - cachekey
        """

        if postBackUrl == "":
            if len(list(form.references.objects.keys())) == 1:
                okey = list(form.references.objects.keys())[0]
                osis = form.references.objects[okey]
                postBackUrl = "/restmachine/system/contentmanager/modelobjectupdate?appname=%s&actorname=%s&key=%s" %\
                    (form.actor.appname, form.actor.actorname, form.references.id)

        if postBackUrl != "":
            # add postback button
            form.addSaveButton(postBackUrl)

        form.references.save()

        self.page.addMessage(str(form))
        return self.page


class References():

    def __init__(self, actor):
        self.refs = {}
        self.db = actor.dbmem
        self.id = j.data.idgenerator.generateGUID()
        self.counter = 0
        self.objects = {}

    def getNextId(self):
        self.counter += 1
        return self.counter

    def addReference(self, obj, reference):
        key = "%s__%s__%s__%s" % (obj._meta[0], obj._meta[1], obj._meta[2], obj.guid)
        if key not in self.objects:
            self.objects[key] = obj
        id = self.getNextId()
        self.refs[id] = [key, reference]
        default = eval("obj.%s" % reference)
        return (id, default)

    def save(self):
        self.db.cacheSet("form_%s" % self.id, [self.objects, self.refs], expirationInSecondsFromNow=600)
        return self.id


from js9 import j


class Form:

    def __init__(self, formname="", actor=None):
        self.references = References(actor)
        self.closeStatements = []
        self.actor = actor
        self.lastId = 0
        self.content = """
<form id="$formname" class="form-horizontal" method="post" action="$postBackUrl">
<fieldset>
<div id="legend" class="">
    <legend class="">$formname</legend>
</div>
"""
        self.content = self.content.replace("$formname", formname)
        self.content = self.content.replace("$formname", formname)
        self.closeStatements.append("</form>")
        self.closeStatements.append("</fieldset>")

    def getReference(self, obj, reference):
        """
        example:
        user=j.apps.system.usermanager.model_user_new()
        getReference(user,"name")
        getReference(user,"contacts[1].tel") #means in list first element with property tel
        """
        return self.references.addReference(obj, reference)

    def _addDefault(self, inputt, label, name="", reference=None, default="", help="", classs=""):
        """
        @param reference use self.getReference(...)
        """
        C = """
<div class="control-group">
<label class="control-label" for="$name">$label</label>
<div class="controls">
  $input
  $help
</div>
</div>
"""
        if reference is not None:
            reference, default = reference
            name = "ref_%s" % reference

        if name == "":
            name = label

        if help != "":
            C = C.replace("$help", "<p class=\"help-block\">%s</p>" % help)
        else:
            C = C.replace("$help\n", "")
        C = C.replace("$input", inputt)
        C = C.replace("$name", name)
        C = C.replace("$label", label)
        C = C.replace("$default", str(default))
        if classs != "":
            C = C.replace("$classs", " class=\"%s\"" % classs)
        else:
            C = C.replace("$classs", "")

        if default != "":
            C = C.replace("$default", "placeholder=\"%s\"" % default)
        return C

    def addTextInput(self, label, name="", reference=None, default="", help="", classs="input-xlarge"):
        C = """<input id="$name" name="$name" type="text" placeholder="$default" $classs>\n"""
        self.content += self._addDefault(C, label, name, reference, default, help, classs=classs)

    def addSelectFromList(self, label, llist, multiple=False, name="",
                          reference=None, default="", help="", classs="input=xlarge"):
        c = ""
        if multiple:
            c += "<select multiple=\"multiple\" $class >\n"
        else:
            c += "<select class=\"%s\" >\n" % classs
        for item in llist:
            c += "<option>%s</option>\n" % item
        c += "</select>\n"
        self.content += self._addDefault(c, label, name, reference, default, help)

    def addSaveButton(self, postBackUrl):
        C = """
<div class="form-actions">
    <button type="submit" class="btn btn-primary">Save changes</button>
</div>"""
        self.content = self.content.replace("$postBackUrl", postBackUrl)
        self.content += C

    def __str__(self):
        closeStatements = copy.copy(self.closeStatements)
        closeStatements.reverse()
        c = copy.copy(self.content)

        for item in closeStatements:
            c += "%s\n" % item

        return c

    __repr__ = __str__

from js9 import j


class SpecModelactorsGenerator:

    def __init__(self, appname, actorname, specpath, typecheck=True, dieInGenCode=True):
        self.content = ""
        self.typecheck = typecheck
        self.die = dieInGenCode
        self.appname = appname
        self.actorname = actorname
        self.specpath = specpath

    def descrTo1Line(self, descr):
        if descr == "":
            return descr
        descr = descr.strip()
        descr = descr.replace("\n", "\\n")
        return descr

    def addModel(self, modelname, actorname, spec):
        s = """
[actor]
	\"\"\"
	is actor to manipulate JSModel {name}
	\"\"\"
	method:model_{name}_delete
		\"\"\"
		remove the model {name} with specified id and optionally guid
        if secret key is given then guid is not needed, other guid is authentication key
		\"\"\"
        @tasklettemplate:modeldelete
		var:id int,None,Object identifier
        var:guid str,"",unique identifier can be used as auth key  @tags: optional
		result:bool    #True if successful, False otherwise

	method:model_{name}_get
		\"\"\"
		get model {name} with specified id and optionally guid
        if secret key is given then guid is not needed, other guid is authentication key
		\"\"\"
        @tasklettemplate:modelget
		var:id int,None,Object identifier
        var:guid str,"",unique identifier can be used as auth key  @tags: optional
        result:object

    method:model_{name}_new
        \"\"\"
        Create a new modelobject{name} instance and return as empty.
        A new object will be created and a new id & guid generated
        \"\"\"
        @tasklettemplate:modelnew
        result:object    #the JSModel object

	method:model_{name}_set
		\"\"\"
		Saves model {name} instance starting from an existing JSModel object (data is serialized as json dict if required e.g. over rest)
		\"\"\"
        @tasklettemplate:modelupdate
        var:data str,"",data is object to save
		result:bool    #True if successful, False otherwise

	method:model_{name}_find
		\"\"\"
		query to model {name}
        TODO: how to query
        example: name=aname
        secret key needs to be given
		\"\"\"
        @tasklettemplate:modelfind
		var:query str,"",unique identifier can be used as auth key
		result:list    #list of list [[$id,$guid,$relevantpropertynames...]]

    method:model_{name}_list
        \"\"\"
        list models, used by e.g. a datagrid
        \"\"\"
        @tasklettemplate:modellist novalidation
        result:json

    method:model_{name}_datatables
        \"\"\"
        list models, used by e.g. a datagrid
        \"\"\"
        @tasklettemplate:modeldatatables returnformat:jsonraw
        result:json


"""
        s = s.replace("{name}", modelname)
        s = s.replace("{actorname}", actorname)
        s += ('    method:model_{0}_create\n        \"\"\"\n        Create a new model\n        \"\"\"\n        @tasklettemplate:create\n'.format(modelname))
        for prop in spec.properties:
            if prop.type == 'int' and prop.name == 'id':
                continue
            default = "" if prop.default is None else prop.default
            s += ('        var:{0} {1},{3},{2}\n'.format(prop.name, prop.type,
                                                         prop.description, default))
        s += ('        result:json\n')
        self.content += s

    def generate(self):

        specnames = [item for item in list(j.portal.tools.specparser.specparserfactory.specs.keys()) if item.find(
            "model_%s_%s" % (self.appname, self.actorname)) == 0]

        for specname in specnames:
            print(("##generate %s" % specname))

            spec = j.portal.tools.specparser.specparserfactory.specs[specname]

            if spec.tags is not None and spec.tags.find("nocrud") != -1:
                # if no crud should be generated go to next
                continue

            if spec.rootobject:
                modelactorname = spec.name.replace(".", "_")
                modelactorname = "%s_model_%s" % (
                    spec.actorname, modelactorname)
                filename = modelactorname + ".spec"
                specpath = j.sal.fs.joinPaths(self.specpath, filename)

                j.sal.fs.createDir(j.sal.fs.getDirName(specpath))

                if j.sal.fs.exists(specpath):
                    content = j.sal.fs.fileGetContents(specpath)
                    if content.find("##DONOTGENERATE##") != -1:
                        specpath = j.sal.fs.joinPaths(
                            self.specpath, spec.name.lower(), "_modelactors.spec")

                self.addModel(spec.name, modelactorname, spec)

                j.sal.fs.writeFile(specpath, self.content)
                self.content = ""

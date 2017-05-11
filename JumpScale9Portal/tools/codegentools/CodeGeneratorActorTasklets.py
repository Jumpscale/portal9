from js9 import j

from .CodeGeneratorBase import CodeGeneratorBase

NOTGENSTR = "##DONOTGENERATE##"

tasklets = {}
tasklets["default"] = """
def main(j, params, service, tags, tasklet):
    params.result=None
    return params

def match(j, params, service, tags, tasklet):
    return True
"""


class CodeGeneratoractorTasklets(CodeGeneratorBase):

    def __init__(self, spec, typecheck=True, dieInGenCode=True, overwrite=False, codepath=None):
        overwrite = False  # can never overwrite
        CodeGeneratorBase.__init__(self, spec, typecheck, dieInGenCode)
        self.codepath = j.sal.fs.joinPaths(codepath, "methodtasklets")
        j.sal.fs.createDir(self.codepath)
        self.type = "tasklets"
        self.overwrite = overwrite

    def generate(self):
        spec = self.spec

        for method in self.spec.methods:

            path = j.sal.fs.joinPaths(self.codepath, "method_%s" % method.name)
            j.sal.fs.createDir(path)

            path = j.sal.fs.joinPaths(self.codepath, "method_%s" % method.name,
                                      "5_%s_%s.py" % (spec.actorname, method.name))

            path2 = j.sal.fs.joinPaths(
                self.codepath, "method_%s" % method.name, "5_main.py")
            if j.sal.fs.exists(path2):
                j.sal.fs.moveFile(path2, path)

            if j.sal.fs.exists(path):
                path = None

            if path is not None and str(path) != "":
                # lets also check there are no files in it yet

                if len(j.sal.fs.listFilesInDir(j.sal.fs.getDirName(path))) == 0:
                    templ = "default"
                    tags = j.data.tags.getObject(method.tags)
                    if tags.tagExists("tasklettemplate"):
                        templ = tags.tagGet("tasklettemplate").strip().lower()
                    if templ not in tasklets:
                        raise j.exceptions.RuntimeError(
                            "Cannot find tasklet template %s in \n%s" % (templ, method))
                    content = tasklets[templ]
                    if templ.find("model") == 0:  # is used for templates for crud methods
                        content = content.replace("{appname}", spec.appname)
                        content = content.replace(
                            "{actorname}", spec.actorname)
                        content = content.replace(
                            "{modelname}", method.name.split("_", 2)[1])
                    j.sal.fs.writeFile(path, content)

        return self.getContent()

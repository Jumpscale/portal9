from js9 import j
from collections import OrderedDict

PARAMMAP = {'string': 'str',
            'integer': 'int',
            'number': 'float',
            'array': 'list',
            'object': 'dict'}


class actorGen:

    def __init__(self, swagger):
        self.swagger = swagger

    def generate(self, destpath):
        template = self.swagger.jinjaEnv.get_template('actorspec.tmpl')
        paths = self.swagger.spec['paths']
        actors = dict()
        for path, pathinfo in list(paths.items()):
            parts = path.lstrip('/').split('/')
            if len(parts) != 3:
                print('Paths need to be of 3 exactly, skipping', path)
                continue
            appname, actorname, methodname = parts
            pathinfo['name'] = methodname
            actors.setdefault((appname, actorname), list()).append(pathinfo)

        for (appname, actorname), methods in list(actors.items()):
            actorfolder = j.sal.fs.joinPaths(destpath, "%s__%s" % (appname, actorname))
            specfolder = j.sal.fs.joinPaths(actorfolder, "specs")
            for folder in ('.actor', 'methodclass'):
                magicfolder = j.sal.fs.joinPaths(actorfolder, folder)
                j.sal.fs.createDir(magicfolder)
            j.sal.fs.createDir(specfolder)
            specfile = j.sal.fs.joinPaths(specfolder, 'actor.spec')
            output = template.render(methods=methods, parammap=PARAMMAP)
            j.sal.fs.writeFile(specfile, output)

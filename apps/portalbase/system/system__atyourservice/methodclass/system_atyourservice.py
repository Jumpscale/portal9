from js9 import j
from JumpScale.portal.portal import exceptions
from collections import OrderedDict
import requests
import json
import jwt


class system_atyourservice(j.tools.code.classGetBase()):

    """
    gateway to atyourservice
    """

    def __init__(self):
        # cockpit_cfg = j.portal.server.active.cfg.get('cockpit')
        # self.base_url = "http://{host}:{port}".format(**cockpit_cfg)
        self.base_url = "http://127.0.0.1:5000"
        self._cuisine = j.tools.cuisine.local

    def get_client(self, **kwargs):
        production = j.portal.server.active.cfg.get('production', True)
        production = j.data.text.getBool(production)
        if production:
            session = kwargs['ctx'].env['beaker.session']
            jwttoken = session.get('jwt_token')
            if jwttoken:
                claims = jwt.decode(jwttoken, verify=False)
                # if jwt expire, we fore reloading of client
                # new jwt will be created it needed.
                if j.data.time.epoch >= claims['exp']:
                    jwttoken = None

            if jwttoken is None:
                jwttoken = j.apps.system.oauthtoken.generateJwtToken(scope='', audience='', **kwargs)
                session['jwt_token'] = jwttoken
                session.save()
        else:
            jwttoken = ''
        return j.clients.cockpit.getClient(self.base_url, jwttoken)

    def cockpitUpdate(self, **kwargs):
        cl = self.get_client(**kwargs)
        return cl.updateCockpit()

    def templatesUpdate(self, repo=None, template_name=None, ays_repo=None, **kwargs):
        cl = self.get_client(**kwargs)
        if not repo and not template_name:
            if not ays_repo:
                updated = list()
                for domain, domain_info in j.core.atyourservice.config['metadata'].items():
                    base, provider, account, repo, dest, url = j.do.getGitRepoArgs(domain_info.get('url'),
                                                                                   codeDir=j.dirs.codeDir)
                    self._cuisine.development.git.pullRepo(domain_info.get('url'),
                                                           branch=domain_info.get('branch', 'master'),
                                                           dest=dest)
                    updated.append(domain)
                return "template repos [" + ', '.join(updated) + "] are updated"
            else:
                updated = self._cuisine.development.git.pullRepo(ays_repo, codedir=j.dirs.codeDir)
                return "template %s repo updated" % updated
        elif not template_name:
            cl.updateTemplates(repo)
            return "templates updated"
        cl.updateTemplate(repo, template_name)
        return "template updated"

    def addTemplateRepo(self, url, branch='master', **kwargs):
        """
        Add a new service template repository.
        param:url Service template repository URL
        param:branch Branch of the repo to use default:master
        result json
        """
        if url == '':
            raise exceptions.BadRequest("URL can't be empty")

        if not url.startswith('http'):
            raise exceptions.BadRequest("URL Format not valid. It should starts with http")

        if url.endswith('.git'):
            url = url[:-len('.git')]

        cl = self.get_client(**kwargs)

        try:
            cl.addTemplateRepo(url=url, branch=branch)
        except j.exceptions.RuntimeError as e:
            raise exceptions.BadRequest(e.message)

        self.reload(**kwargs)

        return "Repository added"

    def listRepos(self, **kwargs):
        cl = self.get_client(**kwargs)
        repos = cl.listRepositories()
        return repos

    def listRuns(self, repository=None, **kwargs):
        """
        list all repository's runs
        param:repository in that repo will only be returned otherwise all runs
        result list of runids
        """
        cl = self.get_client(**kwargs)
        output_runs = dict()
        repos = self.listRepos(**kwargs)
        repos = [repository] if repository else [r['name']for r in repos]

        for aysrepo in repos:
            runs = cl.listRuns(repository=aysrepo)
            output_runs.update({aysrepo: runs})
        return output_runs

    def getSource(self, hash, repository, **kwargs):
        """
        param:repository where source is
        param: hash hash of source file
        result json of source
        """
        cl = self.get_client(**kwargs)
        source = cl.getSource(source=hash, repository=repository)
        return source

    def getHRD(self, hash, repository, **kwargs):
        """
        param:repository where source is
        param: hash hash of hrd file
        result json of hrd
        """
        cl = self.get_client(**kwargs)
        hrd = cl.getHRD(hrd=hash, repository=repository)
        return hrd

    def getRun(self, repository=None, runid=None, **kwargs):
        """
        get run
        param:repository
        param: runid
        result json of runinfo
        """
        cl = self.get_client(**kwargs)
        aysrun = cl.getRun(aysrun=runid, repository=repository)
        return aysrun

    def createRun(self, repository=None, **kwargs):
        """
        get run
        param:repository
        param: runid
        result json of runinfo
        """
        cl = self.get_client(**kwargs)
        aysrun = cl.createRun(repository=repository)
        return aysrun['key']

    def listServices(self, repository=None, role=None, templatename=None, **kwargs):
        """
        list all services
        param:name services in that base name will only be returned otherwise all names
        result json of {aysname:services}
        """
        cl = self.get_client(**kwargs)
        output_services = dict()
        repos = self.listRepos(**kwargs)
        repos = [repository] if repository else [r['name']for r in repos]

        for aysrepo in repos:
            services = cl.listServices(repository=aysrepo)
            if role:
                output_services.update(
                    {aysrepo: {service['key']: service for service in services if service['role'] == role}})
            elif templatename:
                output_services.update(
                    {aysrepo: {service['key']: service for service in services if service['name'] == templatename}})
            else:
                output_services.update({aysrepo: services})
        return output_services

    def getService(self, repository, role, instance, **kwargs):
        cl = self.get_client(**kwargs)
        return cl.getServiceByInstance(instance, role, repository)

    def createBlueprint(self, repository, blueprint, contents, **kwargs):
        """
        create a blueprint
        param:repository where blueprint will be created
        param:blueprint blueprint name
        param:contents content of blueprint
        result json
        """
        cl = self.get_client(**kwargs)
        return cl.createNewBlueprint(repository, blueprint, contents)

    def deleteBlueprint(self, repository, blueprint, **kwargs):
        """
        delete a blueprint
        param:repository where blueprint will be created
        param:blueprint blueprint name
        result json
        """
        cl = self.get_client(**kwargs)
        return cl.deleteBlueprint(repository, blueprint)

    def executeBlueprint(self, repository, blueprint='', role='', instance='', **kwargs):
        """
        execute blueprint
        param:name blueprints in that base name will only be returned otherwise all names
        result json
        """
        cl = self.get_client(**kwargs)
        role = '' if not role else role
        instance = '' if not instance else instance
        if not blueprint:
            blueprints = [
                bp['name'] for bp in self.listBlueprints(
                    repository=repository,
                    archived=False,
                    **kwargs)[repository]]
        else:
            blueprints = [blueprint]

        if not blueprints:
            return 'No Blueprints Found in Repo!'
        try:
            for bp in blueprints:
                cl.executeBlueprint(repository=repository, blueprint=bp, role=role, instance=instance)
        except Exception as e:
            raise exceptions.BadRequest(str(e))

        msg = "blueprint%s\n %s \nexecuted" % ('s' if len(blueprints) > 1 else '', ','.join(blueprints))
        return msg

    def quickBlueprint(self, repository, name='', contents='', **kwargs):
        """
        quickly execute blueprint and remove from filesystem
        param:contents of blueprint
        result json
        """
        bpname = name or j.data.time.getLocalTimeHRForFilesystem() + '.yaml'
        try:
            self.createBlueprint(repository=repository, blueprint=bpname, contents=contents, **kwargs)
            self.executeBlueprint(repository=repository, blueprint=bpname, **kwargs)
            if not name:
                self.archiveBlueprint(repository=repository, blueprint=bpname, **kwargs)
        except Exception as e:
            raise exceptions.BadRequest("Blueprint failed to execute. Error was %s" % e)
        msg = "Blueprint executed!"
        return msg

    def listBlueprints(self, repository=None, archived=True, **kwargs):
        """
        list all blueprints
        param:name blueprints in that base name will only be returned otherwise all names
        result json
        """
        cl = self.get_client(**kwargs)
        blueprints = OrderedDict()
        repos = self.listRepos(**kwargs)
        repos = [repository] if repository else [r['name']for r in repos]

        for aysrepo in repos:
            bps = cl.listBlueprints(repository=aysrepo, archived=archived)
            blueprints.update({aysrepo: bps})

        return blueprints

    def archiveBlueprint(self, repository, blueprint, **kwargs):
        """
        archive blueprint
        param:name blueprints in that base name will only be returned otherwise all names
        result json
        """
        cl = self.get_client(**kwargs)
        try:
            resp = cl.archiveBlueprint(repository=repository, blueprint=blueprint)
        except Exception as e:
            raise exceptions.BadRequest(str(e))
        return resp['msg']

    def restoreBlueprint(self, repository, blueprint, **kwargs):
        """
        list all blueprints
        param:name blueprints in that base name will only be returned otherwise all names
        result json
        """
        cl = self.get_client(**kwargs)
        try:
            resp = cl.restoreBlueprint(repository=repository, blueprint=blueprint)
        except Exception as e:
            raise exceptions.BadRequest(str(e))
        return resp['msg']

    def listTemplates(self, repository=None, **kwargs):
        """
        list all templates of a certain type
        result json
        """
        cl = self.get_client(**kwargs)
        templates = dict()
        repos = self.listRepos(**kwargs)
        repos = [repository] if repository else [r['name']for r in repos]

        for aysrepo in repos:
            tmpls = cl.listTemplates(repository=aysrepo)
            templates.update({aysrepo: tmpls})
        return templates

    def getTemplate(self, repository, template, **kwargs):
        """
        list all templates of a certain type
        result json
        """
        cl = self.get_client(**kwargs)
        return cl.getTemplate(repository=repository, template=template)

    def createRepo(self, name, **kwargs):
        git_url = kwargs['git_url']
        cl = self.get_client(**kwargs)
        data = j.data.serializer.json.dumps({'name': name, "git_url": git_url})
        try:
            resp = cl._client.createNewRepository(data=data)
        except Exception as e:
            if "Failed to establish a new connection" in str(e.args[0]):
                raise requests.exceptions.ConnectionError('Ays API server is not running')
            raise RuntimeError("unknown error in creation of repo:%s" % e)
        if resp.status_code != 200:
            ret = resp.json()
            ret['status_code'] = resp.status_code
            return ret
        return resp.json()

    def deleteRepo(self, repositorypath, **kwargs):
        try:
            repo = j.core.atyourservice.repoGet(repositorypath)
            repo.destroy()
        except Exception as e:
            raise exceptions.BadRequest(str(e))
        return "repo destroyed."

    def deleteRuns(self, repositorypath, **kwargs):
        try:
            repo = j.core.atyourservice.repoGet(repositorypath)
            j.core.jobcontroller.db.runs.delete(repo=repo)
        except Exception as e:
            raise exceptions.BadRequest(str(e))

        return "runs removed."

    def init(self, repository, role='', instance='', force=False, **kwargs):
        cl = self.get_client(**kwargs)
        try:
            resp = cl.initRepository(repository=repository, role=role, instance=instance, force=force)
        except Exception as e:
            raise exceptions.BadRequest(str(e))
        return resp['msg']

    def install(self, repository, **kwargs):
        try:
            contents = 'actions:\n    - action: install'
            bpname = j.data.idgenerator.generateXCharID(8) + '.yaml'
            self.createBlueprint(repository=repository, blueprint=bpname, contents=contents)
            self.executeBlueprint(repository=repository)
            self.deleteBlueprint(repository=repository, blueprint=bpname)
            run = self.createRun(repository=repository)
        except Exception as e:
            raise exceptions.BadRequest(str(e))
        return run

    def simulate(self, repositorypath, **kwargs):
        try:
            repo = j.core.atyourservice.repoGet(repositorypath)
            run = repo.runCreate()
            return run.__repr__()
        except Exception as e:
            raise exceptions.BadRequest(str(e))

    def executeAction(self, repository, action, role='', instance='', **kwargs):
        cl = self.get_client(**kwargs)
        role = '' if not role else role
        instance = '' if not instance else instance
        try:
            resp = cl.executeAction(
                repository=repository,
                action=action,
                role=role,
                instance=instance)
        except Exception as e:
            raise exceptions.BadRequest(str(e))
        return resp['msg']

    def deleteService(self, repositorypath, role='', instance='', **kwargs):
        try:
            repo = j.core.atyourservice.repoGet(repositorypath)
            service = repo.serviceGet(role=role, instance=instance)
            service.delete()
        except Exception as e:
            raise exceptions.BadRequest(str(e))
        return "Service deleted"

    def reload(self, **kwargs):
        cl = self.get_client(**kwargs)
        try:
            cl.reloadAll()
        except j.exceptions.RuntimeError as e:
            return 'Error during reloading : %s' % e.message
        return 'Cockpit reloaded'

    def commit(self, message, branch='master', push=True, **kwargs):
        path = j.sal.fs.joinPaths(j.dirs.codeDir, 'ays_cockpit')
        if not j.core.atyourservice.exist(path=path):
            return "can't find ays repository for cockpit at %s" % path
        repo = j.core.atyourservice.get(path=path)

        sshkey_service = repo.getService('sshkey', 'main', die=False)
        if sshkey_service is None:
            return "can't find sshkey service"

        sshkey_service.actions.start(service=sshkey_service)

        if message == "" or message is None:
            message = "log changes for cockpit repo"
        gitcl = j.clients.git.get("/opt/code/cockpit")
        if branch != "master":
            gitcl.switchBranch(branch)

        gitcl.commit(message, True)

        if push:
            print("PUSH")
            gitcl.push()

        msg = "repo committed"
        if push:
            msg += ' and pushed'
        return msg

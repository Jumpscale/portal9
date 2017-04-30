[actor] @dbtype:mem,fs
    """
    gateway to atyourservice
    """
    method:cockpitUpdate
        result:json

    method:templatesUpdate
        """
        update templates repo
        """
        result:json

    method:addTemplateRepo
        """
        Add a new service template repository.
        """
        var:url str,, Service template repository URL
        var:branch str,, Branch of the repo to use default:master
        result:str

    method:listRepos
        """
        list all repository
        """
        result:json

    method:listServices
        """
        list all services
        """
        var:repository str,,services in that base path will only be returned otherwise all paths @tags: optional
        var:templatename str,, only services with this templatename else all service names @tags: optional
        var:role str,, only services with this role else all service names @tags: optional
        result:json

    method:getService
        """
        get one services
        """
        var:repository str,,services in that base path will only be returned otherwise all paths
        var:role str,, service role
        var:instance str,, service instance
        result:json


    method:listTemplates
        """
        list ays templates
        """
        var:repository str,,services in that base path will only be returned otherwise all paths @tags: optional
        result:json

    method:getTemplate
        """
        list ays templates
        """
        var:repository str,,repository in which look for template
        var:template str,,template name
        result:json

    method:createBlueprint
        """
        create a blueprint
        """
        var:repository str,,blueprints in that base path will only be returned otherwise all paths
        var:blueprint str,,blueprint name @tags: optional
        var:role str,,role @tags: optional
        result:json

    method:executeBlueprint
        """
        execute all blueprints
        """
        var:repository str,,blueprints in that base path will only be returned otherwise all paths
        var:blueprint str,,blueprint name @tags: optional
        var:role str,,role @tags: optional
        result:json

    method:quickBlueprint
        """
        execute all blueprints
        """
        var:repository str,,blueprints in that base path will only be returned otherwise all paths
        var:name str,,name of blueprint. if empty will archive with name being time @tags: optional
        var:contents str,,content of blueprint
        result:json

    method:listBlueprints
        """
        list all blueprints
        """
        var:repository str,,blueprints in that base path will only be returned otherwise all paths @tags: optional
        var:archived bool,,include archived blueprints or not @tags: optional default:True
        result:json

    method:archiveBlueprint
        """
        archive a blueprint
        """
        var:repository str,,repository name
        var:blueprint str,,blueprint name
        result:json

    method:restoreBlueprint
        """
        restore a blueprint
        """
        var:repository str,,repository name
        var:blueprint str,, blueprint name
        result:json

    method:createRepo
        """
        Create AYS repository
        """
        var:name str,, name of the repository
        result:json

    method:deleteRepo
        """
        Destroy AYS repository
        """
        var:repositorypath str,, path of the repository
        result:json
        
    method:deleteRuns
        """
        Destroy all runs in DB.
        """
        result:json
    method:init
        """
        Run init on AYS repository
        """
        var:repository str,, name of the repository
        var:role str,, role of the services to simulate action on @tag optional
        var:instance str,, instance name of the service to simulate action on @tag optional
        var:force bool,, force init

    method:install
        """
        Run install on AYS repository
        """
        var:repository str,, name of the repository
        result:json


    method:simulate
        """
        Run simulate on AYS repository
        """
        var:repositorypath str,, path of the repository
        result:json

    method:executeAction
        """
        Run execute on AYS repository
        """
        var:repository str,, name of the repository
        var:action str,, name of the action to execute
        var:role str,, role of the services to simulate action on @tag optional
        var:instance str,, instance name of the service to simulate action on @tag optional
        var:force bool,, force the action or not
        var:async bool,, execution action asynchronously @tag optional
        result:json

    method:deleteService
        """
        Uninstall a service
        """
        var:repositorypath str,, path of the repository
        var:role str,, role of the services to delete @tag optional
        var:instance str,, instance name of the service to delete @tag optional
        result:json

    method:commit
        """
        Commit AYS repository and push to github
        """
        var:name str,, name of the repository
        result:json

    method:reload
        """
        Unload all services from memory and force reload.
        """
        result:json

    method:commit
        """
        Commit change in the cockpit repo.
        """
        var:branch str,, branch to commit on
        var:push bool,, push after commit
        var:message str,, name of the repository @tag optional
        result:json

    method:createRun
        """
        """
        var:repository str,, repository name

from js9 import j
from JumpScale9Portal.portal import exceptions
from JumpScale9Portal.portal.auth import auth
import re


class system_usermanager(j.tools.code.classGetBase()):

    """
    register a user (can be done by user itself, no existing key or login/passwd is needed)

    """

    def __init__(self):

        self._te = {}
        self.actorname = "usermanager"
        self.appname = "system"

    def authenticate(self, name, secret, **kwargs):
        """
        The function evaluates the provided username and password and returns a session key.
        The session key can be used for doing api requests. E.g this is the authkey parameter in every actor request.
        A session key is only vallid for a limited time.
        param:username username to validate
        param:password password to validate
        result str,,session
        """

        ctx = kwargs['ctx']
        if j.portal.tools.server.active.auth.authenticate(name, secret):
            session = ctx.env['beaker.session']
            session['user'] = name
            session._redis = True
            session.save()
            return session.id
        raise exceptions.Unauthorized("Unauthorized")

    @auth(['admin'])
    def userget(self, name, **kwargs):
        """
        get a user
        param:name name of user
        """
        user = j.portal.tools.models.system.User.find({"name": name})
        return user[0].to_dict()

    def getuserwithid(self, id, **kwargs):
        """
        get a user
        param:id id of user
        """
        return j.portal.tools.models.system.User.get(id).to_dict()

    def getgroup(self, id, **kwargs):
        """
        get a user
        param:id id of user
        """
        return j.portal.tools.models.system.Group.get(id).to_dict()

    def listusers(self, **kwargs):
        dict_users = list()
        users = j.portal.tools.models.system.User.find({})
        for user in users:
            dict_users.append(user.to_dict())
        return dict_users

    def usergroupsget(self, user, **kwargs):
        """
        return list of groups in which user is member of
        param:user name of user
        result list(str)

        """
        user = self._getUser(user)
        ctx = kwargs['ctx']

        if not user:
            ctx.start_response('404 Not Found', [('Content-Type', 'text/plain')])
            return "User %s not found" % user
        else:
            # print "usergroups:%s" % user.groups
            return user.groups

    def _getUser(self, user):
        users = j.portal.tools.models.system.User.find({"name": user})
        if not users:
            return None
        return users[0]

    @auth(['admin'])
    def editUser(self, username, groups, emails, password, **kwargs):
        ctx = kwargs['ctx']
        user = self._getUser(username)
        if not user:
            ctx.start_response('404 Not Found', [('Content-Type', 'text/plain')])
            return "User %s not found" % username
        if groups:
            if isinstance(groups, str):
                groups = [x.strip() for x in groups.split(',')]
            elif not isinstance(groups, list):
                ctx.start_response('400 Bad Request', [('Content-Type', 'text/plain')])
                return "Groups paramter should be a list or string"
        else:
            groups = []
        if emails:
            if isinstance(emails, str):
                emails = [x.strip() for x in emails.split(',')]
            elif not isinstance(emails, list):
                ctx.start_response('400 Bad Request', [('Content-Type', 'text/plain')])
                return "Emails should be a list or a comma seperated string"
            user.emails = emails
        if password:
            user.passwd = password

        user.groups = groups
        user.save()
        return True

    @auth(['admin'])
    def delete(self, username, **kwargs):
        models = j.portal.tools.models
        user = models.system.User.objects.get(name=username)
        sessions = models.system.SessionCache.objects(user=username)
        for session in sessions:
            session.delete()
        user.delete()
        return True

    @auth(['admin'])
    def deleteGroup(self, id, **kwargs):
        group = j.portal.tools.models.system.Group.get(id)
        for user in j.portal.tools.models.system.User.find({"groups": group['name']}):
            user['groups'].remove(group.name)
            user.save()
        group.delete()

    @auth(['admin'])
    def createGroup(self, name, description, **args):
        """
        create a group
        param:name name of group
        param:description of group
        result bool

        """
        if j.portal.tools.models.system.Group.find({"name": name}):
            raise exceptions.Conflict("Group with name %s already exists" % name)
        group = j.portal.tools.models.system.Group()
        group.name = name.strip()
        group.description = description
        group.save()
        return True

    @auth(['admin'])
    def editGroup(self, name, description, users, **args):
        """
        edit a group
        param:name name of group
        param:description of group
        result bool

        """
        groups = j.portal.tools.models.system.Group.find({"name": name})

        if not groups:
            raise exceptions.NotFound("Group with name %s does not exists" % name)
        else:
            group = groups[0]
        if users and isinstance(users, str):
            users = users.split(',')
        elif not users:
            users = []
        users_old = [u['name'] for u in j.portal.tools.models.system.User.find({'groups': name})]
        users_remove = [x for x in users_old if x not in users]
        for user_name in users_remove:
            user = self._getUser(user_name)
            user['groups'].remove(group.name)
            user.save()

        users_add = [x for x in users if x not in users_old]
        for user_name in users_add:
            user = self._getUser(user_name)
            user['groups'].append(group.name)
            user.save()

        group['name'] = name
        group['description'] = description
        group.save()
        return True

    def _isValidUserName(self, username):
        r = re.compile('^[a-z0-9]{1,20}$')
        return r.match(username) is not None

    @auth(['admin'])
    def create(self, username, emails, password, groups, **kwargs):
        ctx = kwargs['ctx']
        headers = [('Content-Type', 'text/plain'), ]

        if not self._isValidUserName(username):
            ctx.start_response('409', headers)
            return 'Username may not exceed 20 characters and may only contain a-z and 0-9'

        check, result = self._checkUser(username)
        if check:
            ctx.start_response('409', headers)
            return "Username %s already exists" % username
        groups = groups or []
        return j.portal.tools.server.active.auth.createUser(username, password, emails, groups)

    def _checkUser(self, username):

        users = j.portal.tools.models.system.User.find({"name": username})
        if not users:
            return False, 'User %s does not exist' % username
        return True, users[0]

    def userexists(self, name, **args):
        """
        param:name name
        result bool

        """
        user = j.portal.tools.models.system.User.find({"name": name})[0]
        if user:
            return True

    def whoami(self, **kwargs):
        """
        result current user
        """
        ctx = kwargs["ctx"]
        return {
            "name": ctx.env['beaker.session']["user"],
            "admin": j.portal.tools.server.active.isAdminFromCTX(ctx)
        }

    def userregister(self, name, passwd, emails, reference, remarks, config, **args):
        """
        param:name name of user
        param:passwd chosen passwd (will be stored hashed in DB)
        param:emails comma separated list of email addresses
        param:reference reference as used in other application using this API (optional)
        param:remarks free to be used field by client
        param:config free to be used field to store config information e.g. in json or xml format
        result bool

        """
        # put your code here to implement this method
        raise NotImplementedError("not implemented method userregister")

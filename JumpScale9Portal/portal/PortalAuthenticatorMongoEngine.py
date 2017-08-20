from js9 import j
from JumpScale9Portal.portal import exceptions

class PortalAuthenticatorMongoEngine(object):

    def __init__(self):
        self.usermodel = j.portal.tools.models.system.User
        self.groupmodel = j.portal.tools.models.system.Group
        self.key2user = {user['authkey']: user['id']
                         for user in j.portal.tools.models.system.User.find(query={'authkey': {'$ne': ''}})}
        if not self.key2user:
            # Only to create a default admin user to login with.
            # Should be done in AYS
            if not j.portal.tools.models.system.User.find(query={'name': 'admin'}):
                self.createUser('admin', 'admin', 'demo@1234.com', ['admin'], 'domain.com')

    def getUserFromKey(self, key):
        if key not in self.key2user:
            return "guest"
        return self.key2user[key]

    def _getkey(self, model, name):
        results = model.find({'name': name})
        if results:
            return results[0].pk
        else:
            return name

    def getUserInfo(self, user):
        return j.portal.tools.models.system.User.get(self._getkey(self.usermodel, user))

    def getGroupInfo(self, groupname):
        return j.portal.tools.models.system.Group.get(self._getkey(self.groupmodel, groupname))

    def userExists(self, user):
        return j.portal.tools.models.system.User.get(self._getkey(self.usermodel, user))

    def createUser(self, username, password, email, groups, domain):
        if self.userExists(username):
            raise exceptions.Conflict("Username with name {} already exists".format(username))
        user = self.usermodel()
        user.name = username
        if isinstance(groups, str):
            groups = [groups]
        user.groups = groups
        for group in user.groups:
            g = self.groupmodel.find({'name': group})
            if g:
                continue
            g = self.groupmodel()
            g.name = group
            g.save()
        if isinstance(email, str):
            email = [email]
        user.emails = email
        user.domain = domain
        user.passwd = password
        return user.save()

    def listUsers(self):
        return self.usermodel.find({})

    def listGroups(self):
        return self.groupmodel.find({})

    def getGroups(self, user):
        try:
            userinfo = self.getUserInfo(user)
            return userinfo['groups'] + ["all"]
        except:
            return ["guest", "guests"]

    def loadFromLocalConfig(self):
        #@tddo load from users.cfg & populate
        # see jsuser for example
        pass

    def authenticate(self, login, passwd):
        """
        """
        login = login[0] if isinstance(login, list) else login
        passwd = passwd[0] if isinstance(passwd, list) else passwd
        result = j.portal.tools.models.system.User.authenticate(username=login, passwd=passwd)
        return result

    def getUserSpaceRights(self, username, space, **kwargs):
        spaceobject = kwargs['spaceobject']
        groupsusers = set(self.getGroups(username))

        for groupuser in groupsusers:
            if groupuser in spaceobject.model.acl:
                right = spaceobject.model.acl[groupuser]
                if right == "*":
                    return username, "rwa"
                return username, right

        # No rights .. check guest
        rights = spaceobject.model.acl.get('guest', '')
        return username, rights

    def getUserSpaces(self, username, **kwargs):
        spaceloader = kwargs['spaceloader']
        return [x.model.id.lower() for x in list(spaceloader.spaces.values())]

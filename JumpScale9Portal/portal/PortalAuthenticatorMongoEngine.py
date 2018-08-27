from js9 import j
from JumpScale9Portal.portal import exceptions
import uuid

class PortalAuthenticatorMongoEngine(object):

    def __init__(self):
        self.usermodel = j.portal.tools.models.system.User
        self.groupmodel = j.portal.tools.models.system.Group
        self.key2user = {}
        self._get_key2user()
        if not self.key2user:
            # Only to create a default admin user to login with.
            # Should be done in AYS
            if not j.portal.tools.models.system.User.find(query={'name': 'admin'}):
                self.createUser('admin', 'admin', 'demo@1234.com', ['admin'])

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

    def _get_key2user(self):
        for user in j.portal.tools.models.system.User.find(query={'authkeys': {'$ne': {}}}):
            for authkey in user.authkeys.values():
                self.key2user[authkey] = user.name

    def getUserInfo(self, user):
        return j.portal.tools.models.system.User.get(self._getkey(self.usermodel, user))

    def getGroupInfo(self, groupname):
        return j.portal.tools.models.system.Group.get(self._getkey(self.groupmodel, groupname))

    def userExists(self, user):
        user = j.portal.tools.models.system.User.find({"name": user})
        if user:
            return True

    def emailExists(self, emails):
        user = j.portal.tools.models.system.User.find({"emails": {"$in": emails}})
        if user:
            return True

    def addAuthkey(self, username, key_name):
        authkey = str(uuid.uuid4())
        user = self.getUserInfo(username)
        user.authkeys[key_name] = authkey
        user.save()
        self.key2user[authkey] = username
        return authkey

    def deleteAuthkey(self, username, key_name):
        user = self.getUserInfo(username)
        authkey = user.authkeys.pop(key_name)
        user.save()
        self.key2user.pop(authkey)
        return True

    def createUser(self, username, password, email, groups, authkey=None, authkey_name=None):
        """
        Creates a new user and returns the result of the creation.
        :param username: user's name
        :param password: user's password
        :param email: user's email
        :param groups: list of groups the user belongs
        :param authkey: user's auth key
        :param authkey_name: user's auth key's name
        :return: mongodb WriteResult object
        """
        if self.userExists(username):
            raise exceptions.Conflict("Username with name {} already exists".format(username))
        if isinstance(email, str):
            email = [email]
        if self.emailExists(email):
            raise exceptions.Conflict("User with email {} already exists".format(" or ".join(email)))
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
        if authkey:
            if not authkey_name:
                raise exceptions.BadRequest("Authkey_name can't be none")
            user.authkeys[authkey_name] = authkey
            self.key2user[authkey] = username
        user.emails = email
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

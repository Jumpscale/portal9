from js9 import j
from JumpScale9Portal.portal import exceptions

base = j.portal.tools._getBaseClassLoader()


class UserManager:

    def __init__(self):
        base.__init__(self)

    def createUser(self, username, password, email, groups, authkey=None):
        """
        Creates a new user and returns the result of the creation.
        :param username: user's name
        :param password: user's password
        :param email: user's email
        :param groups: list of groups the user belongs
        :param authkey: user's auth key
        :return: mongodb WriteResult object
        """
        if self.userExists(username):
            raise exceptions.Conflict("Username with name {} already exists".format(username))
        if isinstance(email, str):
            email = [email]
        if self.emailExists(email):
            raise exceptions.Conflict("User with email {} already exists".format(" or ".join(email)))
        user = j.portal.tools.models.system.User()
        user.name = username
        if isinstance(groups, str):
            groups = [groups]
        user.groups = groups
        for group in user.groups:
            g = j.portal.tools.models.system.Group.find({'name': group})
            if g:
                continue
            g = j.portal.tools.models.system.Group()
            g.name = group
            g.save()
        if authkey:
            user.authkeys = [authkey]
        user.emails = email
        user.passwd = password
        return user.save()


    def getUser(self, user):
        user = j.portal.tools.models.system.User.find({"name": user})
        return user

    def emailExists(self, emails):
        user = j.portal.tools.models.system.User.find({"emails": {"$in": emails}})
        if user:
            return True

    def userExists(self, user):
        user = j.portal.tools.models.system.User.find({"name": user})
        if user:
            return True
from js9 import j


class PortalAuthenticatorMinimal(object):
    """
    Main functionality is to provide authenticate() function and other helper functions
    Those functions are all added to client
    """

    def __init__(self, instance='main'):
        pass

    def authenticate(self, login, password):
        return True

    def getGroups(self, username):
        return ['guest']

    def getUserFromKey(self, key):
        return "guest"

    def getUserSpaces(self, username, **kwargs):
        # TODO
        return []

    def getUserSpacesObjects(self, username):
        return []

    def getUserSpaceRights(self, username, space, **kwargs):
        return 'guest', 'rwa'

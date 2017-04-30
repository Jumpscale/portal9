from js9 import j
from JumpScale.portal.portal import exceptions
import requests


class system_oauthtoken(j.tools.code.classGetBase()):

    def __init__(self):
        pass

        self._te = {}
        self.actorname = "oauthtoken"
        self.appname = "system"

    def generateJwtToken(self, **kwargs):
        ctx = kwargs['ctx']

        oauth_ctx = ctx.env['beaker.session'].get('oauth', None)
        if oauth_ctx is None:
            raise exceptions.BadRequest("No oauth information in session")

        access_token = oauth_ctx.get('access_token', None)
        if access_token is None:
            raise exceptions.BadRequest("No access_token in session")

        # generate JWT
        headers = {'Authorization': 'bearer ' + access_token}
        url = 'https://itsyou.online/v1/oauth/jwt/refresh'
        resp = requests.post(url, headers=headers, verify=False)
        resp.raise_for_status()

        return resp.text

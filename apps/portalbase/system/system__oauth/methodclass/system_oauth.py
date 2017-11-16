import urllib.request
import urllib.parse
import urllib.error
import json
from js9 import j
from JumpScale9Portal.portal import exceptions


class system_oauth(j.tools.code.classGetBase()):
    """
    Oauth System actors
    """

    def __init__(self):
        self.logger = j.logger.get("j.portal.oauth")
        self.cfg = j.portal.tools.server.active.oauth_cfg
        self._client = None

    @property
    def client(self):
        if not self._client:
            self._client = j.clients.oauth.get(addr=self.cfg.get('client_url'), accesstokenaddr=self.cfg.get('token_url'), id=self.cfg.get('client_id'),
                                               secret=self.cfg.get('client_secret'), scope=self.cfg.get('client_scope'), redirect_url=self.cfg.get('redirect_url'),
                                               user_info_url=self.cfg.get('client_user_info_url'), logout_url='', instance=self.cfg.get('force_oauth_instance'))
        return self._client

    def authenticate(self, type='', **kwargs):
        cache = j.core.db

        if j.portal.tools.server.active.force_oauth_instance:
            type = j.portal.tools.server.active.force_oauth_instance

        if not type:
            type = 'github'

        ctx = kwargs['ctx']

        cache_data = json.dumps({'type': type, 'redirect': ctx.env.get('HTTP_REFERER', '/')})
        cache.set(self.client.state, cache_data, ex=180)
        ctx.start_response('302 Found', [('Location', self.client.url)])
        return 'OK'

    def getOauthLogoutURl(self, **kwargs):
        ctx = kwargs['ctx']
        redirecturi = ctx.env.get('HTTP_REFERER')
        if not redirecturi:
            redirecturi = 'http://%s' % ctx.env['HTTP_HOST']
        session = ctx.env['beaker.session']
        if session:
            oauth = session.get('oauth')
            session.delete()
            session.save()
            if oauth:
                back_uri = urllib.parse.urlencode({'redirect_uri': redirecturi})
                location = str('%s?%s' % (oauth.get('logout_url'), back_uri))
                ctx.start_response('302 Found', [('Location', location)])
            else:
                ctx.start_response('302 Found', [('Location', redirecturi)])
        else:
            ctx.start_response('302 Found', [('Location', redirecturi)])
        return ''

    def authorize(self, **kwargs):
        ctx = kwargs['ctx']
        session = ctx.env['beaker.session']
        code = kwargs.get('code')
        cache_result = None

        def authfailure(msg):
            session['autherror'] = msg
            session._redis = True
            session.save()
            self.logger.warn(msg)
            if cache_result:
                redirect_url = str(cache_result['redirect'])
            else:
                redirect_url = '/'
            raise exceptions.Redirect(redirect_url)

        if not code:
            return authfailure('Code is missing')

        state = kwargs.get('state')
        if not state:
            return authfailure('State is missing')

        cache = j.core.db
        cache_result = cache.get(state)
        cache.delete(state)

        if not cache_result:
            msg = 'Failed to authenticate. Invalid or expired state'
            return authfailure(msg)

        cache_result = j.data.serializer.json.loads(cache_result)

        # generate access_token / master jwt
        try:
            accesstoken = self.client.getAccessToken(code, state)
            userinfo = self.client.getUserInfo(accesstoken)
        except AuthError as e:
            return authfailure(str(e))

        user_model = j.portal.tools.models.system.User
        user_obj = user_model.find({'name': userinfo.username})

        if not user_obj:
            # register user
            u = user_model()
            u.name = userinfo.username
            if userinfo.emailaddress:
                u.emails = [userinfo.emailaddress]
            u.groups.extend(self.cfg.get('default_groups', ['user']))
            u.save()
        else:
            u = user_obj[0]
            if userinfo.username != u['name']:
                return authfailure('User with the same name already exists')

        session = ctx.env['beaker.session']
        session['user'] = userinfo.username
        if userinfo.emailaddress:
            session['email'] = userinfo.emailaddress
        session['oauth'] = {
            'authorized': True,
            'type': str(cache_result['type']),
            'logout_url': self.client.logout_url,
            'access_token': accesstoken['access_token']
        }
        session.pop('autherror', None)
        session['_expire_at'] = int(j.data.time.epoch + accesstoken['expires_in'] - 3600)
        session.save()

        raise exceptions.Redirect(str(cache_result['redirect']))


class AuthError(Exception):
    pass

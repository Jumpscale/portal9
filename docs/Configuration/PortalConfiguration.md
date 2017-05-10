# Portal Configuration

The configuration of the portal is stored in the ays `service.hrd file` eg. at `/optvar/cfg/jumpscale/portals/main/config.yaml
`

```python

mongoengine.connection:
    host: 'localhost'
    port: 27017

rootpasswd: 'admin'

ipaddr: '127.0.0.1'
port: '8200'
appdir: '$JSAPPSDIR/portals/portalbase'
filesroot: '$VARDIR/portal/files'
defaultspace: 'system'
admingroups:
    - 'admin'
authentication.method: 'me'
gitlab.connection: 'main'
force_oauth_instance: ''  # set to use oauth
contentdirs:  ''

production:  False

oauth.client_url:  'https://itsyou.online/v1/oauth/authorize'
oauth.token_url:  'https://itsyou.online/v1/oauth/access_token'
oauth.redirect_url:  'http://ae5d255c.ngrok.io/restmachine/system/oauth/authorize'
oauth.client_scope:  'user:email:main,user:memberof:JSPortal'
oauth.client_id:  'JSPortal'
oauth.client_secret:  '8plUHNtpaQp8NExkRa-3MYa1SWkOr1mgEqRxGBm25DD78tHXiIlS'
oauth.client_user_info_url:  'https://itsyou.online/api/users/'
oauth.client_logout_url:  ''
oauth.organization: testOrg
oauth.default_groups:
    - admin
    - user

# instance.proxy:
#     - 1:
#         dest:'http://localhost:8086'
#         path:'/proxy/influxdb'
#
#     - 2:
#         dest:'http://localhost:5000'
#         path:'/proxy/eve'

# instance.navigationlinks.ExtraMenu:
#     - My Website:'https://example.com'
#     - Another Webiste:'https://example.com'
#     - Contact US:'mailto:contactus@exammple.com'

```

|Key|Type|Description|
|---|----|-----------|
|admingroups|list of str| Groups a user needs to be part of to be considered admin|
|appdir|str|path to base portal|
|authentication.method|str|Currently portal supports two authentication methods `mongoengine` and `oauth`|
|contentdirs|str|Comma seperated list of dirs which should be considerd as basedirs, directories which can contain spaces and actors|
|defaultspace|str|The space to use when navigation to the root of the application|
|filesroot|str|Place where static files are used (not used in current version)|
|force_oauth_instance|str|When this option is set authentication will be forced over this specified oauth providerd|
|gitlab.connection|str|Connection used when `authentication.method` = `gitlab`|
|ipaddr|str|Not used currently (we always listen on 0.0.0.0)|
|port|int|Port the portalserver will listen on|
|mongoengine.connection|dict|host and ip of mongod|
|portal.name|str|portal instance name|
|portal.rootpasswd|str| ??|
|production|bool|false if development (disables oauth)|
|oauth.client_url|str|oauth provider authorization url|
|oauth.token_url|str|oauth provider token url|
|oauth.redirect_url|str|redirect url to authorize|
|oauth.client_scope|str|oauth scope|
|oauth.client_id|str|oauth client id|
|oauth.client_secret|str|oauth client secret|
|oauth.client_user_info_url|str|oauth provider user info url|
|oauth.client_logout_url|str|oauth provider logout url|
|oauth.organization|str|oauth organization|
|oauth.default_groups|list of str| groups auto created for logged in users|


## Navigationlinks

`instance.navigationlinks.example` will show a new column in the Navigations menu.
The values of the mapping will be shown underneed eachother.
It is possible to use this to overwrite the visibles spaces by defining `instance.navigationlinks.spaces`.

## OAuth

[See](Oauth-Support.md)

## Gitlab Authentication

When specifying gitlab as authentication we need to know which gitlab_client is currently used.
This fields need to be provided in `gitlab.connection`

# Portal Configuration

The configuration of the portal is stored in the main jumpscale configuration file, located at `~/js9host/cfg/jumpscale9.toml`. It will be added to the configuration after portal is installed.

An examlpe configuration for an instance of portal called main:
`

```python

[portal.main]
rootpasswd = "admin"

ipaddr = "127.0.0.1"
port = "8200"
appdir = "$JSAPPSDIR/portals/portalbase"
filesroot = "$VARDIR/portal/files"
defaultspace = "system"
admingroups = ["admin"]
authentication_method = "me"
gitlab_connection = "main"
contentdirs =  ""
production = false

[portal.main.mongoengine]
host = "localhost"
port = 27017

[portal.main.oauth]
force_oauth_instance = ""  # set to use oauth
client_url = "https://itsyou.online/v1/oauth/authorize"
token_url = "https://itsyou.online/v1/oauth/access_token"
redirect_url = "{portal url}/restmachine/system/oauth/authorize" 
client_scope = "user:email:main,user:memberof:JSPortal"
client_id = "JSPortal"
client_secret = "8plUHNtpaQp8NExkRa-3MYa1SWkOr1mgEqRxGBm25DD78tHXiIlS"
client_user_info_url = "https://itsyou.online/api/users/"
client_logout_url = ""
organization =  "testOrg"
default_groups = ["admin", "user"]

```

In the above file `[portal.main]` means that this is an instance of portal called "main". For each instance there is three sections:

- The main section where general configurations are defined

- '[portal.{instance name}.mongoengine]': The configuration for the portal mongo connection

- '[portal.{instance name}.oauth]': Configuration for oauth when portal is in production mode


|Key|Type|Description|
|---|----|-----------|
|admingroups|list of str| Groups a user needs to be part of to be considered admin|
|appdir|str|path to base portal|
|authentication_method|str|Currently portal supports two authentication methods `mongoengine` and `oauth`|
|contentdirs|str|Comma seperated list of dirs which should be considerd as basedirs, directories which can contain spaces and actors|
|defaultspace|str|The space to use when navigation to the root of the application|
|filesroot|str|Place where static files are used (not used in current version)|
|force_oauth_instance|str|When this option is set authentication will be forced over this specified oauth providerd|
|gitlab_connection|str|Connection used when `authentication_method` = `gitlab`|
|ipaddr|str|Not used currently (we always listen on 0.0.0.0)|
|port|int|Port the portalserver will listen on|
|mongoengine|dict|host and port of mongod|
|rootpasswd|str| Password of the default admin user|
|production|bool|false if development (disables oauth)|
|client_url|str|oauth provider authorization url|
|token_url|str|oauth provider token url|
|redirect_url|str|redirect url to authorize|
|client_scope|str|oauth scope|
|client_id|str|oauth client id|
|client_secret|str|oauth client secret|
|client_user_info_url|str|oauth provider user info url|
|client_logout_url|str|oauth provider logout url|
|organization|str|oauth organization|
|default_groups|list of str| groups auto created for logged in users|

## OAuth

[See](Oauth-Support.md)

## Gitlab Authentication

When specifying gitlab as authentication we need to know which gitlab_client is currently used.
This fields need to be provided in `gitlab_connection`

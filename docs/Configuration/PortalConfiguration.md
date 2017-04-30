# Portal Configuration

The configuration of the portal is stored in the ays `service.hrd file` eg. at `/optvar/hrd/apps/jumpscale__portal__main/service.hrd
`

The most important variables to play with are prefixed with instance

```python
instance.param.cfg.admingroups = 'admin,'
instance.param.cfg.appdir      = '$base/apps/portals/portalbase'
instance.param.cfg.contentdirs =
instance.param.cfg.defaultspace = 'home'
instance.param.cfg.filesroot   = '$vardir/portal/files'
instance.param.cfg.force_oauth_instance = ''
instance.param.cfg.gitlab.connection = 'main'
instance.param.cfg.ipaddr      = 'localhost'
instance.param.cfg.port        = 82
instance.param.cfg.secret      = 'rooter'
instance.param.portal.name     = 'main'
instance.param.portal.rootpasswd = 'rooter'
instance.proxy.1               =
    dest:'http://localhost:8086',
    path:'/proxy/influxdb',

instance.proxy.2               =
    dest:'http://localhost:5000',
    path:'/proxy/eve',

instance.navigationlinks.ExtraMenu =
    My Website:'https://example.com',
    Another Webiste:'https://example.com',
    Contact US:'mailto:contactus@exammple.com',

```

|Key|Type|Description|
|---|----|-----------|
|cfg.admingroups|list of str| Groups a user needs to be part of to be considered admin|
|cfg.appdir|str|path to base portal|
=|cfg.contentdirs|str|Comma seperated list of dirs which should be considerd as basedirs, directories which can contain spaces and actors|
|cfg.defaultspace|str|The space to use when navigation to the root of the application|
|cfg.filesroot|str|Place where static files are used (not used in current version)|
|cfg.force_oauth_instance|str|When this option is set authentication will be forced over this specified oauth providerd|
|cfg.gitlab.connection|str|Connection used when `authentication.method` = `gitlab`|
|cfg.ipaddr|str|Not used currently (we always listen on 0.0.0.0)|
|cfg.port|int|Port the portalserver will listen on|
|cfg.secret|str|If set this `secret` can be used as `authkey` for admin rights|
|portal.name|str|Name which corresponds to the `ays` instance name|
|portal.rootpasswd|str| ??|
|proxy.1|dict|With this option one can make the portalserver act as a reverse proxy|
|navigationlinks.\*|dict|Mapping of links to appear in Navigation menu|


## Navigationlinks

`instance.navigationlinks.example` will show a new column in the Navigations menu.  
The values of the mapping will be shown underneed eachother.  
It is possible to use this to overwrite the visibles spaces by defining `instance.navigationlinks.spaces`.

## OAuth

[See](Oauth-Support.md)

## Gitlab Authentication

When specifying gitlab as authentication we need to know which gitlab_client is currently used.  
This fields need to be provided in `gitlab.connection`

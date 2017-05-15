Portal Webserver Flow
=====================

startup
-------

-   PortalProcess()
    -   loads all info from portal.cfg
    -   starts PortalServer () : use factory j.portal.tools.server.get()
    -   passes secret, cfgdir & port to the PortalServer
-   PortalServer
    -   ...
-   self.bootstrap()
    -   generate actors for usermanager & content manager
-   ask webserver to do loadFromConfig4loader() passes the actors loader

the PortalProcess is the main gevent look and the gevent webserver is
plugged into it.

when incoming request
---------------------

### router

-   gets environ as input.
-   create object RequestContext
    -   will create a requestcontext (is an obj with info specific for
        this webrequest)
    -   is like a placeholder for info for the request
    -   no auth or further processing happens
-   will parse the start of the url path and define where to send the
    request to, this is the router functionality
-   router step 1 (no security, no session)
    -   images -\> page is created, image loaded from /image directory
        under space
    -   files/specs/ will let the remote user download the specs from an
        actor (the specs where put in advance by a rest call in that
        dir, that dir is underneath self.filesroot which is default
        /opt/jumpscale/var/portal/files).
    -   .files -\> allow download of files which are under /.files dir
        of space.
-   call startSession(), a session object is created
-   router step 2 (session is required)
    -   /restmachine -\> self.processor\_rest (old style rest based on
        get), no formatted output
    -   /rest -\> processor\_rest (as restmachine but human readable
        output, so in wiki page)
    -   /restextmachine -\> self.processor\_restext (new style handler
        on rest requests), not formatted output
    -   /restext -\> processor\_restext (as restextmachine but human
        readable output, so in wiki page)
    -   /jobs -\> do we still need this??? TODO @question
    -   /elfinder -\> this to let the explorer work
    -   /ping -\> return pong
    -   /files -\> allows download from self.files location
    -   and then the catch all (return a wiki page)
        -   self.path2spacePagename( defines relation between path &
            space,pathname
        -   self.returnDoc( fetches the doc and returns the formatted
            output

### requestcontext

-   gets the params from the environment (get statements)
-   is done by create of an object RequestContext

### startsession

-   see if 'authkey' is used as param (e.g. in get), if yes lookup which
    user corresponds
-   here the main authentication happens for rest
-   for a not logged in user the username will become guest (not
    authorization is done)

### rest processing

#### processor\_rest

#### processor\_restext

#### process\_elfinder

#### path2spacePagename

#### path2spacePagename

#### returnDoc

-   getDoc() fetches the doc & checks on security
-   execute macros
-   convert to html
-   return page to browser

#### getDoc

-   getUserRight() \#do the authorization
-   fetches the doc (no processing)


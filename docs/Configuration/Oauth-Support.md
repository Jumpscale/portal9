## Portal OAUTH Authentication

###Adding support for specific oauth server

* You need to **add an application in oauth server** in order to obtain a client ID and client SECRET
  * In case of github, open settings/applications/developer applications then create a new app there
* **Add support in portal** for that application
   * installing the package (oauth_client)  `ays install -n oauth_client -i github`
   * Now in Login page you should see something like:
![](https://cloud.githubusercontent.com/assets/526328/8205659/2469402c-14fb-11e5-81f5-69e87405e294.png)
   * If you need to support extra servers, just install (oauth_client) with a new instance for the server you need to add.
   * **Information needed while installing oauth_client package**:
        * OAUTH SERVER AUTHORIZE URL, i.e; https://github.com/login/oauth/authorize
        * OAUTH SERVER ACCESS TOKEN URL, i.e; https://github.com/login/oauth/access_token
        * REDIRECT URL, (FIXED) http://portal_IP:82/restmachine/system/oauth/authorize
        * SCOPE, i.e; user:email
        * CLIENT ID, In case of github you can get it from the developer application used.
        * CLIENT SECRET,   In case of github you can get it from the developer application used.
        * USER INFO URL, the API URL for getting user info, in case of github https://api.github.com/user

## Force using oauth only authentication
* During installing portal set the "force_oauth_instance" attribute value to the name of the oauth instance you want to force using.


## Development Section

* Support for oauth authentication is spread across 3 areas
     * **@ys package** :  _clients/oauth_client
     * **jumpscale client** : `jumpscale_core8/lib/Jumpscale/baselib/oauth/OauthInstance.py`
           * You can use it from shell using `j.clients.oauth.get(type='github')` 
           * replace type by whatever instance you need.
     * **jumpscale portal support**
          * actors: `jumpscale_portal/apps/system/system__oauth`
               * authenticate :`/restmachine//system/oauth/authenticate?type=github` redirects to certain oauth server
               * authorize : `/restmachine//system/oauth/authorize`  call back api oauth server calls
* If username and email returned from oauth server found then user is logged in.
* If username is found but email is different than that returned from oauth server, 400 bad request (User already exists) response is returned

## Force using oauth only authentication
* During installing portal set the "force_oauth_instance" attribute value to the name of the oauth instance you want to force using.

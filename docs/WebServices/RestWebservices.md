Rest Services
=============

```
http://localhost:82/rest/system/contentmanager/getSpaces
```
(Where 82 is your configured port)

if no error:

```
result of rest call


['tests', 'system', 'testwebsite', 'grid', 'testspace', 'home', 'ays']

how to get machine readable output?

if you want to use this rest interface from a machine (so not by browser) use the following url

http://127.0.0.1/restmachine/system/contentmanager/getSpaces?human=falseauthkey=???

Be carefull generated authkey above has been generated for you as administrator.
```


if error:

```
"Param with name:namespace is missing."
```
or 

```
Execute method GET_system_contentmanager_modelobjectlist failed.
Traceback (most recent call last):
~ File "/opt/jumpscale8/lib/JumpScale/portal/portal/PortalRest.py", line 163, in execute_rest_call
result = method(ctx=ctx, **ctx.params)
~ File "/opt/jumpscale8/apps/portals/portalbase/system/system__contentmanager/methodclass/system_contentmanager.py", line 94, in modelobjectlist
data = dtext.getData(namespace, category, key, **args)
~ File "/opt/jumpscale8/apps/portals/portalbase/system/system__contentmanager/extensions/extension_datatable/DataTables.py", line 88, in getData
datainfo = self.getFromCache(key)
~ File "/opt/jumpscale8/apps/portals/portalbase/system/system__contentmanager/extensions/extension_datatable/DataTables.py", line 69, in getFromCache
return self.cache.cacheGet(key)
~ File "/opt/jumpscale8/lib/JumpScale/baselib/key_value_store/store.py", line 102, in cacheGet
r=self.get("cache",key)
~ File "/opt/jumpscale8/lib/JumpScale/baselib/key_value_store/memory_store.py", line 21, in get
raise j.exceptions.RuntimeError("Could not find object with category %s key %s"%(category,key))
~ RuntimeError: Could not find object with category cache key 1234

type/level: UNKNOWN/1
Execute method GET_system_contentmanager_modelobjectlist failed.
querystr was:category=%27%27&namespace=%27%27&key=1234&format=str
method was:/rest/system/contentmanager/modelobjectlist
```


This format is very difficult to parse but ideal to play around with on webserver.

For machine usage, [RestMachine services](RestMachineServices) would be a better fit.


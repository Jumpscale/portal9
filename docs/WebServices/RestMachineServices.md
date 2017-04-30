RestMachine Services
====================

```
http://localhost:82/restmachine/system/contentmanager/getSpaces
```

if no error:

```
{
    result: [
    "tests",
    "system",
    "testwebsite",
    "grid",
    "testspace",
    "home",
    "ays"
]
}
```

if error:
```
{
    code: "/opt/jumpscale8/lib/JumpScale/baselib/key_value_store/memory_store.py",
    backtrace: "Traceback (most recent call last): ~ File "/opt/jumpscale8/lib/JumpScale/portal/portal/PortalRest.py", line 163, in execute_rest_call result = method(ctx=ctx, **ctx.params) ~ File "/opt/jumpscale8/apps/portals/portalbase/system/system__contentmanager/methodclass/system_contentmanager.py", line 94, in modelobjectlist data = dtext.getData(namespace, category, key, **args) ~ File "/opt/jumpscale8/apps/portals/portalbase/system/system__contentmanager/extensions/extension_datatable/DataTables.py", line 88, in getData datainfo = self.getFromCache(key) ~ File "/opt/jumpscale8/apps/portals/portalbase/system/system__contentmanager/extensions/extension_datatable/DataTables.py", line 69, in getFromCache return self.cache.cacheGet(key) ~ File "/opt/jumpscale8/lib/JumpScale/baselib/key_value_store/store.py", line 102, in cacheGet r=self.get("cache",key) ~ File "/opt/jumpscale8/lib/JumpScale/baselib/key_value_store/memory_store.py", line 21, in get raise j.exceptions.RuntimeError("Could not find object with category %s key %s"%(category,key)) ~ RuntimeError: Could not find object with category cache key 1234 ",
    pid: 0,
    occurrences: 2,
    frames: [ ],
    guid: "48c78186-86f2-4a78-9acc-bc2cbbf89336",
    category: "",
    exceptionclassname: "RuntimeError",
    appname: "portal",
    epoch: 1439285590,
    funclinenr: 21,
    state: "NEW",
    gid: 1,
    type: "UNKNOWN",
    funcfilename: "/opt/jumpscale8/lib/JumpScale/portal/portal/PortalRest.py",
    uniquekey: "060433fc4b550fc961bbf3b6ab3c6105",
    tags: "",
    exceptionmodule: null,
    jid: 0,
    closetime: 0,
    exceptioninfo: "{"message":"Could not find object with category cache key 1234"}",
    nid: 1,
    lasttime: 1439287100,
    data: null,
    errormessagePub: "",
    level: 1,
    tb: "",
    caller: "10.0.3.1",
    errormessage: "Execute method GET_system_contentmanager_modelobjectlist failed. querystr was:category=%27%27&namespace=%27%27&key=1234&format=json method was:/restmachine/system/contentmanager/modelobjectlist",
    funcname: "get",
    backtraceDetailed: " File "/opt/jumpscale8/lib/JumpScale/portal/portal/PortalRest.py" Line 163, in execute_rest_call result = method(ctx=ctx, **ctx.params) File "/opt/jumpscale8/apps/portals/portalbase/system/system__contentmanager/methodclass/system_contentmanager.py" Line 94, in modelobjectlist data = dtext.getData(namespace, category, key, **args) File "/opt/jumpscale8/apps/portals/portalbase/system/system__contentmanager/extensions/extension_datatable/DataTables.py" Line 88, in getData datainfo = self.getFromCache(key) File "/opt/jumpscale8/apps/portals/portalbase/system/system__contentmanager/extensions/extension_datatable/DataTables.py" Line 69, in getFromCache return self.cache.cacheGet(key) File "/opt/jumpscale8/lib/JumpScale/baselib/key_value_store/store.py" Line 102, in cacheGet r=self.get("cache",key) File "/opt/jumpscale8/lib/JumpScale/baselib/key_value_store/memory_store.py" Line 21, in get raise j.exceptions.RuntimeError("Could not find object with category %s key %s"%(category,key)) ",
    masterjid: 0
}
```

if "result" is in the returned dict of the restful call, then no error has occured.
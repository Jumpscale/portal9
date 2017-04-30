Eve Grid Macro
==============

This macro is used to show Grioview based on Eve Please notice that if
you use eve in onother server you need to make sure that, X\_DOMAINS =
'\*' in settings file. And spec.json file is allwoed to reach from
another server like:

```
@app.route('/docs/spec.json')
def specs():
    return send_response(None, [get_cfg()])
```

Example
=======

```
{{evegrid:
    schema.url=':5000/system'
    spec.json.path=/docs/spec.json
    entity.name=eco
    datetime.fields=datefield1
    datetime.fields=datefield2
    sortBy =
        epoch: -1,
        pid:1,

    column.1 = 
        data:epoch,
        header:Time Stamp,
        format:<a href="/grid/eco?id={guid}">{epoch}</a>,

    column.2 = 
        data:errormessage,
        header:Error Message,

    column.3 =
        data:category,
        header:Category,

    column.4 =
        data:level,
        header:Level,

    column.5 =
        data:appname,
        header:App name,

    column.6 =
        data:pid,
        header:PID,

    column.7 =
        data:nid,
        header:Node ID,

    column.8 = 
        data:gid,
        header:GID,

    column.9 =
        data:masterjid,
        header:Master JID,
}}
```

Params
======

* **sortBy**: uses Mongo syntax where you can pass the field and (Ascending [1] or Descending[-1])
* **datetime.fields=field1** : pass to it (epoch) type field to be converted to local date time for user

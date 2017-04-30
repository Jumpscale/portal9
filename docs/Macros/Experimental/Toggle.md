Toggle
======

Macro built for boatomatic to enable and disable ports.

Parameters
----------

-   title: Title to show infront of the toggle
-   nodeid: Nodeid to control
-   cmdipaddr: IP Address to send command to

Examples
--------

### Wiki

Single toggle

```
|\{\{toggle: title:'A switch with title' nodeid:2 cmdipaddr:127.0.0.1\}\}|
```

now 4 on row

```
|\{\{toggle: nodeid:2 value:on cmdipaddr:127.0.0.1\}\}|\{\{toggle: nodeid:3 cmdipaddr:127.0.0.1\}\}|\{\{toggle: nodeid:4 cmdipaddr:127.0.0.1\}\}|\{\{toggle: nodeid:5 cmdipaddr:127.0.0.1\}\}|
```

now in table with titles at left col

```
||type||switch||
|Power|\{\{toggle: value:on nodeid:2 cmdipaddr:127.0.0.1\}\}|
|Raymarine|\{\{toggle: nodeid:2 cmdipaddr:127.0.0.1\}\}|
```

### Output

Single button

now 4 on row

now in table with titles at left col WARNING: UNSUPPORTED DOC, TABLES
NOT SUPPORT YET.

Explorer
========

Params
------

### path

-   Path to explore

#### Example

```
\{\{explorer: ppath:c:/data \}\}
```

### height

-   Hight in pixels of control

#### Example

```
\{\{explorer: hight:400 \}\}
```

### readonly

-   If files cannot be modified/uploaded
-   Remark: admin will always have right to modify & upload

#### Example

```
\{\{explorer: readonly \}\}
```

### bucket

-   Name of bucket to show in explorer
-   Do not use bucket & path at same time

#### Example

```
\{\{explorer: bucket:mydocs \}\}
```

Example
-------

```
\{\{explorer: ppath:system/system__contentmanager/ readonly height:400\}\}
```

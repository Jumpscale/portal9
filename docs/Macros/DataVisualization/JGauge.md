Gauge Macro
===========

Wiki
----

```
\{\{jgauge: id:1 width:200 height:114 val:5\}\}
    \{\{jgauge: id:2 start:200 end:800 random:50 style:black val:600 labelsuffix:A\}\}
    \{\{jgauge: id:3 width:200 height:114 val:5 random:0.5 randomspeed:300\}\}
    \{\{jgauge: id:4 start:0 end:400 random:5 randomspeed:300 style:black val:250 labelsuffix:l\}\}
```

val is the value of the arrow on the gauge

Output (without url)
--------------------

there are 2 known styles: default & black (they are predefined styles)

for style black the size is predefined on 144 for now

Most important params
---------------------

-   id : if you want to overrule the id
-   start: start of gauge in int
-   end: end of gauge in int
-   random: int of variation random
-   style: black or default
-   height & width
-   value of the gauge it is starting positioned on
-   labelsuffix what goes after label e.g. W from WATT

Other params
------------

dont use the leading '.' unsupported
image:/images/unknownspace/jgaugeParams.png !jgaugeParams.png!

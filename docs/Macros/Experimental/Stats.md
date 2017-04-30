statistics related macro's
==========================

following shows info for a specific entry mod =100 means data is
modified with 100% so not, mod=50 would mean all values/2 (ideal for
simulation)

multistatsmonth
---------------

```
\{\{multistatsmonth id:tanks.water.level.sb.1 mod:50 title:'Black Water Level Starboard Side' width:800 height:400\}\}
```

stats
-----

show statistics for 1 specific measurement

-   start & stop can be as follows: -2h 3d or 0 (means till now), always
    need to be a (not +)
-   widht & height is in pixels
-   id is the name of the counter
-   mod see above
-   maxvalues: max nr of items which will be put on graph (cols), std
    200

```
\{\{stats: id:$id start:-2h stop:-1h title:'$t1' width:$w height:$h mod:$modamount maxvalues=200\}\}
```

liststats
---------

list all know stats for the system, from these you can then click to
data & graphs

statsdata
---------

```
\{\{statsdata: id:$id start:-2h stop:-1h\}\}
```

show table with the raw data per 5 min

statsdatahour
-------------

show stats per hour data shown is

-   avg value per hour
-   max value per hour
-   min value per hour
-   nr of measurements per hour
-   total value per hour

```
\{\{statsdatahour: id:$id start:-2h stop:-1h\}\}
```

statsdataday
------------

show stats per day

data shown is

-   avg value per day
-   max value per day
-   min value per day
-   nr of measurements per day
-   total value per day

```
\{\{statsdataday: id:$id start:-2h stop:-1h\}\}
```

statsdatamonth
--------------

show stats per month

data shown is

-   avg value per month
-   max value per month
-   min value per month
-   nr of measurements per month
-   total value per month

```
\{\{statsdatamonth: id:$id start:-2h stop:-1h\}\}
```

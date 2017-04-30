
## Host based content



This is a demo which demonstrate content generation based on the
hostname.

Depending on the url the users enters specific information will be
displayed.


### How to use



You need to specify for every part 3 parameters

-   hostname: the matching hostname, if the page is visited via this
    hostname, the div with the correct divid will be enabled
-   divid: The Specific divid which should visible when the correct host
    is visiting the page
-   contentpage: name of the wiki page to include. You only need to
    specifiy the name without the .wiki, the page should be located in
    the same space

preferable in the same directory

The example below has the following structure:

Two *wiki* files:

-   test1.wiki
-   test2.wiki

And 2 hostbasedcontent macros.

```
\{\{hostbasedcontent: hostname:test1.com | divid:test1.com | contentpage:test1\}\}
  \{\{hostbasedcontent: hostname:test2.com | divid:test2.com | contentpage:test2\}\}
```

How to test:

Create in your hostfile a line matching the ipaddress of your wiki
server and test1.com and test2.com. Example hosts:

```
192.168.11.26           test1.com test2.com
```

Create two references(test1.com and test2.com) and browse to this page
this should give two different contents.

### Example

```
\{\{hostbasedcontent: hostname:test1.com | divid:test1.com | contentpage:test1\}\}
  \{\{hostbasedcontent: hostname:test2.com | divid:test2.com | contentpage:test2\}\}
```



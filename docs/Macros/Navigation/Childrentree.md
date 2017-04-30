Childrentree
============

This macro shows a tree of all the children of the current document

-   'page': Define from which page to start. Optional. Default value is
    the current page.
-   'bullets': Show the children with bullets. Optional. Default value
    is 'False'.
-   'depth': The depth of the children tree to go. Optional. The default
    is 0, causing it to view the complete children tree.
-   'no-tree': By default, the children list is viewed as tree with
    collapsed items. If 'no-tree' is specified, it will be just plain
    nested 'ul' elements, with no collapsing.
-   'items': A tree of the children to view. This can be used to show
    only some of the children in specific order. Take care that items
    must *not* be separated by spaces

Children ordering
-----------------

By default, children are sorted alphabetically. If you want to specify a
specific order to be used in all trees, you can create a file '.order'
inside the page directory, specifying the order of each page, as in this
example

```
1:ActorTaskletEngines
2:GenericSpecFormat
3:ActorSpec
4:DbTags
5:DirStructure
6:ModelSpec
```

This specifies the ordering of elements under the 'Actor' page. You can
recognize its effect in all the below examples.

The parameter 'items' overrides the '.order' behavior.

UI customization
----------------

The macro depends on 'pagetree.js' for tree behavior, and 'pagetree.css'
for default layout. These files exist in
'pylabs-core-6.0xtensionsoretmltmllibagetree'.

Examples
--------

### Default layout

```
\{\{childrentree: page:macros \}\}
```

### bullets

```
\{\{childrentree: page:Docs bullets no-tree\}\}
```

### no-tree

```
\{\{childrentree: page:Docs no-tree\}\}
```

### items

```
\{\{childrentree: items:[Macros(Children,JGauge(JGauge3,'St. Thomas'),MenuAdmin),UserManagement]\}\}
```

### depth

```
\{\{childrentree: page:Docs depth:1\}\}
```

### page

```
\{\{childrentree: page:Macros \}\}
```

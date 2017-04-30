Demo Gallery
============

Macro syntax
------------

The gallery macro has three optional keywords:

-   'picturedir': sub directory in '*spacename*/.files/img', e.g.
    'testimages3' will point to 'Docs/.files/img/testimages3'. If you
    don't specify the picturedir, the local directory of the wiki page
    will be selected.
-   'title': Title printed on the gallery viewer
-   'thumb\_size': The size of the thumbnail images which are viewed in
    the main gallery, in the format
    '\<em\>width\</em\>x\<em\>height\</em\>' e.g. '300x200'. If this
    option is not passed to the macro, it will be read from the file
    '.params.cfg'. If the file '.params.cfg' is not available, then the
    size will be '150x100'.

Later we will add bucket support.

Examples
--------

-   'gallery: picturedir: testimages3 | title: test': This will search
    for images in '*space*/.files.img/testimage'
-   'gallery': This will list all the images in the local directory
    (supported formats: jpg, jpeg, bmp, gif, png)
-   'gallery: title:demo': This will list all the images in the local
    dir and use 'demo' as title

Demo
----

If you write this in your page

```
\{\{gallery: picturedir: | title:demo | thumb_size:300x200\}\}
```

This will be the result

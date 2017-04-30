Thumbnail
=========

Macro syntax
------------

The thumbnail macro has a 3 parameters

-   'picture\_path': The path to the picture, *without* space name, e.g.
    '.files/img/testimages3/test1.jpg'. This parameter is mandatory.
-   'thumb\_size': The size of the thumbnail, as in the format
    '\<em\>width\</em\>x\<em\>height\</em\>' e.g. '300x200'. It can be
    specified for the whole website (or folder) in the file
    '.params.cfg', or it can be specified explicitly as a parameter. If
    it's not specified in either of them, then the default thumb size
    will be 150x100. This parameter is optional.
-   'exact\_size': If this parameter is specified, then the generated
    thumbnail will be *exactly* of the specified size. If this parameter
    is not specified, the generated thumbnail will keep the aspect ratio
    of the original image.

Demos
-----

```
\{\{thumbnail:.files/img/tiger.jpg\}\}
```

```
\{\{thumbnail:.files/img/tiger.jpg 200x100\}\}
```

```
\{\{thumbnail:.files/img/tiger.jpg 500x200 exact_size\}\}
```

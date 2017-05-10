# Macros

JumpScale Portal comes shipped with a big variety of macros.

The portal supports three kind of macros.

For details how to write macros please see the [HowTo](/Howto.md) section.

## Description

A macro is a block inside the WIKI content which get processed on the server side of the portal server. It can be used to retrieve extra data.

## Location

Macros can be stored as system macros or on a per space basis.

* `spacepath/.macros/`
* `apps/portals/portalbase/macros/`

Under these paths we should have three subpaths `page`, `wiki` and `preprocess`

## Wiki Macros

Wiki macros replace with body of the macro with new wiki syntax and can write out new macros in its turn.
The [doc](https://github.com/Jumpscale/jumpscale_portal/blob/master/lib/portal/docpreprocessor/Doc.py) object get passed to the params of these macros.

[Examples](https://github.com/Jumpscale/jumpscale_portal/tree/master/apps/portalbase/macros/wiki)

## Page Macros

Page macros work on a high level of the document and manipulate the HTML itself. The [page](https://github.com/Jumpscale/jumpscale_portal/blob/master/lib/portal/docgenerator/PageHTML.py) object gets passed to the params which makes it easy to add CSS or JavaScript to the document.

[Examples](https://github.com/Jumpscale/jumpscale_portal/tree/master/apps/portalbase/macros/page)

## Preprocess macros

Currently only [include](https://github.com/Jumpscale/jumpscale_portal/tree/master/apps/portalbase/macros/preprocess/include) uses the preprocessor macro.

[Examples](https://github.com/Jumpscale/jumpscale_portal/tree/master/apps/portalbase/macros/preprocess)

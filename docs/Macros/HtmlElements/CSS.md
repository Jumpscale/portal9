CSS Macro
=========

This macro is used to add CSS file to a page, or remove one

Example
=======

```
#following will remove bootstrap.min.css from page & add another one
\{\{css:/$$space/.files/test.css exclude:bootstrap.min.css\}\}
```

You can now inspect the loaded CSS resources on the page to find that
test.css is now included

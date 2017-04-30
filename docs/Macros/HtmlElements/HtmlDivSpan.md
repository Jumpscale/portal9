Span
====

A div/span macro, like the one in Confluence. In practice, this supports
any macro in this format:

and all attributes will be converted to HTML attributes. To close the
macro, use the same macro name without any parameters, like:

Wiki:
-----

The generated HTML will be:

```
<div>
    <div id="left-panel" class="clearbox column8">
        <span id="span1">Text inside</span>
    </div>
</div>
```

Output
------

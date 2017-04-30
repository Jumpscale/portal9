ListDocs
========

View a list of documents, based on these criteria

-   'name': A regular expression used to match the document name or
    alias. This is case-insensitive.
-   'parent': The name of the parent, case-insensitive.
-   'types': A comma separated list of document types. The document is
    selected if the document matches any of types.
-   'products': A comma separated list of document products. The
    document is selected if the document matches any of products.

Example
-------

```
\{\{listdocs: name:code\}\}
```

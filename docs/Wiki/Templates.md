How templates works
===================

Instead of repeating the commont layout inside each wiki page, they can
get their layout from a template.

The template must contain the placeholder '{content}'. During rendering,
the content of the wiki page is inserted in place of the placeholder,
and the combined result is returned to the user.

There are 3 different ways of specifying the template of the page

-   Specify the template explicitly using the <'@template>' directive,
    e.g. <'@template> blog\_post', which will load the template from
    '.space/blog\_post.wiki'.
-   A wiki page inside a folder of the same name (e.g. Blogs/Blogs.wiki)
    will use the template '.space/default.wiki'. If you want to specify
    another template, either use the <'@template>' directive, or use the
    <'@nodefault>' directive & create your own layout.
-   A wiki page inside a folder of a different name will not use any
    template, unless it uses the <'@template>' directive or the
    <'@usedefault>' directive, which will use the '.space/default.wiki'.

Example of page with custom template
------------------------------------

```
@template blog_post

Content of the page with custom template
```

Example of page with default template
-------------------------------------

```
@usedefault

Content of the page with default template
```

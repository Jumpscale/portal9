Configuring a Space
===================

A space is a collection of pages. Every page in a space must have a
unique name. Every space can be configured independently, with its own
style and user management. All configuration files of a space are stored
in the .space directory, located in the root of the space.

In this section you find the list of configuration files that can be
used in a space.

acl.cfg
-------

In the acl.cfg configuration file, you can define the different rights
to the defined groups. The following rights can be assigned:

-   R: read-only
-   W: read/write
-   S: synchronize the documentation to a local file system
-   A: administrator right
-   : all rights

The definition of user and group rights has the following structure:

\<group name\>: \<rights\> \<user name\>: \<rights\>

default.wiki
------------

The default.wiki file is the landing page of the space. This page
defines the default parameters of the space. In this page you define the
different sections that each page of the space will contain.

The following parameters are accepted:

-   'title': defines the name that appears on your Internet browser's
    tab and title bar.
    -   Usage: 'title: \<your title\>'
-   'projectname': the name of your complete project, not limited to the
    documentation.
    -   Usage: 'projectname: \<your project name\>'
-   'find': adds a search box to find information in the space.
    -   Usage: 'find'
-   'menu': adds a menu item to the horizontal menu bar.
    -   Usage: \`menu:

\<menu label\>: \<root page name\>\`

-   'menuadmin': adds the administrator menu to the horizontal menu bar.
    -   Usage: 'menuadmin'
-   'navigation': adds a navigation menu.
    -   Usage: 'navigation'
-   'content': adds the content of the wiki pages that you create.
    -   Usage: 'content'
    -   Single curly braces instead of double curly braces!

To define the sections of each page, you have the following parameters:

-   'block': displays a table in which you can define rows and columns.
    For example, when you want to add a fixed footer, you can add a
    block for the content and another one for the footer.
-   'row': creates a row in a block.
-   'col': creates a column in a block. You can add the width of the
    column as extra parameter, for example col 3.
-   'divend': indicates the end of an HTML div section.

nav.wiki
--------

This page is the default navigation page of the space. The page is used
by the navigation macro.

notfound.wiki
-------------

This page is shown when a requested page can not be found. This page
will replace the default HTTP Not Found page. You can put any
information on this page, using the default wiki style.

template.wiki
-------------

The template.wiki file is the default wiki file which is used as
template when a new page is created in the space.

Publishing the space on its URL
===============================

nginx is a web server just like Apache & IIS. If you want to make a
space has its own URL, you need to configure nginx.

-   Login to nginx machine 172.19.49.230 (ask Tomas for access)
-   'cd /etc/nginx/sites-available/'
-   Create a new configuration file with the URL, e.g.
    'www.my\_space.com.conf'. It works for subdomains also, e.g.
    'docs.my\_space.com.conf'
-   Add this content to the file (we will use 'www.my\_space.com' as an
    example)

```nginx
server {
        access_log  /var/log/nginx/www.my_space.com.log ;
        listen 80;

        server_name www.my_space.com;

        location / {
                proxy_set_header        X-Real-IP       $remote_addr;
                proxy_pass http://172.19.49.185/my_space/; # Put the space here
        }

        location /my_space {
                proxy_set_header        X-Real-IP       $remote_addr;
                proxy_pass http://172.19.49.185/my_space;
        }

        location /images {
                proxy_set_header  X-Real-IP $remote_addr;
                proxy_pass http://172.19.49.185/images;
        }


        location /lib {
                proxy_set_header        X-Real-IP       $remote_addr;
                proxy_pass http://172.19.49.185/lib/;
        }

        location /restmachine {
                proxy_set_header        X-Real-IP       $remote_addr;
                proxy_pass http://172.19.49.185/restmachine/;
        }

}
```

contact\_form
=============

'contact\_form' macro will create a 'Contact us' form which will send an
email message to a specified email address give to the macro. The form
will be composed of 3 fields

-   Sender name
-   Sender email
-   Body

There are 3 optional parameters that you can use to specify which SMTP
server will be used for sending the email

-   'smtp\_server': The IP & port of the SMTP server. The default value
    is 'smtp.gmail.com:587'
-   'smtp\_login': The login of the SMTP server. The default value is
    <'smtp@incubaid.com>'
-   'smtp\_password': The password of the SMTP server. The default value
    is 'smtp987smtp'

This is a sample of the default layout & behavior

```
\{\{ contact_form: receiver_email:info@incubaid.com \}\}
```

Custom layout
-------------

Another sample with custom layout

```
\{\{ contact_form: receiver_email:info@incubaid.com | custom | subject: Custom title for email\}\}
    \{\{div: class=control-group\}\}
        \{\{ email: name=sender_email | required | placeholder= The email\}\}
    \{\{div\}\}
    \{\{div: class=control-group\}\}
        \{\{ text: name=sender_name | required=true | placeholder= whatever title\}\}
    \{\{div\}\}
    \{\{div: class=control-group\}\}
        \{\{ text: name=age | required=true | placeholder=Your age\}\}
    \{\{div\}\}
    \{\{div: class=control-group \}\}
        \{\{ textarea: rows=10 | cols=20 | required | name=body\}\}
    \{\{div\}\}
    \{\{dropdown: name=single_option | id=single_option
        * option 1
        * option 2
        * option 3.1
        ** option 3.1.1 
        ** option 3.1.1.1.1.1
        ** option 3.1.1.1.1.2
        ** option 3.2
        * option 3
    \}\}

    \{\{dropdown: name=multiple_options | id=multiple_options | multiple
        * option 1
        * option 2
        * option 3.1
        ** option 3.1.1 
        ** option 3.1.1.1.1.1
        ** option 3.1.1.1.1.2
        ** option 3.2
        * option 3
    \}\}

    \{\{div: class=control-group\}\}
        \{\{ submit: class=btn btn-primary | data-loading-text=Sending... \}\}
            Send the big email
        \{\{submit\}\}

        \{\{ reset \}\}
    \{\{div\}\}
\{\{ contact_form \}\}
```

Send the big email

Below you will find a list of all input macros. All of them accept HTML
attributes, with this format

```
\{\{text: name=single_option | id=single_option | class=btn btn-primary | style=font-weight: bold | data-loading-text=Sending... \}\}
```

### text

This is a single-line input field, accepting free-form text

### textarea

A large input field, accepting free-form text

### email

A single-line input field, accepting emails only.

### dropdown

An input control which allows the user to use a single option or
multiple options.

### Options

-   'multiple': allows selecting multiple options. Without it, the user
    can select only a single option
-   All other HTML attributes

### submit

Creates a button which will submit the form to the server.

### reset

Creates a link which will clear the form data when clicked.

Storage
-------

By default, all emails are stored in '\<system
space\>/.space/emails.json'.

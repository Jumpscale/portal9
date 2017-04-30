Steps
=====

To create an actor, you have to follow these steps:

1.  Under your space or base folder, create a new folder named as follows
    **spacename\_\_actorname** (will be referred to as actor folder
    later on)
2.  Under your actor folder, create the following folders: **.actor**,
    **methodclass**, **specs** and **extensions**
3.  **Specs** folder will hold your .spec files. You should create an
    actors.spec as an entry point, and start spec'ing your actor methods
    (names, parameters, documentation, etc)
4.  **Methodclass** folder will hold the actual methods implementations
5.  **Extensions** folder will contain any extension or let's say any
    library or helper code, that may be used by your actor methods
6.  **actor** folder will basically contain 2 files, main.cfg and
    acl.cfg

-   main.cfg will contain basically a 'main' section with a single entry
    id=spacename}\_\_actorname}
-   acl.cfg will be just an empty file

Example
-------

Let's assume that we have an already created app *myapp* with a single
space *myspace*. We will create the folder structure as described above.
We will create a simple actor named *test* with a single method *print*
which prints an input string param passed to it

**actors.spec**

```cfg
[actor]
    """
    Test actor
    """
    method:echo @noauth
        var:input str,,
        result:str

    method:sum
        """
        Doc string for sum method
        Requires authentication (aka logged in user)
        """
        var:a int,1,input a with default value 1
        var:b int,,input b without default value
        result:int

    method:substract
        """
        Doc string for substract method
        Requires authentication (aka logged in user)
        variable `a` is optional, default value will be used if ommited
        """
        var:a int,1,input a with default value 1 @optional
        var:b int,,input b without default value
        result:int

```

**methodclass/myspace\_test.py**

```python
class myspace_test(object):

    def echo(self, input, *args, **kwargs):
        return input

    def sum(self, a, b, *args, **kwargs):
        return a + b

    def substract(self, a, b, *args, **kwargs):
        return a - b

```

**.actor/main.cfg**

```cfg
[main]
id = myspace__test
```

## Raising http errors

Following example will return a 404 message with header application/json.
For full list of available exceptions see [github](https://github.com/jumpscale/jumpscale_portal/blob/master/lib/portal/portal/exceptions.py)

```python
from JumpScale.portal.portal import exceptions
class myspace_test(object):

    def echo(self, input, *args, **kwargs):
        raise exceptions.NotFound("Could not find console to echo to")
```
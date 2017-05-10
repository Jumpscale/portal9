## How to delete a service instance

You can delete a repository in multiple ways:

- [In the Cockpit Portal](#portal)
- [Using the Cockpit API](#api)
- [At the CLI](#cli)


<a id="portal"></a>
### Using the Cockpit Portal

@todo


<a id="api"></a>
### Using the Cockpit API

In order to use the Cockpit API you first need to obtain an JWT, as documented in the section about [how to get a JWT](../Get_JWT/Get_JWT.md).

Once you got the JWT:

```
curl -X DELETE
     -H "Authorization: bearer JWT"  /
     -H "Content-Type: application/json" /
     -d '{"name":"test-repo"}'
     https://BASE_URL/api/ays/repository/{repository}/service/{role}/{instance}
```

In the **API Console**:

![](delete-service.png)

For more information about the **API Console** go to the section about the [API Console](../../API_Console/API_Console.md).


<a id="cli"></a>
### At the CLI

@todo

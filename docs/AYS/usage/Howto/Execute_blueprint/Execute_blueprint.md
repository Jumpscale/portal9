## How to execute a blueprint

Executing a blueprint means that you will initialize all service instances as described in the blueprint.

You can execute a blueprint in three ways:

- [Using the Telegram Chatbot](#telegram)
- [In the Cockpit Portal](#portal)
- [Using the Cockpit API](#api)
- [At the CLI](#cli)

<a id="telegram"></a>
### Using the Telegram Chatbot

@todo


<a id="portal"></a>
### Using the Cockpit Portal

See the [Getting started with blueprints](../../Getting_started_with_blueprints/getting_started_with_blueprints.md) section.


<a id="api"></a>
### Using the Cockpit API

In order to use the Cockpit API you first need to obtain an JWT, as documented in the section about [how to get a JWT](../Get_JWT/Get_JWT.md).

Once you got the JWT, you can execute a blueprint:

```
curl -H "Authorization: bearer JWT"  /  
     https://BASE_URL/api/ays/repository/REPOSITORY-NAME/blueprint/BLUEPRINT-NAME
```

For instance in order to execute the blueprint discussed in the section [How to create a blueprint](../Create_blueprint/Create_blueprint.md):

```
curl -H "Authorization: bearer JWT"  /  
     https://BASE_URL/api/ays/repository/REPOSITORY-NAME/blueprint/user1.yaml
```

> Note that once executed the user still is not created. One more step is required, that is executing the install action on the user1 service instance, as documented in the section [How to install a service](Install_service/Install_service.md).

Also see the section about the [API Console](../../API_Console/API_Console.md)

<a id="cli"></a>
### At the CLI

Navigate to your repo.

Use the following command to execute blueprints:

`ays blueprint`

The above command will execute all the blueprints in the repo. To execute a specific blueprint, you can specify the name of the blueprint as follows:

`ays blueprint {blueprint name}.yaml`

## How to create a blueprint

You can create a blueprint in multiple ways:

- [Using the Telegram Chatbot](#telegram)
- [In the Cockpit Portal](#portal)
- [Using the Cockpit API](#api)
- [At the CLI](#cli)

All are discussed here below.

Make sure to validate your blueprint first to have valid YAML format using a tool like [YAML Lint](http://www.yamllint.com/).


<a id="telegram"></a>
### Using the Telegram Chatbot

@todo


<a id="portal"></a>
### Using the Cockpit Portal

See the [Getting started with blueprints](../../Getting_started_with_blueprints/getting_started_with_blueprints.md) section.


<a id="api"></a>
### Using the Cockpit API

In order to use the Cockpit API you first need to obtain an JWT, as documented in the section about [how to get a JWT](../Get_JWT/Get_JWT.md).

Once you got the JWT, you can create a blueprint, for instance here below for creating a new user "mike" on gig.demo.greenitglobe.com:

```
curl -H "Authorization: bearer JWT"  /
     -H "Content-Type: application/json" /
     -d '{"name":"user1.yaml","content":"ovc_user__user1:\n  g8.client.name: 'gig'\n  username: 'mike'\n  email: 'mike@gmail.com'\n  provider: 'itsyouonline'"}'
     https://BASE_URL/api/ays/repository/
```

> Note that the above blueprint will not create the user. Two more steps are are required for that, first execute the blueprint and then install the user, respectively documented in the sections [How to execute a blueprint](../Execute_blueprint/Execute_blueprint.md) and [How to install a service](Install_service/Install_service.md).

Also see the section about the [API Console](../../API_Console/API_Console.md)

<a id="cli"></a>
### At the CLI

Navigate to your blueprints subdirectory in your repo.

Using your preferred text editor (in this example vim) create a new YAML file.

`vim user1.yaml`

To create a new virtual data center, paste this code in the new file:

```yaml
g8client__dubai:
  url: 'gig.demo.greenitglobe.com'
  login: 'yves'
  password: '****'
  account: 'Demo Account'

vdc__demo1:
  g8.client.name: 'dubai'
  g8.location: 'du-conv-1'
  maxMemoryCapacity: 2
  maxVDiskCapacity: 10
  maxCPUCapacity: 2
  maxNASCapacity: 20
  maxArchiveCapacity: 20
  maxNetworkOptTransfer: 5
  maxNetworkPeerTransfer: 15
  maxNumPublicIP: 1
```
It is now possible to execute the blueprint as documented in [Execute_blueprint](../Execute_blueprint/Execute_blueprint.md).

Also see [How to add a user](../Add_user/Add_user.md).

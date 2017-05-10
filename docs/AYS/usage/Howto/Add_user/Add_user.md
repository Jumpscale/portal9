## How to add a user

First step will be to create a user in ItsYou.online.

Then use following blueprint to add a user to a G8 environment:

```yaml
ovc_user__user1:
  g8.client.name: ‘$instance_name_of_g8_client_connection$’
  username: ‘$username_xyz$’
  email: ‘$xyz@vreegoebezig.be$’
  provider: 'itsyouonline'
```

The first parameter **$instance_name_of_g8_client_connection$** is the name of the G8 client connection service instance to be used by the Cockpit. This service instance needs to be existing in the same repository. If not already created previously, add it to your blueprint:

```yaml
g8client__$instance_name_of_g8_client_connection$:
  g8.url: '$G8_URL$'
  g8.login: '$username$'
  g8.password: '****'
  g8.account: '$$'
```

Hereby:
- The G8 URL is the http address of the G8 node, e.g. **gig.demo.greenitglobe.com**
- The G8 login is the ItsYou.online username of the user with administrative rights on the G8 system
- The G8 account is the account

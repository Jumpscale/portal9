# Portal client

The API available for the portal can be accessed using the portal client.

`portal_client = j.clients.portal.get(ip={portal-address}, port={portal-port})`

To have access to the different portal API groups, the portal client needs to be first authenticated with a user on the portal.

`portal_client.system.usermanager.authenticate(name={user}, secret={password})`

It is now possible to load the API groups using the following command:

`portal_client.load_swagger()`

For loading specific API groups:

`portal_client.load_swagger(group={name of group})`

To use the client:

`portal_client.{group name}.{actro name}.{method}`

For example:

`portal_client.ays.tools.listBlueprints(repository={name of ays repo})`

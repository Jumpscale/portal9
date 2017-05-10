## How to get a JWT

In order to use the **Cockpit API** a JSON Web Token (JWT) is needed. The Cockpit will use this JWT in order check if your application (code) was granted the right to interact with the Cockpit on behalf of the user of organization for which the Cockpit was setup.

A JWT is requested from ItsYou.online, and requires an OAuth access token, which you first also need to request from ItsYou.online, as documented in the section about [How to get an OAuth access token](../Get_oauth_access_token/Get_oauth_access_token.md).

Once you've got the OAuth access token, the JWT is requested as follows.

- If on behalf of a user:

  ```
  curl -H "Authorization: token OAUTH-TOKEN" /
       https://itsyou.online/v1/oauth/jwt?scope=user:memberof:org1
  ```

- Or, if on behalf of the organization for which the Cockpit was set-up:

  ```
  curl -H "Authorization: token OAUTH-TOKEN" /
       https://itsyou.online/v1/oauth/jwt?aud=client_id
  ```

In the above:
- **scope=user:memberof:client_id** claims that the user is member of the organization identified with **client_id**
- **aud=client_id** claims that the JWT was issued for the organization identified with **client_id**

Also see:
- The [ItsYou.online documentation](https://www.gitbook.com/book/gig/itsyouonline/details), specifically the sections about [JWT Support](https://gig.gitbooks.io/itsyouonline/content/oauth2/jwt.html) and [ItsYou.online API Console](https://itsyou.online/apidocumentation)
-[Generating JWT tokens](../JWT/JWT.md)

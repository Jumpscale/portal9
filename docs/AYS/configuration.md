# Configuration

The Cockpit uses [ItsYou.online](https://itsyou.online/) to authenticate users.

A Cockpit is always deployed for a specific organization that needs to be registered at [ItsYou.online](https://itsyou.online/).

In order to make sure only members of this organization can interact with the Cockpit we use OAuth 2.0:

- For the REST API we use [JWT](https://jwt.io/) tokens to authenticate all requests
- For the Telegram chatbot we request the user to authenticate on [ItsYou.online](https://itsyou.online/) and authorize the chatbot to check that the user is member/owner of the organization for which the Cockpit is setup


## Cockpit configuration file & manually starting your chatbot

This configuration file is generated automatically during the deployment of the Cockpit.

For development purposes, you can also create the configuration file manually, and start a new Cockpit server manually.

Here is an example in 3 steps:
- Step 1: Create the configuration file
- Step 2: Create a new Telegram chatbot and get an API token for it
- Step 3: Start your Cockpit server


### Step 1: Create the configuration file

```toml
[oauth]
client_secret = 'okla3Z2PLNmxu9sdfgrtFaOyBlCmOz4OeNW-V1lJh66OBtuqkk7_5H'
client_id = 'MyID'
redirect_uri = 'https://mycockpit.aydo.com/oauth/callback'
organization = 'MyID'
jwt_key = "-----BEGIN PUBLIC KEY-----\nMHYwEAYHKoZIzj0CAQYFK4EEACIDYgAES5X8XrfKdx9gYayFITc89wad4usrk0n2\n7MjiGYvqalizeSWTHEpnd7oea9IQ8T5oJjMVH5cc0H5tFSKilFFeh//wngxIyny6\n6+Vq5t5B0V0Ehy01+2ceEon2Y0XDkIKv\n-----END PUBLIC KEY-----"
itsyouonlinehost = 'https://itsyou.online'

[api.ays]
active = true
host = "0.0.0.0"
port = 5000

[bot]
token = "205766488:AAEizYAolZddhL-G21oOM5JL1lmOf9slh4s"

[mail]
host = "0.0.0.0"
port = 25
```


### Step 2: Create a new Telegram chatbot and get an API token

- Connect to Telegram and talk to @botfather
- Execute the command `/newbot` and choose a name and username for your chatbot
- @botfather should give you a token, add it to the `main.py` file


Add a commands description to your chatbot:

- Type `/setcommands` in @botfather, choose your chatbot and paste following lines:

  ```
  start - Start discussion with the bot
  repo - Manage your AYS repositories
  blueprint - Manage your blueprints project
  service - Perform actions on your service instances
  help - Show you what I can do
  ```


### Step 3: Start your Cockpit

```bash
jspython cockpit start --config config.toml
```


## Cockpit CLI commands

```
./cockpit --help
Usage: cockpit [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  clean_cache  Empty Oauth cache for telegram bot
  start        Start cockpit server

```

- **start** starts the Cockpit server
- **clean_cache**: empties the cache that stores oauth authentification for Telegram chatbot
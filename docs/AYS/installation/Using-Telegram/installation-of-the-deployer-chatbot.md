# Installation of the Cockpit Deployer Chatbot

This Telegram chatbot is used to allow people to easily deploy a Cockpit.

This chatbot is composed of two components:

- the chatbot itself
- a small [Flask](http://flask.pocoo.org/) app that is used to receive callbacks from ItsYou.online for OAuth 2.0 workflow

Both need to be started for the chatbot to work properly.


## How to start the chatbot

To start the chatbot you can use the little **telegram-bot** CLI command:

```bash
Usage: telegram-bot [OPTIONS]

Options:
  -c, --config TEXT  path to the config file
  --help             Show this message and exit.

```

By default the chatbot looks for a `config.yaml` file in the current directory, but you can specify a path using the `--config` argument.

Here a example of the required configuration:

```yaml
bot:
    # bot token from @botfather
    token: "205766488:AAEizHUvxZddhL-G21oOM5JL1lmOf9slh4s"

# address of the G8 you want to propose to the users
# during deployment.
g8:
    - gig-demo-greenitglobe:
        address: "gig.demo.greenitglobe.com"
    - g8.be-g8-1:
        address: "be-g8-1.demo.greenitglobe.com"

# credentials for the dns cluster.
# if you don't specify the credentials, they will be ask to the user during deployment
dns:
    login: "login"
    password: "password"
    sshkey: "path of private key"

oauth:
    host: '0.0.0.0'
    port: 5000
    # adress of you oauth server where itsyouonline should send callback. Make sure the same URL is used in itsyou.online.
    redirect_uri: "https://deployerbot.com/callback"
    # CLient ID from your app on itsyou.online
    client_id: 'myId'
    # CLient secret from your on in itsyou.online
    client_secret: 'IuDUBE--6NMQS1OH-UmcOijhT7Uq2lPdWnJ74hMSMqgKjjQhtZDC'
    itsyouonlinehost: "https://itsyou.online"
```

Make sure the `May be used in client credentials gran type` is enable when creating the client secret for this chatbot.

### DNS config

To have more details about how to configure the DNS part, check https://gig.gitbooks.io/ovcdoc_internal/content/InternalIT/internal_it.html.
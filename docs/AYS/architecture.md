# Architecture

The cockpit is composed of multiple components.

These servers communicate using queues on Redis.

{% plantuml %}
@startuml
title Cockpit
[REST Server] as rest
[Mail Server] as mail
[AYS Daemon] as daemon
[Telegram Chatbot] as telegram
database "Redis" {
  node queue{
  }
}

rest .up. HTTP : use
mail .down. SMTP : use
telegram .down. TelegramChatbotAPI : use

rest -down-> queue : send
mail -left-> queue : send
daemon <-right- queue : receive
telegram -up-> queue: send

@enduml

{% endplantuml %}

## Components

### AYS Daemon

This daemon is responsible for executing the recurring actions of services and listent to events sends from other components. For example when an mail is received from
the SMTP server, an event is send to the daemon so it can fires the corresponding actions of the services that subscribed to the events of type mail.


### Mail

The Mail module implements a Simple SMTP server.

It saves the attachments of mails locally and generates an event for every mail it received.


### Telegram Chatbot

Holds the logic for all communication over Telegram.

Some of the chatbot commands generate:

- project create/delete
- action execute


### REST Server

It's a flask REST Server, it exposes the AYS REST APIs.
Some of the endpoint expose by the API are asyncronous. In this case, the REST server forward the request to the AYS daemon.
The daemon then execute the requested action and can notify the caller via a webhooks when the actions has finishes.
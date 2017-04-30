import smtplib
import os
from js9 import j

ujson = j.data.serializer.serializers.getSerializerType('j')


class system_emailsender(j.tools.code.classGetBase()):

    """
    Email sender
    """
    # Maybe we can add this later
    output_format_mapping = {
        'json': ujson.dumps
    }

    def __init__(self):
        self._te = {}
        self.actorname = "emailsender"
        self.appname = "system"

    def format(self, obj, format=None):
        if not format or format not in self.output_format_mapping:
            format = 'json'
        output_formatter = self.output_format_mapping[format]
        return output_formatter(obj)

    def send(self, sender_name, sender_email, receiver_email, subject, body, smtp_key, format, *args, **kwargs):
        """
        param:sender_name The name of the sender
        param:sender_email The email of the sender
        param:receiver_email The email of the receiver
        param:subject Email subject
        param:body Email body
        param:format The request & response format of the HTTP request itself
        result 'Success' in case of success, or 'Failure: ERROR_MSG' in case of the error message.
        """

        # The idea behind honeypots is simple. Most spamming bots are stupid & fill all the form fields, so if I put
        # an invisible field in the form it will be filled by the bot, but not by humans.
        #
        # For better protection, I can encode the names & IDs of the fields here, but this should be done at a later
        # time
        honeypot = kwargs.pop('honeypot', None)
        if honeypot:
            return 'Error: SPAMMER'

        kwargs.pop('ctx', None)

        # TODO: configure mail client to use ut
        # smtp_server, smtp_login, smtp_password = j.apps.system.contentmanager.dbmem.cacheGet(smtp_key)

        if sender_name:
            sender = '{0} <{1}>'.format(sender_name, sender_email)
        else:
            sender = sender_email

        # This is the same email pattern used in `contact_form` macro
        # TODO: abstract it in one place
        email_pattern = r"^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)+$"
        if not j.tools.code.regex.match(email_pattern, receiver_email):
            return 'Error: receiver email is not formatted well.'
        if not j.tools.code.regex.match(email_pattern, sender_email):
            return 'Error: your email is not formatted well.'

        receivers = [receiver_email]
        kwargs['sender'] = sender_email

        if kwargs:
            other_params = []
            for k, v in list(kwargs.items()):
                if isinstance(v, list):
                    v = ', '.join(v)
                other_params.append('<tr><th>{0}</th><td>{1}</td></tr>'.format(k, v))

            body = body + '<br /><table border=1>{0}</table>'.format(''.join(other_params))

        self.save_emails(sender_name, sender_email, receiver_email, subject, body, *args, **kwargs)
        j.clients.email.send(receivers, sender, subject, body)

        return 'Success'

    def save_emails(self, sender_name, sender_email, receiver_email, subject, body, *args, **kwargs):
        system_path = j.portal.server.active.getSpace('system').model.path
        emails_file = os.path.join(system_path, '.space', 'emails.json')
        try:
            emails = j.data.serializer.serializers.json.loads(open(emails_file).read())
        except IOError:  # File doesn't exist yet
            emails = []

        emails.append({
            'sender_name': sender_name,
            'sender_email': sender_email,
            'receiver_email': receiver_email,
            'subject': subject,
            'body': body,
            'args': args,
            'other_data': kwargs
        })

        open(emails_file, 'w').write(j.data.serializer.serializers.json.dumps(emails))

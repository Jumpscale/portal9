Loading and working with actors remotely
========================================

In order to be able to connect to a remote appserver, you'll have to
provide the following to the getPortalClient call:

1.  ip: the IP of the remote appserver
2.  port: the port on which Nginx is listening
3.  secret: appserver secret token

```python
import JumpScale.portal
cl = j.clients.portal.get(ip='<REMOTE-APPSERVER-IP>', port=82, secret="1234")
```

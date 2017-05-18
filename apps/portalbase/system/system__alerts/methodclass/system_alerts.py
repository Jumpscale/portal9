from js9 import j


class system_alerts(j.tools.code.classGetBase()):

    """
    Alerts handler

    """

    def __init__(self):

        self._te = {}
        self.actorname = "alertshandler"
        self.appname = "system"
        self.alertmodel = j.portal.tools.models.system.Alert

    def update(self, state, alert, comment=None, username=None, **kwargs):
        alert_obj = self._update(state, alert, comment=None, username=None, **kwargs)
        attrs = {'state': state, 'alert': alert,
                 'comment': comment, 'username': username}
        attrs.update(**kwargs)
        for attr in attrs:
            if attr == 'ctx':
                continue
            setattr(alert_obj, attr, eval(attr))
        alert_obj.save()
        return True

    def _update(self, state, alert, comment=None, username=None, **kwargs):
        """
        process eco
        first find duplicates for eco (errorcondition obj of style as used in this actor)
        the store in db
        """
        if not j.portal.tools.models.system.Alert.exists(alert):
            raise RuntimeError('Invalid Alert')

        alert_obj = j.portal.tools.models.system.Alert.get(alert)

        if username and not j.portal.tools.models.system.Alert.find({'username': username})[0]:
            raise RuntimeError('User %s does not exist' % username)

        username = username or kwargs['ctx'].env['beaker.session']['user']
        comment = comment or ''
        epoch = j.data.time.getTimeEpoch()

        history = {'user': username,
                   'state': state,
                   'comment': comment,
                   'epoch': epoch}

        alert_obj.state = state

        alert_obj.history.append(history)
        return alert_obj

    def escalate(self, alert, username=None, comment=None, **kwargs):
        alert_obj = self._update('ALERT', alert, comment, username, **kwargs)
        alert_obj.level += 1
        alert_obj.save()
        return True

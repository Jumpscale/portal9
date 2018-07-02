from js9 import j

db = j.portal.tools.models.system.User._get_db()
db.user.update({}, {'$unset': {'authkey': ""}}, multi=True)
for user in j.portal.tools.models.system.User.find({}):
    authkeys = {}
    for authkey in user.authkeys:
        authkeys[authkey] = authkey
    user.authkeys = authkeys
    user.save()

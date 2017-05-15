from beaker.container import NamespaceManager
from js9 import j


class MongoEngineBeaker(NamespaceManager):

    def __init__(self, id, namespace_args, **kwargs):
        self.namespace = id

    def __getitem__(self, key):
        item = j.portal.tools.models.system.SessionCache.get(guid=self.namespace)
        if item:
            value = item.to_dict()
            kwargs = value.pop('kwargs', {})
            value.update(kwargs)
            return value
        else:
            raise KeyError(self.namespace)

    def __setitem__(self, key, value):
        user = value.pop('user', None)
        if not user:
            self._remove(self.namespace)
            return
        elif user == 'guest' and not value:
            return
        sessioncache = j.portal.tools.models.system.SessionCache()
        sessioncache._expire_at = value.pop('_expire_at', None)
        sessioncache._creation_time = value.pop('_creation_time', None)
        sessioncache._accessed_time = value.pop('_accessed_time', None)
        sessioncache.guid = self.namespace
        sessioncache.user = user
        sessioncache.kwargs = value
        sessioncache.save()

    def _remove(self, key):
        sessioncache = j.portal.tools.models.system.SessionCache.get(self.namespace)
        if sessioncache:
            sessioncache.delete()

    def __contains__(self, key):
        key = "%s_%s" % (self.namespace, key)
        return j.portal.tools.models.system.SessionCache.exists(key)

    def __delitem__(self, key, **kwargs):
        self._remove(key)

    def acquire_read_lock(self, **kwargs):
        return True

    def release_read_lock(self, **kwargs):
        return True

    def acquire_write_lock(self, **kwargs):
        return True

    def release_write_lock(self, **kwargs):
        return True

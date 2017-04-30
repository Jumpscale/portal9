from beaker.container import NamespaceManager


class MinimalBeaker(NamespaceManager):

    def __init__(self, id, namespace_args, **kwargs):
        self._namespace = 'Home'
        self._category = 'sessioncache'
        self.namespace = id
        self._client = None

    def __getitem__(self, key):
        return

    def __setitem__(self, key, value):
        pass

    def _remove(self, key):
        pass

    def __contains__(self, key):
        return True

    def __delitem__(self, key, **kwargs):
        pass

    def acquire_read_lock(self, **kwargs):
        return True

    def release_read_lock(self, **kwargs):
        return True

    def acquire_write_lock(self, **kwargs):
        return True

    def release_write_lock(self, **kwargs):
        return True

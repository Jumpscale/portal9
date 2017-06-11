class async(object):
    def __init__(self, title, success, error):
        self._title = title
        self._success = success
        self._error = error

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            if kwargs.pop('async', False) and 'ctx' in kwargs:
                ctx = kwargs['ctx']
                ctx.events.runAsync(func,
                                    args,
                                    kwargs,
                                    self._title,
                                    self._success,
                                    self._error)
                return True
            else:
                return func(*args, **kwargs)
        return wrapper

from js9 import j

base = j.portal.tools._getBaseClassLoader()


class portal(base):

    def __init__(self):
        base.__init__(self)

from js9 import j
import inspect

class PortalBaseLoader:

    def __init__(self):
        class_fqdn = str(self.__class__).split("'")[1].split(".")
        myClassName = str(self.__class__).split(".")[-1].split("'")[0]
        localdir = j.sal.fs.getDirName(inspect.getsourcefile(self.__class__))
        classes = [j.sal.fs.getBaseName(item)[0:-3] for item in j.sal.fs.listFilesInDir(localdir, filter="Portal*")]
        package_name = ".".join(class_fqdn[0:-2])
        for className in classes:
            # import the class
            exec("from %s.%s import *" % (package_name, className))
            do = "self.%s=%s()" % (className.lower()[6:], className)
            exec(do)

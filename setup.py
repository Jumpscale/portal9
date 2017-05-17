from setuptools import setup
from setuptools.command.install import install as _install
from setuptools.command.develop import develop as _develop
import os
import collections

# zlib1g-dev/zesty
# libjpeg-dev/zesty

def _post_install(libname, libpath):
    from JumpScale9 import j as j
#    from js9 import j
    import os
    j.tools.jsloader.copyPyLibs()

    # ensure plugins section in config
    if 'plugins' not in j.application.config:
        j.application.config['plugins'] = {}

    # add this plugin to the config
    j.application.config['plugins'][libname] = libpath

    moduleList = {}
    gigdir = os.environ.get('GIGDIR', '/root/gig')
    mounted_lib_path = os.path.join(gigdir, 'python_libs')

    for name, path in j.application.config['plugins'].items():
        if j.do.exists(path, followlinks=True):
            moduleList = j.tools.jsloader.findModules(path=path, moduleList=moduleList)
            # link libs to location for hostos
            j.do.copyTree(path,
                          os.path.join(mounted_lib_path, libname),
                          overwriteFiles=True,
                          ignoredir=['*.egg-info',
                                     '*.dist-info',
                                     "*JumpScale*",
                                     "*Tests*",
                                     "*tests*"],

                          ignorefiles=['*.egg-info',
                                       "*.pyc",
                                       "*.so",
                                       ],
                          rsync=True,
                          recursive=True,
                          rsyncdelete=True,
                          createdir=True)

    # DO NOT AUTOPIP the deps are now installed while installing the libs
    j.application.config["system"]["autopip"] = False
    j.application.config["system"]["debug"] = True

    j.tools.jsloader.generate(path=path, moduleList=moduleList)
    j.tools.jsloader.generate(path=path, moduleList=moduleList, codecompleteOnly=True)

    j.do.initEnv()


class install(_install):

    def run(self):
        _install.run(self)
        libname = self.config_vars['dist_name']
        libpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), libname)
        self.execute(_post_install, (libname, libpath), msg="Running post install task")


class develop(_develop):

    def run(self):
        _develop.run(self)
        libname = self.config_vars['dist_name']
        libpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), libname)
        self.execute(_post_install, (libname, libpath), msg="Running post install task")

setup(
    name='JumpScale9Portal',
    version='9.0.0a1',
    description='Automation framework for cloud workloads portal',
    url='https://github.com/Jumpscale/portal9',
    author='GreenItGlobe',
    author_email='info@gig.tech',
    license='Apache',
    packages=['JumpScale9Portal'],
    install_requires=[
        'redis',
        'colorlog',
        'pytoml',
        'ipython',
        'colored_traceback',
        'pystache',
        'libtmux',
        'httplib2',
        'redis',
        'colorlog',
        'pytoml',
        'ipython',
        'colored_traceback',
        'pystache',
        'libtmux',
        'httplib2',
        'netaddr',
        'peewee',
        'uvloop',
        'redis',
        'paramiko',
        'watchdog',
        'pymux',
        'uvloop',
        'pyyaml',
        'ipdb',
        'requests',
        'netaddr',
        'cython',
        'pycapnp',
        'path.py',
        'colored-traceback',
        'pudb',
        'colorlog',
        'msgpack-python',
        'pyblake2',
        'mongoengine',
        'gevent',
        'beaker',
        'gitlab3',
        'mimeparse',
        'flask',
        'flask-bootstrap',
    ],
    cmdclass={
        'install': install,
        'develop': develop,
        'developement': develop
    },
)


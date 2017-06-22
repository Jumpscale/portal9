from setuptools import setup
from setuptools.command.install import install as _install
from setuptools.command.develop import develop as _develop
import os
import collections

# zlib1g-dev/zesty
# libjpeg-dev/zesty

def _post_install(libname, libpath):
    from js9 import j

    # add this plugin to the config
    c = j.core.state.configGet('plugins', defval={})
    c[libname] = libpath
    j.core.state.configSet('plugins', c)

    j.tools.jsloader.generatePlugins()
    j.tools.jsloader.copyPyLibs()


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
        'JumpScale9>=9.0.1',
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

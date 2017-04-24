from distutils.core import setup

setup(
    name='JumpScalePortal9',
    version='9.0.0a1',
    description='Automation framework for cloud workloads portal',
    url='https://github.com/Jumpscale/portal9',
    author='GreenItGlobe',
    author_email='info@gig.tech',
    license='Apache',
    packages=['JumpScalePortal9'],
    install_requires=[
        'redis',
        'colorlog',
        'pytoml',
        'ipython',
        'colored_traceback',
        'pystache',
        'libtmux',
        'httplib2',
        'netaddr'
    ]
)

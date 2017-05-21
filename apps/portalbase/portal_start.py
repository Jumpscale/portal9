# this must be in the beginning so things are patched before ever imported by other libraries
from gevent import monkey
monkey.patch_socket()
monkey.patch_ssl()
monkey.patch_thread()
monkey.patch_time()

from js9 import j
import JumpScale9Portal.portal
import click


@click.group(invoke_without_command=True)
@click.pass_context
@click.option('--instance', default='main', help='instance of portal')
def cli(ctx, instance):
    if ctx.invoked_subcommand is None:
        ctx.obj['INSTANCE'] = instance
        start()


@click.command()
@click.pass_context
@click.option('--instance', default='main', help='instance of portal')
def start(ctx, instance):
    import pdb; pdb.set_trace()
    instance = instance or ctx.obj.get('INSTANCE')
    cfg = j.data.serializer.yaml.load('%s/portals/%s/config.yaml' % (j.dirs.CFGDIR, instance))
    j.application.instanceconfig = cfg

    j.application.start("portal")

    server = j.portal.tools.server.get()
    server.start()

    j.application.stop()

if __name__ == '__main__':
    cli(obj={})

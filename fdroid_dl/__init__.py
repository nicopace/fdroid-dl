"""main entrypoint into fdroid-dl."""
import logging
import click
from .model import Config
from .update import Update


name = 'fdroid-dl'
version = '0.0.1'
author = 't4skforce'
author_mail = '7422037+t4skforce@users.noreply.github.com'

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(name)


@click.group(invoke_without_command=True)
@click.option('-d', '--debug', is_flag=True, default=False, help='enable debug level logging')
@click.option('-c', '--config', default='fdroid-dl.json', type=click.Path(dir_okay=False, writable=True, resolve_path=True), show_default=True, help='location of your fdroid-dl.json configuration file')
@click.option('-r', '--repo', default='./repo', type=click.Path(file_okay=False, writable=True, resolve_path=True), show_default=True, help='location of your fdroid repository to store the apk files')
@click.option('-m', '--metadata', default='./metadata', type=click.Path(file_okay=False, writable=True, resolve_path=True), show_default=True, help='location of your fdroid metadata to store the asset files')
@click.option('--cache', default='./.cache', type=click.Path(file_okay=False, writable=True, resolve_path=True), show_default=True, help='location for fdroid-dl to store cached data')
@click.pass_context
def cli(ctx, debug, config, repo, metadata, cache):
    """
        Is a python based f-droid mirror generation and update utility.
        Point at one or more existing f-droid repositories and the utility will download the metadata (pictures, descriptions,..)
        for you and place it in your local system.

        Simply run "fdroid-dl update && fdroid update" in your folder with repo and you are set.
    """
    if ctx.obj is None:
        ctx.obj = {}
    ctx.obj['debug'] = debug
    ctx.obj['config'] = config
    ctx.obj['repo'] = repo
    ctx.obj['metadata'] = metadata
    ctx.obj['cache_dir'] = cache
    if debug:
        logger.setLevel(logging.DEBUG)
    logger.info('Debug mode is %s' % ('on' if debug else 'off'))
    if ctx.invoked_subcommand is None:
        with click.Context(cli) as ctx:
            click.echo(cli.get_help(ctx))


@cli.group(name='update', invoke_without_command=True, short_help='starts updating process')
@click.option('--index/--no-index', default=True, show_default=True, help='download repository index files')
@click.option('--metadata/--no-metadata', default=True, show_default=True, help='download metadata assset files')
@click.option('--apk/--no-apk', default=True, show_default=True, help='download apk files')
@click.option('--src/--no-src', default=True, show_default=True, help='download src files')
@click.pass_context
def update(ctx, index, metadata, apk, src):
    with Config(ctx.obj['config'], cache_dir=ctx.obj['cache_dir']) as cfg:
        u = Update(cfg)
        if index:
            u.index()
        if metadata:
            u.metadata()
        if apk:
            u.apk()
        if src:
            u.src()


__all__ = ['cli', 'update']

if __name__ == '__main__':
    cli()

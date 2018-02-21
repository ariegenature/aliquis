"""Aliquis command line commands."""

import os
import subprocess

from babel.messages.frontend import CommandLineInterface as BabelCLI
import click

from aliquis import create_app, read_config
import aliquis


app = create_app(read_config())

I18N_PATH = os.path.join(os.path.dirname(aliquis.__file__), 'i18n')


def _extract_18n_messages():
    """Extract messages to translate from application files."""
    BabelCLI().run(['', 'extract', '-F', 'babel.cfg', '-k', '_t', '--no-location', '--sort-output',
                    '--omit-header', '-o', os.path.join(I18N_PATH, 'messages.pot'), 'aliquis'])


def _write_message_files(lang, command='update'):
    """Extract messages to translate from application files."""
    BabelCLI().run(['', command, '-i', os.path.join(I18N_PATH, 'messages.pot'), '-d', I18N_PATH,
                    '-l', lang])


@app.cli.command()
def i18ninit():
    """Extract messages to translate from application files and init messages files for
    configured languages."""
    click.echo('-> Initializing i18n message files...')
    _extract_18n_messages()
    langs = app.config['BABEL_LANGUAGES']
    for lang in langs:
        _write_message_files(lang, command='init')
    click.echo('-> i18n message files initialized.')
    click.echo('You should now edit translations in following files:')
    for lang in langs:
        click.echo(os.path.join(I18N_PATH, lang, 'LC_MESSAGES', 'messages.po'))


@app.cli.command()
def i18nupdate():
    """Extract messages to translate from application files and update messages files for
    configured languages."""
    click.echo('-> Updating i18n message files...')
    _extract_18n_messages()
    langs = app.config['BABEL_LANGUAGES']
    for lang in langs:
        _write_message_files(lang)
    click.echo('-> i18n message files updated.\n')
    click.echo('You should now edit translations in following files:')
    for lang in langs:
        click.echo(os.path.join(I18N_PATH, lang, 'LC_MESSAGES', 'messages.po'))


@app.cli.command()
def i18ncompile():
    """Compile translations for configured languages."""
    click.echo('-> Compiling translations...')
    BabelCLI().run(['', 'compile', '-d', I18N_PATH])
    click.echo('-> Translations compiled.\n')
    click.echo('You should now restart Flask server to take new translations into account.')


@app.cli.command(name='install-js-deps')
def install_js_deps():
    """Run ``npm install`` for the Vue.js client in order to install its JavaScript dependencies."""
    click.echo('-> Installing JavaScript dependencies for the Vue.js client...')
    subprocess.check_call(['npm',
                           '--prefix={0}'.format(os.path.join(os.path.dirname(aliquis.__file__),
                                                              'aliquisjs')),
                           'install'])
    click.echo('-> JavaScript dependencies succesfully installed.')


@app.cli.command(name='build-js-client')
def build_js_client():
    """Execute ``npm run build`` for the Vue.js client to build it so that it can be served."""
    click.echo('-> Building the Vue.js client...')
    subprocess.check_call(['npm',
                           '--prefix={0}'.format(os.path.join(os.path.dirname(aliquis.__file__),
                                                              'aliquisjs')),
                           'run',
                           'build'])
    click.echo('-> Vue.js client succesfully built.')

import os

from babel.messages.frontend import CommandLineInterface as BabelCLI
from flask import redirect, url_for
from flask_login import current_user
import click

from aliquis import create_app


app = create_app(os.environ.get('ALIQUIS_CONF',
                                os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                             'settings.ini')))


def _extract_18n_messages():
    """Extract messages to translate from application files."""
    BabelCLI().run(['', 'extract', '-F', 'babel.cfg', '-k', '_t', '--no-location', '--sort-output',
                    '--omit-header', '-o', 'aliquis/i18n/messages.pot', 'aliquis'])


def _write_message_files(lang, command='update'):
    """Extract messages to translate from application files."""
    BabelCLI().run(['', command, '-i', 'aliquis/i18n/messages.pot', '-d', 'aliquis/i18n/',
                    '-l', lang])


@app.route('/')
def home():
    """Homepage for aliquis."""
    if current_user.is_authenticated:
        return redirect(url_for('sign.user', user_id=current_user.username))
    else:
        return redirect(url_for('sign.login'))


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
        click.echo('aliquis/i18n/{0}/LC_MESSAGES/messages.po'.format(lang))


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
        click.echo('  * aliquis/i18n/{0}/LC_MESSAGES/messages.po'.format(lang))


@app.cli.command()
def i18ncompile():
    """Compile translations for configured languages."""
    click.echo('-> Compiling translations...')
    BabelCLI().run(['', 'compile', '-d', 'aliquis/i18n/'])
    click.echo('-> Translations compiled.\n')
    click.echo('You should now restart Flask server to take new translations into account.')

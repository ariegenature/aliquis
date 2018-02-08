# -*- coding: utf-8 -*-

"""Aliquis package."""


from flask import Flask
from konfig import Config
import os
import sys

from six import PY2
from xdg import XDG_CONFIG_HOME
from werkzeug.contrib.fixers import ProxyFix

from aliquis.extensions import babel, celery, csrf, ldap_manager, login_manager
from aliquis.views import (
    blueprints,
    home as home_view,
    forbidden as forbidden_handler,
    page_not_found as page_not_found_handler,
    internal_error as internal_error_handler,
)


class VueFlask(Flask):
    jinja_options = Flask.jinja_options.copy()
    jinja_options.update({
        'block_start_string': '«%',
        'block_end_string': '%»',
        'comment_start_string': '«#',
        'comment_end_string': '#»',
        'variable_start_string': '««',
        'variable_end_string': '»»',
    })


def create_app(config):
    local_configs = []
    local_configs.append(config.get_map('aliquis'))
    local_configs.append(config.get_map('ldap'))
    local_configs.append(config.get_map('celery'))
    local_configs.append(config.get_map('mail-sendgrid'))
    local_configs.append(config.get_map('babel'))
    app = VueFlask(__name__)
    app.wsgi_app = ProxyFix(app.wsgi_app)
    for config in local_configs:
        app.config.update(config)
    app.config['CELERY_IMPORTS'] = ('aliquis.background_tasks',)
    langs = app.config.get('BABEL_LANGUAGES', 'fr')
    app.config['BABEL_LANGUAGES'] = list(map(lambda s: s.strip(), langs.split(',')))
    app.config['BABEL_TRANSLATION_DIRECTORIES'] = 'i18n'
    app.config['LDAP_READONLY'] = False
    # XXX: Since we use ldap3 ObjectDef (which needs a LDAP class), we make this option computed
    user_ldap_filter = app.config.get('LDAP_USER_OBJECT_FILTER')
    user_ldap_class = app.config['LDAP_USER_CLASS']
    if user_ldap_filter is None:
        app.config['LDAP_USER_OBJECT_FILTER'] = '(objectClass={0})'.format(user_ldap_class)
    elif 'objectClass' not in user_ldap_filter:
        app.config['LDAP_USER_OBJECT_FILTER'] = '(&(objectClass={0}){1})'.format(user_ldap_class,
                                                                                 user_ldap_filter)
    else:
        assert user_ldap_class in user_ldap_filter, ('Looks like there is an inconsistency between '
                                                     'options LDAP_USER_OBJECT_FILTER and '
                                                     'LDAP_USER_CLASS')
    for blueprint in blueprints:
        app.register_blueprint(blueprint)
    babel.init_app(app)
    csrf.init_app(app)
    ldap_manager.init_app(app)
    login_manager.init_app(app)
    celery.init_app(app)
    # Register views, handlers and cli commands
    app.route('/')(home_view)
    app.errorhandler(403)(forbidden_handler)
    app.errorhandler(404)(page_not_found_handler)
    app.errorhandler(500)(internal_error_handler)
    return app


def read_config(cli_fname=None):
    """Return a config (``dict``) object reading configuration from the first existing file among
    all known folders."""
    # If given on command line, use this file
    if cli_fname:
        return Config(cli_fname)
    # If given with env variable, use this file
    env_fname = os.environ.get('ALIQUIS_CONF')
    if env_fname:
        return Config(env_fname)
    # Else use the first file found
    config_folders = []
    if PY2:
        venv = getattr(sys, 'real_prefix', None)
    else:
        venv = sys.base_prefix if sys.base_prefix != sys.prefix else None
    if venv:
        config_folders.append(os.path.join(venv, 'etc', 'aliquis'))
    config_folders.extend([
        os.path.join(XDG_CONFIG_HOME, 'aliquis'),
        os.path.join('/', 'usr', 'local', 'etc', 'aliquis'),
        os.path.join('/', 'etc', 'aliquis'),
    ])
    config_fnames = (os.path.join(config_folder, 'aliquis.ini') for config_folder in config_folders)
    for fname in config_fnames:
        if os.path.exists(fname):
            return Config(fname)

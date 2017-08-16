"""Aliquis package."""

from flask import Flask
from flask_ldap3_login import LDAP3LoginManager
from flask_wtf.csrf import CSRFProtect
from konfig import Config

from aliquis.views import blueprints


csrf = CSRFProtect()
ldap_manager = LDAP3LoginManager()


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


def create_app(config_fname):
    local_configs = []
    local_config = Config(config_fname)
    local_configs.append(local_config.get_map('aliquis'))
    local_configs.append(local_config.get_map('ldap'))
    app = VueFlask(__name__)
    for config in local_configs:
        app.config.update(config)
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
    csrf.init_app(app)
    ldap_manager.init_app(app)
    return app

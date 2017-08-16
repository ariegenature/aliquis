"""Aliquis package."""

from flask import Flask
from flask_wtf.csrf import CSRFProtect
from konfig import Config

from aliquis.views import blueprints


csrf = CSRFProtect()


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
    for blueprint in blueprints:
        app.register_blueprint(blueprint)
    csrf.init_app(app)
    return app

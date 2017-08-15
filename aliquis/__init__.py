"""Aliquis package."""

from flask import Flask
from konfig import Config

from aliquis.views import blueprints


def create_app(config_fname):
    local_configs = []
    local_config = Config(config_fname)
    local_configs.append(local_config.get_map('aliquis'))
    local_configs.append(local_config.get_map('ldap'))
    app = Flask(__name__)
    for config in local_configs:
        app.config.update(config)
    for blueprint in blueprints:
        app.register_blueprint(blueprint)
    return app

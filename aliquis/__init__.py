"""Aliquis package."""

from flask import Flask
from konfig import Config


def create_app(config_fname):
    local_configs = []
    local_config = Config(config_fname)
    local_configs.append(local_config.get_map('aliquis'))
    local_configs.append(local_config.get_map('ldap'))
    app = Flask(__name__)
    for config in local_configs:
        app.config.update(config)
    return app

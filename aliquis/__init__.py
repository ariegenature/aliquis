"""Aliquis package."""

from flask import Flask
from konfig import Config


def create_app(config_fname):
    local_config = Config(config_fname)
    app = Flask(__name__)
    app.config.update(local_config.get_map('aliquis'))
    return app

"""Extensions used by aliquis."""

from flask import current_app, request
from flask_babel import Babel
from flask_celery import Celery
from flask_ldap3_login import LDAP3LoginManager
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

babel = Babel()
celery = Celery()
csrf = CSRFProtect()
ldap_manager = LDAP3LoginManager()
login_manager = LoginManager()


@babel.localeselector
def get_locale():
    try:
        return request.accept_languages.best_match(current_app.config['BABEL_LANGUAGES'])
    except RuntimeError:
        return babel.default_locale.language

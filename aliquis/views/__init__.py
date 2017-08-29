from flask import redirect, url_for
from flask_login import current_user

from aliquis.views.sign import sign
from aliquis.views.mail import mail

blueprints = [mail, sign]


def home():
    """Homepage for aliquis."""
    if current_user.is_authenticated:
        return redirect(url_for('sign.user', user_id=current_user.username))
    else:
        return redirect(url_for('sign.login'))


def forbidden(e):
    return redirect(url_for('sign.error', code=403))


def page_not_found(e):
    return redirect(url_for('sign.error', code=404))


def internal_error(e):
    return redirect(url_for('sign.error', code=500))

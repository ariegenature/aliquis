"""aliquis blueprint for sending mail."""

from collections import namedtuple

from flask import Blueprint, current_app

from aliquis.views.mail import sendgrid


mail = Blueprint('mail', __name__, url_prefix='mail', template_folder='templates')

Contact = namedtuple('Contact', ['name', 'email'])


def send_sendgrid_email(recipient, subject, html_content, txt_content):
    """Send an email with the given information using sendgrid API.

    ``recipient`` must be an instance of the ``Contact`` class.
    """
    config = current_app.config
    api_key = config['SENDGRID_API_KEY']
    sender = Contact(name=config['SENDGRID_SENDER_NAME'], email=config['SENDGRID_SENDER_EMAIL'])
    sendgrid.send_email(sender, recipient, subject, html_content, txt_content, api_key)

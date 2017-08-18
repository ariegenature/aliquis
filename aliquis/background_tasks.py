"""Background tasks for aliquis."""

from flask import render_template

from aliquis.extensions import celery
from aliquis.views.mail import Contact, send_sendgrid_email


@celery.task
def send_sign_up_confirm_email(person_dict):
    send_sendgrid_email(
        recipient=Contact(person_dict['display_name'], person_dict['email']),
        subject="Please confirm your ANA's registration",
        html_content=render_template('sign/sign-up-confirm-email.html', **person_dict),
        txt_content=render_template('sign/sign-up-confirm-email.txt', **person_dict)
    )

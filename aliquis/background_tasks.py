"""Background tasks for aliquis."""

from flask import render_template
from flask_babel import _, get_locale

from aliquis.extensions import celery
from aliquis.views.mail import Contact, send_sendgrid_email


@celery.task
def send_sign_up_confirm_email(person_dict):
    lang = str(get_locale() or 'fr')[:2]
    send_sendgrid_email(
        recipient=Contact(person_dict['display_name'], person_dict['email']),
        subject=_("Please confirm your ANA account creation"),
        html_content=render_template('sign/sign-up-confirm-email.{lang}.html'.format(lang=lang),
                                     **person_dict),
        txt_content=render_template('sign/sign-up-confirm-email.{lang}.txt'.format(lang=lang),
                                    **person_dict)
    )

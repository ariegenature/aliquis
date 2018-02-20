"""Background tasks for aliquis."""

from flask import current_app, render_template
from flask_babel import _, get_locale

from aliquis.extensions import celery
from aliquis.views.mail import Contact, send_sendgrid_email


@celery.task
def send_email_confirm_email(person_dict, token_url, when='sign-up'):
    lang = str(get_locale() or 'fr')[:2]
    templates = dict(
        (ftype,
         'sign/{when}-confirm-email.{lang}.{ftype}'.format(when=when, lang=lang, ftype=ftype))
        for ftype in ('html', 'txt')
    )
    if when == 'sign-up':
        subject = _("Please confirm your ANA account creation")
    elif when == 'email-change':
        subject = _("Please confirm your email address")
    elif when == 'reset-password':
        subject = _("How to reset your ANA password")
    elif when == 'reactivate':
        subject = _("Your activation link")
    send_sendgrid_email(
        recipient=Contact(person_dict['display_name'], person_dict['email']),
        subject=subject,
        html_content=render_template(templates['html'], token_url=token_url, **person_dict),
        txt_content=render_template(templates['txt'], token_url=token_url, **person_dict)
    )


@celery.task
def send_activation_notification(person_dict):
    lang = str(get_locale() or 'fr')[:2]
    templates = dict(
        (ftype,
         'sign/notif-account-activated.{lang}.{ftype}'.format(lang=lang, ftype=ftype))
        for ftype in ('html', 'txt')
    )
    subject = _("%(display_name)s has created or reactivated his/her ANA account",
                display_name=person_dict['display_name'])
    send_sendgrid_email(
        recipient=Contact(current_app.config['NOTIFICATION_TO_NAME'],
                          current_app.config['NOTIFICATION_TO_EMAIL']),
        subject=subject,
        html_content=render_template(templates['html'], **person_dict),
        txt_content=render_template(templates['txt'], **person_dict)
    )

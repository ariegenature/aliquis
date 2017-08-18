"""Functions to send emails with sendgrid."""

import json

import requests


SENDGRID_API_URL = 'https://api.sendgrid.com/v3'
SENDGRID_POST_HEADERS = {
    'Content-Type': 'application/json; charset=utf-8',
}


def send_email(sender, recipient, subject, html_content, txt_content, api_key):
    """Send an email with the given information using sendgrid API.

    ``sender`` and ``recipient`` must be ``Contact`` instances.
    """
    post_headers = SENDGRID_POST_HEADERS.copy()
    post_headers['Authorization'] = 'Bearer {0}'.format(api_key)
    data = {
        'content': [
            {
                'type': 'text/plain',
                'value': txt_content,
            },
            {
                'type': 'text/html',
                'value': html_content,
            }
        ],
        'from': {
            'email': sender.email,
            'name': sender.name,

        },
        'personalizations': [
            {
                'to': [
                    {
                        'email': recipient.email,
                        'name': recipient.name,
                    }
                ],
            }
        ],
        'subject': subject,
    }
    response = requests.post(
        '{api_url}/mail/send'.format(api_url=SENDGRID_API_URL),
        headers=post_headers,
        data=json.dumps(data, ensure_ascii=False).encode('utf-8')
    )
    response.raise_for_status()

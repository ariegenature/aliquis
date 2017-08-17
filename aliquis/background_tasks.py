"""Background tasks for aliquis."""

from aliquis.extensions import celery


@celery.task
def send_sign_up_confirm_email(person):
    print(person)

from collections.abc import Callable

from celery import Celery

from aliquis import create_app, read_config


def _call_cls_in_app_context(base_cls, instance, app, *args, **kwargs):
    """Call the Callable ``base_cls ``class on the given instance within the context of the given
    Flask app.

    ``instance`` may be an instance of a subclass of ``base_cls``.
    """
    print(args, kwargs)
    with app.app_context():
        return base_cls.__call__(instance, *args, **kwargs)


def make_celery(app):
    """Create and return a new ``Celery`` instance."""
    celery = Celery(
        app.import_name,
        broker=app.config['CELERY_BROKER_URL'],
        backend=app.config['CELERY_RESULT_BACKEND']
    )
    celery.conf.update(app.config)
    CeleryTask = celery.Task
    ContextTask = type('ContextTask', (CeleryTask, Callable), {
        'abstract': True,
        '__call__': lambda self, *args, **kwargs: _call_cls_in_app_context(CeleryTask, self, app,
                                                                           *args, **kwargs),
    })
    celery.Task = ContextTask
    return celery


# Do not call this app instance 'app' as it will conflict with Celery
config = read_config()
flask_app = create_app(config)
celery = make_celery(flask_app)

import os

from aliquis import create_app


app = create_app(os.environ.get('ALIQUIS_CONF',
                                os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                             'settings.ini')))


@app.route('/')
def home():
    """Homepage for aliquis."""
    return 'Work in progress'

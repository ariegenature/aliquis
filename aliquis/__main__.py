#!/usr/bin/env python

import argparse
import os
import signal
import sys

from chaussette.server import make_server as make_chaussette_server

from aliquis.server import app


def command_line_options():
    parser = argparse.ArgumentParser(description=('Web application allowing user to sign-up and'
                                                  'sign-in'))
    parser.add_argument('--config', '-c', help='Path to the aliquis configuration file',
                        default=os.environ.get('ALIQUIS_CONF'))
    parser.add_argument('--fd', type=int, default=None,
                        help='File descriptor of the socket to bind to with chaussette')
    return parser.parse_args()


def start_aliquis():
    """Start the aliquis flask application.

    Either use the classical werkzeug runner or the chaussette runner depending whether or not a
    socket file descriptor is passed on command line.
    """
    args = command_line_options()
    signal.signal(signal.SIGINT, stop_aliquis)
    signal.signal(signal.SIGTERM, stop_aliquis)
    if args.fd is not None:
        srv = make_chaussette_server(app, host='fd://{0}'.format(args.fd))
    else:
        host, port = app.config.get('SERVER_NAME', 'localhost:5000').split(':')
        port = int(port) if port.isdigit() else 5000
        srv = make_chaussette_server(app, host=host, port=port)
    srv.serve_forever()


def stop_aliquis(signal, frame):
    """Hook called when quitting application to cleanup before exiting."""
    sys.exit(0)


main = start_aliquis


if __name__ == '__main__':
    main()

"""Aliquis blueprint allowing a user to sign up."""

import mimetypes

from flask import Blueprint, make_response, render_template

from aliquis.person import USERNAME_REGEXP


sign = Blueprint('sign', __name__,
                 static_folder='templates/static',
                 template_folder='templates')


def sign_up():
    return render_template('sign/index.html')


@sign.route('/sign/static/<path:fpath>', methods=['GET'])
def sign_static(fpath):
    print('static/{0}'.format(fpath))
    resp = make_response(render_template('static/{0}'.format(fpath)))
    resp.headers['Content-Type'], resp.headers['Content-Encoding'] = mimetypes.guess_type(fpath)
    return resp

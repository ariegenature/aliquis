"""Aliquis blueprint allowing a user to sign up."""

import mimetypes

from flask import Blueprint, make_response, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, Regexp

from aliquis.person import USERNAME_REGEXP


sign = Blueprint('sign', __name__,
                 static_folder='templates/static',
                 template_folder='templates')


class SignUpForm(FlaskForm):
    """Sign up form for ANA."""

    first_name = StringField('First name', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    display_name = StringField('Display name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired(), Regexp(USERNAME_REGEXP)])
    password = PasswordField('Password', validators=[DataRequired()])

    def validate(self):
        are_fields_ok = super(SignUpForm, self).validate()
        if not are_fields_ok:
            return False
        return True


@sign.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    form = SignUpForm()
    if form.validate_on_submit():
        return 'OK'
    return render_template('sign/index.html')


@sign.route('/sign/static/<path:fpath>', methods=['GET'])
def sign_static(fpath):
    print('static/{0}'.format(fpath))
    resp = make_response(render_template('static/{0}'.format(fpath)))
    resp.headers['Content-Type'], resp.headers['Content-Encoding'] = mimetypes.guess_type(fpath)
    return resp

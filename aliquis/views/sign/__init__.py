"""Aliquis blueprint allowing a user to sign up."""

from contextlib import contextmanager
import mimetypes

from flask import Blueprint, current_app, jsonify, make_response, render_template
from flask_wtf import FlaskForm
from ldap3 import ObjectDef, Reader, Writer
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, Regexp

from aliquis.person import person as new_person, USERNAME_REGEXP
from aliquis.background_tasks import send_sign_up_confirm_email


LDAP_ATTR_MAPPING = {
    'first_name': 'givenName',
    'surname': 'sn',
    'email': 'mail',
    'display_name': 'displayName',
    'username': 'uid',
    'password': 'userPassword',
}


sign = Blueprint('sign', __name__,
                 static_folder='templates/static',
                 template_folder='templates')


def _username_exists(username):
    """Check if username already exists in LDAP directory related to the Flask app."""
    return bool(
        current_app.ldap3_login_manager.get_user_info_for_username(username)
    )


def _email_exists(email):
    """Check if email address already exists in LDAP directory related to the Flask app."""
    ldap_manager = current_app.ldap3_login_manager
    ldap_filter = '(&(mail={0}){1})'.format(email,
                                            current_app.config['LDAP_USER_OBJECT_FILTER'])
    return bool(ldap_manager.get_object(
        dn=ldap_manager.full_user_search_dn,
        filter=ldap_filter,
        attributes=current_app.config.get('LDAP_GET_USER_ATTRIBUTES')
    ))


@contextmanager
def _add_cursor(ldap_conn, search_class, base_dn, ldap_filter=None):
    """Return a new ``ldap3.Writer`` cursor for adding a new entry in the LDAP directory.

    Added entry must match given parameters.

    This can be used as a context manager.
    """
    object_def = ObjectDef(search_class, ldap_conn)
    cur_params = {
        'connection': ldap_conn,
        'object_def': object_def,
        'base': base_dn,
    }
    if ldap_filter is not None:
        cur_params['query'] = ldap_filter
    wcur = Writer.from_cursor(Reader(**cur_params))
    yield wcur
    wcur.commit()


def _save_person_to_ldap(person, ldap_conn):
    """Add the given person in the LDAP directory."""
    config = current_app.config
    ldap_manager = current_app.ldap3_login_manager
    user_search_dn = ldap_manager.full_user_search_dn
    rdn = '{attr}={value}'.format(attr=config['LDAP_USER_RDN_ATTRIBUTE'], value=person.username)
    with _add_cursor(ldap_conn, config['LDAP_USER_CLASS'], user_search_dn,
                     config.get('LDAP_USER_OBJECT_FILTER')) as wcur:
        ldap_person = wcur.new('{rdn},{base_dn}'.format(rdn=rdn, base_dn=user_search_dn))
        for attr in LDAP_ATTR_MAPPING:
            value = getattr(person, attr, None)
            if value is not None:
                if attr == 'password':
                    value = '{{CRYPT}}{0}'.format(value)
                setattr(ldap_person, LDAP_ATTR_MAPPING[attr], value)
        ldap_person.cn = u'{0} {1}'.format(person.first_name, person.surname)


class SignUpForm(FlaskForm):
    """Sign up form for ANA."""

    first_name = StringField('First name', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    display_name = StringField('Display name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired(), Regexp(USERNAME_REGEXP)])
    password = PasswordField('Password', validators=[DataRequired()])

    def validate(self):
        result = super(SignUpForm, self).validate()
        if _username_exists(self.username.data):
            self.username.errors.append('Username already exists')
            result = False
        if _email_exists(self.email.data):
            self.email.errors.append('Email address already exists')
            result = False
        return result


@sign.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    form = SignUpForm()
    if form.validate_on_submit():
        p = new_person(**dict((k, v) for k, v in form.data.items() if k in LDAP_ATTR_MAPPING))
        _save_person_to_ldap(p, current_app.ldap3_login_manager.connection)
        send_sign_up_confirm_email.delay(p.as_json())
        return jsonify({'id': p.username}), 201
    errors = dict((field.name, ' ; '.join(field.errors)) for field in form if field.errors)
    if errors:
        return jsonify(errors), 409
    return render_template('sign/index.html')


@sign.route('/sign/static/<path:fpath>', methods=['GET'])
def sign_static(fpath):
    resp = make_response(render_template('static/{0}'.format(fpath)))
    resp.headers['Content-Type'], resp.headers['Content-Encoding'] = mimetypes.guess_type(fpath)
    return resp

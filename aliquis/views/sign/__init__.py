"""Aliquis blueprint allowing a user to sign up."""

from contextlib import contextmanager
import mimetypes

from flask import Blueprint, current_app, jsonify, make_response, render_template, url_for
from flask_babel import _, lazy_gettext as _t, ngettext, get_locale
from flask_wtf import FlaskForm
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer
from ldap3 import ObjectDef, Reader, Writer
from six import text_type
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

LDAP_ATTR_REV_MAPPING = dict((v, k) for k, v in LDAP_ATTR_MAPPING.items())


sign = Blueprint('sign', __name__,
                 static_folder='templates/static',
                 template_folder='templates')


def _person_from_ldap_entry(ldap_dict):
    """Return a ``Person`` instance from the given LDAP entry."""
    person_dict = dict()
    for ldap_attr, attr in LDAP_ATTR_REV_MAPPING.items():
        try:
            ldap_value = ldap_dict[ldap_attr]
        except KeyError:
            continue
        ldap_value = ldap_value[0] if isinstance(ldap_value, list) else ldap_value
        if attr == 'paswword':
            person_dict[attr] = ldap_value.replace('{CRYPT}', '')
        else:
            person_dict[attr] = ldap_value
    return new_person(**person_dict)


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

    first_name = StringField(_t('First name'), validators=[DataRequired()])
    surname = StringField(_t('Surname'), validators=[DataRequired()])
    display_name = StringField(_t('Display name'),
                               description=_t('How your name will be displayed in applications'),
                               validators=[DataRequired()])
    email = StringField(_t('Email'), validators=[DataRequired(), Email()])
    username = StringField(_t('Username'),
                           description=_t('Only lowercase unaccented letters and digits'),
                           validators=[DataRequired(), Regexp(USERNAME_REGEXP)])
    password = PasswordField(_t('Password'),
                             description=_t('At least 6 characters'),
                             validators=[DataRequired()])

    def validate(self):
        result = super(SignUpForm, self).validate()
        if _username_exists(self.username.data):
            self.username.errors.append(_t('Username already exists'))
            result = False
        if _email_exists(self.email.data):
            self.email.errors.append(_t('Email address already exists'))
            result = False
        return result


@sign.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    form = SignUpForm(meta={'locales': [get_locale()]})
    if form.validate_on_submit():
        p = new_person(**dict((k, v) for k, v in form.data.items() if k in LDAP_ATTR_MAPPING))
        _save_person_to_ldap(p, current_app.ldap3_login_manager.connection)
        token_serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        send_sign_up_confirm_email.delay(
            person_dict=p.as_json(),
            token_url=url_for('sign.confirm_new_account', token=token_serializer.dumps(p.username),
                              _external=True)
        )
        return jsonify({'id': p.username}), 201
    errors = [{
        'field': field.name,
        'message': ', '.join(map(lambda err: text_type(err), field.errors))
    } for field in form if field.errors]
    if errors:
        msg = u'{0} {1}.'.format(
            ngettext('After checking, we found the following problem:',
                     'After checking, we found the following problems:',
                     len(errors)),
            u'; '.join('({i}) {m}'.format(i=i, m=err['message']) for i, err in enumerate(errors, 1))
        )
        return jsonify({'message': msg, 'errors': errors}), 409
    return render_template('sign/index.html')


@sign.route('/confirm/<token>', methods=['GET'])
def confirm_new_account(token):
    """View for confirming account creation token."""
    config = current_app.config
    token_serializer = URLSafeTimedSerializer(config['SECRET_KEY'])
    msg = _('Thank you for confirming. Your account is now activated and you may now log in.')
    msg_cls = 'is-success'
    try:
        username = token_serializer.loads(token, max_age=3600)
    except SignatureExpired:
        msg = _('The confirmation link has expired. Please create your account again.')
        msg_cls = 'is-danger'
    except BadSignature:
        msg = _('The confirmation link is invalid.')
        msg_cls = 'is-danger'
    else:
        p = _person_from_ldap_entry(
            current_app.ldap3_login_manager.get_user_info_for_username(username)
        )
        if p.is_active:
            msg = _('This account is already activated. You can log in.')
            msg_cls = 'is-info'
    return render_template('sign/index.html', msg=msg, msg_cls=msg_cls)


@sign.route('/sign/static/<path:fpath>', methods=['GET'])
def sign_static(fpath):
    resp = make_response(render_template('static/{0}'.format(fpath), form=SignUpForm()))
    resp.headers['Content-Type'], resp.headers['Content-Encoding'] = mimetypes.guess_type(fpath)
    return resp

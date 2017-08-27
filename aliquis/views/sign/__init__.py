"""Aliquis blueprint allowing a user to sign up."""

from contextlib import contextmanager
from functools import wraps
import mimetypes

from flask import (Blueprint, abort, current_app, jsonify, make_response, render_template, redirect,
                   request, url_for)
from flask_babel import _, lazy_gettext as _t, ngettext, get_locale
from flask_ldap3_login import AuthenticationResponseStatus
from flask_ldap3_login.forms import LDAPLoginForm
from flask_login import current_user, login_required, login_user, logout_user
from flask_login.config import EXEMPT_METHODS as LOGIN_EXEMPT_METHODS
from flask_wtf import FlaskForm
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer
from ldap3 import ObjectDef, Reader, Writer
from ldap3.core.exceptions import LDAPCursorError, LDAPNoSuchObjectResult
from six import text_type
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, Length, Regexp

from aliquis.extensions import ldap_manager, login_manager
from aliquis.person import person as new_person, USERNAME_REGEXP
from aliquis.background_tasks import send_email_confirm_email


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


@contextmanager
def _update_cursor(read_cursor):
    """Return a new ``ldap3.Writer`` cursor for updating entries in the LDAP directory.

    The given read cursor must contains entries to be updated.

    This can be used as a context manager.
    """
    wcur = Writer.from_cursor(read_cursor)
    yield wcur
    wcur.commit()


@contextmanager
def _read_cursor(ldap_conn, search_class, base_dn, ldap_filter=None):
    """Return a new ``ldap3.Reader`` cursor for browsing an LDAP tree described by the given
    parameters.

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
    yield Reader(**cur_params)


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


def _update_person_in_ldap(person, ldap_conn, update_password=False):
    """Update the given person in the LDAP directory."""
    config = current_app.config
    ldap_manager = current_app.ldap3_login_manager
    user_search_dn = ldap_manager.full_user_search_dn
    # Find the person by its ursername or email
    with _read_cursor(ldap_conn, config['LDAP_USER_CLASS'], user_search_dn,
                      'uid:={username}'.format(username=person.username)) as cur:
        cur.search()
        assert len(cur) <= 1, ('Problem in your database: more than one user with username '
                               "'{1}'".format(person.username))
        if len(cur) == 0:
            raise LDAPNoSuchObjectResult("No person with username '{0}' in "
                                         'database'.format(person.username))
        with _update_cursor(cur) as wcur:
            entry = wcur[0]
            for attr, ldap_attr in LDAP_ATTR_MAPPING.items():
                value = getattr(person, attr, None)
                if value is None or (attr == 'password' and not update_password):
                    continue
                if attr == 'password':
                    value = '{{CRYPT}}{0}'.format(value)
                try:
                    ldap_value = getattr(entry, ldap_attr)
                except LDAPCursorError:
                    setattr(entry, ldap_attr, value)
                else:
                    if ldap_value.value != value:
                        setattr(entry, ldap_attr, value)


def _activate_ldap_person(person, ldap_conn):
    """Activate the given LDAP person."""
    config = current_app.config
    ldap_manager = current_app.ldap3_login_manager
    user_dn = ldap_manager.get_user_info_for_username(person.username)['dn']
    # Find the avtive role
    with _read_cursor(ldap_conn, config['LDAP_PERMISSION_CLASS'],
                      ldap_manager.compiled_sub_dn(config['LDAP_PERMISSION_DN']),
                      'cn:={name}'.format(name=config['LDAP_ACTIVE_PERM_NAME'])) as cur:
        cur.search()
        assert len(cur) <= 1, 'Problem in your database: more than one active role'
        if len(cur) == 0:
            raise LDAPNoSuchObjectResult('No active role')
        with _update_cursor(cur) as wcur:
            active_dns = wcur[0][config['LDAP_PERMISSION_ATTRIBUTE']]
            if user_dn not in active_dns:
                active_dns += user_dn


def _deactivate_ldap_person(person, ldap_conn):
    """Deactivate the given LDAP person."""
    config = current_app.config
    ldap_manager = current_app.ldap3_login_manager
    user_dn = ldap_manager.get_user_info_for_username(person.username)['dn']
    # Find the avtive role
    with _read_cursor(ldap_conn, config['LDAP_PERMISSION_CLASS'],
                      ldap_manager.compiled_sub_dn(config['LDAP_PERMISSION_DN']),
                      'cn:={name}'.format(name=config['LDAP_ACTIVE_PERM_NAME'])) as cur:
        cur.search()
        assert len(cur) <= 1, 'Problem in your database: more than one active role'
        if len(cur) == 0:
            raise LDAPNoSuchObjectResult('No active role')
        with _update_cursor(cur) as wcur:
            active_dns = wcur[0][config['LDAP_PERMISSION_ATTRIBUTE']]
            if user_dn in active_dns:
                active_dns -= user_dn


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


class LoginForm(LDAPLoginForm):
    """Login form for ANA."""

    username = StringField(_t('Username'), validators=[DataRequired()])
    password = PasswordField(_t('Password'), validators=[DataRequired()])


class UserForm(FlaskForm):
    """Update user data form."""

    first_name = StringField(_t('First name'), validators=[DataRequired()])
    surname = StringField(_t('Surname'), validators=[DataRequired()])
    display_name = StringField(_t('Display name'), validators=[DataRequired()])


class ChangeEmailForm(FlaskForm):
    """Update user email form."""

    current_password = PasswordField(_t('Password'), validators=[DataRequired()])
    new_email = StringField(_t('Email'), validators=[DataRequired(), Email()])

    def validate(self):
        valid = super(ChangeEmailForm, self).validate()
        if not valid:
            return False
        auth_result = current_app.ldap3_login_manager.authenticate(current_user.username,
                                                                   self.current_password.data)
        if auth_result.status != AuthenticationResponseStatus.success:
            self.current_password.errors.append(_t('Wrong password'))
            return False
        if _email_exists(self.new_email.data):
            self.new_email.errors.append(_t('Email address already exists'))
            return False
        return True


class ChangePasswordForm(FlaskForm):
    """Update user password form."""

    current_password = PasswordField(_t('Current password'), validators=[DataRequired()])
    new_password = PasswordField(_t('New password'), validators=[DataRequired(), Length(min=6)])

    def validate(self):
        valid = super(ChangePasswordForm, self).validate()
        if not valid:
            return False
        auth_result = current_app.ldap3_login_manager.authenticate(current_user.username,
                                                                   self.current_password.data)
        if auth_result.status != AuthenticationResponseStatus.success:
            self.current_password.errors.append(_t('Wrong password'))
            return False
        return True


def same_user_id_required(func):
    """Decorator toward view functions. The decorated view function must take a ``user_id`` as its
    first parameter. Then this decorator will ensure that the currently logged in user has the same
    user id (as returned by the ``get_id`` method) than the user id passed when calling the view.
    """
    @wraps(func)
    def decorated_view(user_id, *args, **kwargs):
        if (request.method in LOGIN_EXEMPT_METHODS or current_app.login_manager._login_disabled):
            return func(user_id, *args, **kwargs)
        if current_user.is_authenticated and current_user.get_id() == user_id:
            return func(user_id, *args, **kwargs)
        if current_user.is_anonymous:
            return redirect(url_for('sign.login'))
        return abort(403)
    return decorated_view


@ldap_manager.save_user
def save_user(dn, username, ldap_dict, memberships):
    return _person_from_ldap_entry(ldap_dict)


@login_manager.user_loader
def load_user(username):
    try:
        return _person_from_ldap_entry(
            current_app.ldap3_login_manager.get_user_info_for_username(username)
        )
    except Exception:
        return None


@sign.route('/user/<user_id>', methods=['GET', 'POST'])
@same_user_id_required
def user(user_id):
    """View showing and updating a person's data."""
    form = UserForm(meta={'locales': [get_locale()]})
    if form.validate_on_submit():
        person_dict = dict((k, v) for k, v in form.data.items() if k in LDAP_ATTR_MAPPING)
        person_dict['username'] = current_user.username
        p = new_person(**person_dict)
        _update_person_in_ldap(p, current_app.ldap3_login_manager.connection)
        return jsonify({'id': p.username}), 200
    return render_template('sign/index.html')


@sign.route('/email/<user_id>', methods=['GET', 'POST'])
@same_user_id_required
def change_email(user_id):
    """View allowing to change the person's email."""
    ldap_manager = current_app.ldap3_login_manager
    form = ChangeEmailForm(meta={'locales': [get_locale()]})
    if form.validate_on_submit():
        current_user.email = form.new_email.data
        _update_person_in_ldap(current_user, ldap_manager.connection)
        _deactivate_ldap_person(current_user, ldap_manager.connection)
        token_serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        send_email_confirm_email.delay(
            person_dict=current_user.as_json(),
            token_url=url_for('sign.confirm',
                              token=token_serializer.dumps(user_id),
                              _external=True),
            when='email-change'
        )
        return jsonify({'id': user_id}), 200
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
        return jsonify({'message': msg, 'errors': errors}), 401
    return render_template('sign/index.html')


@sign.route('/password/<user_id>', methods=['GET', 'POST'])
@same_user_id_required
def change_password(user_id):
    """View allowing to change the person's password."""
    form = ChangePasswordForm(meta={'locales': [get_locale()]})
    if form.validate_on_submit():
        current_user.password = form.new_password.data
        _update_person_in_ldap(current_user, current_app.ldap3_login_manager.connection,
                               update_password=True)
        return jsonify({'id': user_id}), 200
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
        return jsonify({'message': msg, 'errors': errors}), 401
    return render_template('sign/index.html')


@sign.route('/api/user/<user_id>', methods=['GET'])
@same_user_id_required
def api_user(user_id):
    """View showing and updating a person's data."""
    return jsonify(dict((k, v) for k, v in _person_from_ldap_entry(
        current_app.ldap3_login_manager.get_user_info_for_username(user_id)
    ).as_json().items()))


@sign.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    form = SignUpForm(meta={'locales': [get_locale()]})
    if form.validate_on_submit():
        p = new_person(**dict((k, v) for k, v in form.data.items() if k in LDAP_ATTR_MAPPING))
        _save_person_to_ldap(p, current_app.ldap3_login_manager.connection)
        token_serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        send_email_confirm_email.delay(
            person_dict=p.as_json(),
            token_url=url_for('sign.confirm', token=token_serializer.dumps(p.username),
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


@sign.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(meta={'locales': [get_locale()]})
    if form.validate_on_submit():
        p = _person_from_ldap_entry(
            current_app.ldap3_login_manager.get_user_info_for_username(form.username.data)
        )
        login_user(p, force=True)
        return jsonify({'id': form.username}), 200
    if form.username.errors:
        msg = u'{0}. '.format(_('Login failed'))
        if 'Invalid Username/Password.' in form.username.errors:
            msg += _('Please check your username and password.')
        else:
            msg += u', '.join(map(lambda err: text_type(err), form.username.errors))
        return jsonify({'message': msg}), 401
    return render_template('sign/index.html')


@sign.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('.login'))


@sign.route('/confirm/<token>', methods=['GET'])
def confirm(token):
    """View for confirming email address."""
    return render_template('sign/index.html')


@sign.route('/api/confirm/<token>')
def api_confirm(token):
    """API view for confirming email address."""
    config = current_app.config
    ldap_manager = current_app.ldap3_login_manager
    token_serializer = URLSafeTimedSerializer(config['SECRET_KEY'])
    try:
        username = token_serializer.loads(token, max_age=3600)
    except SignatureExpired:
        msg = _('The confirmation link has expired. Please generate a new confirmation link.')
        msg_cls = 'is-danger'
        http_code = 409
    except BadSignature:
        msg = _('The confirmation link is invalid.')
        msg_cls = 'is-danger'
        http_code = 403
    else:
        p = _person_from_ldap_entry(
            ldap_manager.get_user_info_for_username(username)
        )
        if p.is_active:
            msg = _('This account is already activated. You can log in.')
            msg_cls = 'is-info'
            http_code = 200
        else:
            _activate_ldap_person(p, ldap_manager.connection)
            msg = _('Thank you for confirming. Your account is now activated and you may now log '
                    'in.')
            msg_cls = 'is-success'
            http_code = 201
    return jsonify({'msg': msg, 'cls': msg_cls}), http_code


@sign.route('/sign/static/<path:fpath>', methods=['GET'])
def sign_static(fpath):
    resp = make_response(render_template('static/{0}'.format(fpath), form=SignUpForm()))
    resp.headers['Content-Type'], resp.headers['Content-Encoding'] = mimetypes.guess_type(fpath)
    return resp


@sign.route('/error/<int:code>')
def error(code):
    return render_template('sign/index.html'), code


@sign.errorhandler(403)
def forbidden(e):
    return redirect(url_for('sign.error', code=403))


@sign.errorhandler(404)
def page_not_found(e):
    return redirect(url_for('sign.error', code=404))


@sign.errorhandler(500)
def internal_error(e):
    return redirect(url_for('sign.error', code=500))

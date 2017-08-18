"""Classes and functions to deal with people account information."""

from crypt import crypt
from hmac import compare_digest as compare_hash
import re

from six import PY3, text_type, binary_type

if PY3:
    from crypt import mksalt, METHOD_SHA512
else:
    from base64 import b64encode
    from os import urandom


# Regexp to check if a string is already hashed using system's crypt()
CRYPT_REGEXP = re.compile(r'(\$\d\$[^$]+\$)')  # XXX: Doesn't work with bcrypt

# Regexp to check if a string is a valid username
USERNAME_REGEXP = re.compile(r'^[a-zA-Z][a-zA-Z0-9_.]+$')


def person(first_name, surname, username, display_name=None, email=None, password=None):
    """Return a new instance of the Person class, built with given values."""
    first_name = _text_value(first_name)
    if not first_name:
        raise ValueError('First name cannot be empty')
    surname = _text_value(surname)
    if not surname:
        raise ValueError('Surname cannot be empty')
    username = _text_value(username)
    if USERNAME_REGEXP.match(username) is None:
        raise ValueError(u'Invalid username: {0}'.format(username))
    email = _text_value(email, allow_empty=False)
    if (email is not None and
            re.match(r'([a-zA-Z0-9.+-]+@[a-zA-Z\d-]+(\.[a-zA-Z\d-]+)+$)', email) is None):
        raise ValueError(u'Invalid email address: {0}'.format(email))
    display_name = _text_value(display_name, allow_empty=False)
    p = Person(first_name, surname, username, display_name, email)
    if password is not None:
        p.password = password
    return p


class Person(object):
    """A human being with an email address.

    Note that two Person instances whose email address is defined compare as equal if their email
    addresses are equals: the goal is to avoid creating two persons with the same email address.
    """

    def __init__(self, first_name, surname, username, display_name=None, email=None):
        self.first_name = first_name
        self.surname = surname
        self.email = email
        self._display_name = display_name
        self._username = username
        self._password = None

    @property
    def display_name(self):
        """The name to display for this person."""
        return (self._display_name or u'{0} {1}'.format(self.first_name, self.surname))

    @display_name.setter
    def display_name(self, display_name):
        self._display_name = display_name

    @property
    def username(self):
        """The person's username."""
        return self._username

    @property
    def password(self):
        """The person's password (hashed)."""
        return self._password.decode('utf-8')

    @password.setter
    def password(self, value):
        if isinstance(value, binary_type):
            value = value.decode('utf-8')
        value = _text_value(value, allow_empty=False)
        if value is None:
            raise ValueError('Password cannot be empty')
        if CRYPT_REGEXP.match(value):  # value is already hashed
            self._password = binary_type(value.encode('utf-8'))
        else:  # value is clear text
            self._password = binary_type(crypt(value, _sha512_salt()).encode('utf-8'))

    def check_password(self, value):
        """Check if the given password matches the person's password."""
        if isinstance(value, binary_type):
            value = value.decode('utf-8')
        value = _text_value(value)
        if CRYPT_REGEXP.match(value):  # value is already hashed
            return self._password.decode('utf-8') == value
        else:  # value is clear text
            salt = CRYPT_REGEXP.match(self._password.decode('utf-8')).group(1)
            return compare_hash(self._password, binary_type(crypt(value, salt).encode('utf-8')))

    def as_json(self):
        return dict((k, getattr(self, k, None)) for k in ('first_name', 'surname', 'display_name',
                                                          'email', 'username', 'password'))

    def __str__(self):
        return self.display_name

    def __eq__(self, other):
        return (self.first_name == other.first_name and self.surname == other.surname and
                self.username == other.username and self.email == other.email)


def _sha512_salt():
    """Return a random SHA-512 salt suitable for the ``crypt.crypt`` function."""
    if PY3:
        return mksalt(METHOD_SHA512)
    else:
        return u'$6${0}$'.format(b64encode(urandom(8)).decode('utf-8'))


def _text_value(x, default=u'', allow_empty=True):
    """Return ``x`` unicode value or the default value if ``x`` is ``None``.

    if ``allow_empty`` is False, and ``x`` is an empty string, return ``None`` instead of an empty
    string."""
    x = text_type(x) if x is not None else default
    if not allow_empty:
        x = x or None
    return x

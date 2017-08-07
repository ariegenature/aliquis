"""LDAP backend for people."""

from configparser import ParsingError
from contextlib import contextmanager
import ssl

from ldap3 import ALL, Connection, MOCK_SYNC, OFFLINE_SLAPD_2_4, ObjectDef, Reader, Server, Writer
from ldap3.core.exceptions import (LDAPCursorError, LDAPEntryAlreadyExistsResult,
                                   LDAPNoSuchObjectResult)

from aliquis.person import person as new_person


_OPT_MAPPING = {
    'LDAP_REQUIRE_CERT': {
        True: ssl.CERT_REQUIRED,
        False: ssl.CERT_NONE,
    },
}

LDAP_ATTR_MAPPING = {
    'first_name': 'givenName',
    'surname': 'sn',
    'email': 'mail',
    'display_name': 'displayName',
    'username': 'uid',
    'password': 'userPassword',
}

LDAP_ATTR_REV_MAPPING = dict((v, k) for k, v in LDAP_ATTR_MAPPING.items())


def _person_from_ldap_entry(entry):
    """Return a ``Person`` instance from the given LDAP entry."""
    person_dict = dict()
    for ldap_attr, attr in LDAP_ATTR_REV_MAPPING.items():
        try:
            ldap_value = getattr(entry, ldap_attr)
        except LDAPCursorError:
            continue
        person_dict[attr] = ldap_value.value
    return new_person(**person_dict)


class LDAPBackend(object):
    """Store person information in an LDAP directory."""

    def __init__(self, app, fake=False):
        self.fake = fake
        self._app = app
        for opt, mapping in _OPT_MAPPING.items():
            if opt in app.config:
                try:
                    app.config[opt] = mapping[app.config[opt]]
                except KeyError:
                    raise ParsingError("Invalid value for option '{opt}' in configuration. "
                                       'Expected: {values}'.format(opt=opt,
                                                                   values=', '.join(mapping)))

        app.config.setdefault('LDAP_SERVER', 'localhost')
        app.config.setdefault('LDAP_PORT', 389)
        app.config.setdefault('LDAP_REQUIRE_CERT', ssl.CERT_REQUIRED)
        self._people_basedn = app.config['LDAP_PEOPLE_BASEDN']
        self._person_class = app.config['LDAP_PERSON_CLASS']
        srv_params = {
            'host': self._app.config['LDAP_SERVER'],
            'port': self._app.config['LDAP_PORT'],
            'use_ssl': self._app.config.get('LDAP_USE_SSL', True),
        }
        if fake is False:
            srv_params['get_info'] = ALL
        else:
            srv_params['get_info'] = OFFLINE_SLAPD_2_4
        self.srv = Server(**srv_params)

    @property
    def app(self):
        """Return the Flask application instance tied to the backend."""
        return self._app

    def connection(self):
        """Connect to LDAP server specified in application config and return the corresponding
        ``ldap3.Connection`` instance.

        This can be used as a context manager.

        If ``fake`` parameter is ``True``, connection will use the ``ldap3.MOCK_SYNC`` strategy.
        """
        conn_params = {
            'server': self.srv,
            'auto_bind': True,
            'user': self._app.config['LDAP_BINDDN'],
            'password': self._app.config['LDAP_SECRET'],
            'check_names': True,
        }
        if self.fake is True:
            conn_params['client_strategy'] = MOCK_SYNC
        return Connection(**conn_params)

    @contextmanager
    def read_cursor(self, ldap_conn, search_class, base_dn, ldap_filter=None):
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

    @contextmanager
    def add_cursor(self, ldap_conn, search_class, base_dn, ldap_filter=None):
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
    def update_cursor(self, read_cursor):
        """Return a new ``ldap3.Writer`` cursor for updating entries in the LDAP directory.

        The given read cursor must contains entries to be updated.

        This can be used as a context manager.
        """
        wcur = Writer.from_cursor(read_cursor)
        yield wcur
        wcur.commit()

    def entries(self, ldap_conn, search_class, base_dn, ldap_filter=None):
        """Yield each LDAP entry (``ldap3.Entry`` instance) matching the given search parameters."""
        with self.read_cursor(ldap_conn, search_class, base_dn, ldap_filter) as cur:
            cur.search()
            for entry in cur:
                yield entry

    def attribute_exists(self, ldap_conn, search_class, base_dn, attr, value):
        """Return ``True`` if there is an entry with the given class, the given attribute and the
        given value in the LDAP directory."""
        with self.read_cursor(ldap_conn, search_class, base_dn,
                              '{attr}:={value}'.format(attr=attr, value=value)) as cur:
            cur.search()
            l = len(cur)
        return bool(l)

    def username_exists(self, username, ldap_conn):
        """Return ``True`` if there is a person with the given username in the LDAP directory."""
        return self.attribute_exists(ldap_conn, self._person_class, self._people_basedn,
                                     'uid', username)

    def email_exists(self, email, ldap_conn):
        """Return ``True`` if there is a person with the given email address in the LDAP
        directory."""
        return self.attribute_exists(ldap_conn, self._person_class, self._people_basedn,
                                     'mail', email)

    def person_by_username(self, username, ldap_conn):
        """Return a ``Person`` instance with the given username.

        Raise an error if no person is found with this username."""
        with self.read_cursor(ldap_conn, self._person_class, self._people_basedn,
                              'uid:={0}'.format(username)) as cur:
            cur.search()
            assert len(cur) <= 1, ('Problem in your database: more than one user with username '
                                   "'{0}'".format(username))
            if len(cur) == 0:
                raise LDAPNoSuchObjectResult("No person with username '{0}' in "
                                             'database'.format(username))
            entry = cur[0]
        return _person_from_ldap_entry(entry)

    def person_by_email(self, email, ldap_conn):
        """Return a ``Person`` instance with the given email address.

        Raise an error if no person is found with this email address."""
        with self.read_cursor(ldap_conn, self._person_class, self._people_basedn,
                              'mail:={0}'.format(email)) as cur:
            cur.search()
            assert len(cur) <= 1, ('Problem in your database: more than one user with email '
                                   "address '{0}'".format(email))
            if len(cur) == 0:
                raise LDAPNoSuchObjectResult("No person with email address '{0}' in "
                                             'database'.format(email))
            entry = cur[0]
        return _person_from_ldap_entry(entry)

    def add_person(self, person, ldap_conn, rdn_attr='uid'):
        """Add the given person in the LDAP directory."""
        # Check that username and email does not exists already
        for attr, attr_exists in (('username', self.username_exists), ('email', self.email_exists)):
            value = getattr(person, attr, None)
            if value is not None:
                if attr_exists(value, ldap_conn):
                    raise LDAPEntryAlreadyExistsResult('There is already a person with {attr} '
                                                       '{value}'.format(attr=attr, value=value))
        rdn_value = getattr(person, LDAP_ATTR_REV_MAPPING[rdn_attr])
        rdn = '{attr}={value}'.format(attr=rdn_attr, value=rdn_value)
        # Build and save the new entry
        with self.add_cursor(ldap_conn, self._person_class, self._people_basedn) as wcur:
            ldap_person = wcur.new('{rdn},{base_dn}'.format(rdn=rdn, base_dn=self._people_basedn))
            for attr in LDAP_ATTR_MAPPING:
                value = getattr(person, attr, None)
                if value is not None:
                    setattr(ldap_person, LDAP_ATTR_MAPPING[attr], value)
            ldap_person.cn = u'{0} {1}'.format(person.first_name, person.surname)

    def update_person(self, person, ldap_conn):
        """Update the given person in the LDAP directory."""
        # Find the person by its ursername or email
        with self.read_cursor(ldap_conn, self._person_class, self._people_basedn,
                              'uid:={username}'.format(username=person.username)) as cur:
            cur.search()
            assert len(cur) <= 1, ('Problem in your database: more than one user with username '
                                   "'{1}'".format(person.username))
            if len(cur) == 0:
                raise LDAPNoSuchObjectResult("No person with username '{0}' in "
                                             'database'.format(person.username))
            with self.update_cursor(cur) as wcur:
                entry = wcur[0]
                for attr, ldap_attr in LDAP_ATTR_MAPPING.items():
                    value = getattr(person, attr, None)
                    if value is None:
                        continue
                    try:
                        ldap_value = getattr(entry, ldap_attr)
                    except LDAPCursorError:
                        setattr(entry, ldap_attr, value)
                    else:
                        if ldap_value.value != value:
                            setattr(entry, ldap_attr, value)

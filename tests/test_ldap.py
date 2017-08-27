# -*- coding: utf-8 -*-

"""Tests about storing person information in an LDAP directory."""

import os
import unittest

from ldap3.core.exceptions import LDAPEntryAlreadyExistsResult, LDAPNoSuchObjectResult

from aliquis import create_app
from aliquis.person import person as new_person
from aliquis.ldap import LDAP_ATTR_MAPPING, LDAPBackend


TEST_CONFIG = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'test-settings.ini')


def setup_add_ldap_person(ldap_backend, person_dict):
    ldap_dict = dict((LDAP_ATTR_MAPPING[attr], v) for attr, v in person_dict.items())
    ldap_dict['cn'] = '{0} {1}'.format(person_dict['first_name'], person_dict['surname'])
    ldap_dict['objectClass'] = ldap_backend._person_class
    with ldap_backend.admin_connection() as ldap_conn:
        ldap_conn.strategy.add_entry('uid={username},{base_dn}'.format(
            username=person_dict['username'], base_dn=ldap_backend._people_basedn
        ), ldap_dict)


def clean_people_tree(ldap_backend):
    with ldap_backend.admin_connection() as ldap_conn:
        for entry in ldap_backend.entries(ldap_conn, ldap_backend._person_class,
                                          ldap_backend._people_basedn):
            ldap_conn.strategy.remove_entry(entry.entry_dn)


class TestSearchPersonByUsername(unittest.TestCase):
    """Check person search by its username."""

    def setUp(self):
        super(TestSearchPersonByUsername, self).setUp()
        self.app = create_app(TEST_CONFIG)
        self.ldap_backend = LDAPBackend(self.app, fake=True)
        # Create a sample person in fake LDAP server
        self.jdoe = {
            'first_name': 'John',
            'surname': 'Doe',
            'email': 'jdoe@example.org',
            'username': 'jdoe',
            'password': ('$6$jOKS9rH/B2hK.6SK$kc3TQJ4AbcJGFzAJZD5yLXL.EiI4eJmdjlK5YHGIu9P2vP7GGj6P4'
                         's88nHB.SQWY8sNYoRCAEEeK4JR7iwEyJ1'),
            'display_name': 'John Doe',
        }
        setup_add_ldap_person(self.ldap_backend, self.jdoe)

    def tearDown(self):
        super(TestSearchPersonByUsername, self).tearDown()
        clean_people_tree(self.ldap_backend)

    def test_username_exists(self):
        """Check that ``username_exists`` function returns correct boolean value."""
        with self.ldap_backend.admin_connection() as ldap_conn:
            self.assertTrue(self.ldap_backend.username_exists('jdoe', ldap_conn))
            self.assertFalse(self.ldap_backend.username_exists('john', ldap_conn))
            self.assertFalse(self.ldap_backend.username_exists('', ldap_conn))
            self.assertFalse(self.ldap_backend.username_exists(None, ldap_conn))

    def test_person_by_username(self):
        """Check that a person can be found by its username."""
        with self.ldap_backend.admin_connection() as ldap_conn:
            p = self.ldap_backend.person_by_username('jdoe', ldap_conn)
        self.assertEqual(p, new_person(**self.jdoe))

    def test_not_found_by_username(self):
        """Check that an error is raised when searching with an inexistent username."""
        with self.assertRaises(LDAPNoSuchObjectResult):
            with self.ldap_backend.admin_connection() as ldap_conn:
                self.ldap_backend.person_by_username('john', ldap_conn)
        with self.assertRaises(LDAPNoSuchObjectResult):
            with self.ldap_backend.admin_connection() as ldap_conn:
                self.ldap_backend.person_by_username('', ldap_conn)
        with self.assertRaises(LDAPNoSuchObjectResult):
            with self.ldap_backend.admin_connection() as ldap_conn:
                self.ldap_backend.person_by_username(None, ldap_conn)

    def test_duplicate_username(self):
        """Check that an error is raised when searching for a duplicated username."""
        with self.ldap_backend.admin_connection() as ldap_conn:
            ldap_conn.strategy.add_entry(
                'uid=jane,{base_dn}'.format(base_dn=u'{0},{1}'.format(
                    self.app.config['LDAP_USER_DN'], self.app.config['LDAP_BASE_DN']
                )),
                {
                    'objectClass': 'inetOrgPerson',
                    'givenName': 'Jane',
                    'sn': 'Doe',
                    'mail': 'jdoe@example.org',
                    'uid': 'jdoe',
                    'userPassword': ('$6$jOKS9rH/B2hK.6SK$kc3TQJ4AbcJGFzAJZD5yLXL.EiI4eJmdjlK5YHGIu'
                                     '9P2vP7GGj6P4s88nHB.SQWY8sNYoRCAEEeK4JR7iwEyJ1'),
                    'displayName': 'Jane Doe',
                    'cn': 'Jane Doe',
                }
            )
        with self.assertRaises(AssertionError):
            with self.ldap_backend.admin_connection() as ldap_conn:
                self.ldap_backend.person_by_username('jdoe', ldap_conn)


class TestSearchPersonByEmail(unittest.TestCase):
    """Check person search by email."""

    def setUp(self):
        super(TestSearchPersonByEmail, self).setUp()
        self.app = create_app(TEST_CONFIG)
        self.ldap_backend = LDAPBackend(self.app, fake=True)
        # Create a sample person in fake LDAP server
        self.jdoe = {
            'first_name': 'John',
            'surname': 'Doe',
            'email': 'jdoe@example.org',
            'username': 'jdoe',
            'password': ('$6$jOKS9rH/B2hK.6SK$kc3TQJ4AbcJGFzAJZD5yLXL.EiI4eJmdjlK5YHGIu9P2vP7GGj6P4'
                         's88nHB.SQWY8sNYoRCAEEeK4JR7iwEyJ1'),
        }
        setup_add_ldap_person(self.ldap_backend, self.jdoe)

    def tearDown(self):
        super(TestSearchPersonByEmail, self).tearDown()
        clean_people_tree(self.ldap_backend)

    def test_email_exists(self):
        """Check that ``email_exists`` function returns correct boolean value."""
        with self.ldap_backend.admin_connection() as ldap_conn:
            self.assertTrue(self.ldap_backend.email_exists('jdoe@example.org', ldap_conn))
            self.assertFalse(self.ldap_backend.email_exists('john.doe@example.org', ldap_conn))
            self.assertFalse(self.ldap_backend.email_exists('', ldap_conn))
            self.assertFalse(self.ldap_backend.email_exists(None, ldap_conn))

    def test_person_by_email(self):
        """Check that a person can be found by its username."""
        with self.ldap_backend.admin_connection() as ldap_conn:
            p = self.ldap_backend.person_by_email('jdoe@example.org', ldap_conn)
        self.assertEqual(p, new_person(**self.jdoe))

    def test_not_found_by_mail(self):
        """Check that an error is raised when searching with an inexistent username."""
        with self.assertRaises(LDAPNoSuchObjectResult):
            with self.ldap_backend.admin_connection() as ldap_conn:
                self.ldap_backend.person_by_email('john@example.org', ldap_conn)
        with self.assertRaises(LDAPNoSuchObjectResult):
            with self.ldap_backend.admin_connection() as ldap_conn:
                self.ldap_backend.person_by_email('', ldap_conn)
        with self.assertRaises(LDAPNoSuchObjectResult):
            with self.ldap_backend.admin_connection() as ldap_conn:
                self.ldap_backend.person_by_email(None, ldap_conn)

    def test_duplicate_email(self):
        """Check that an error is raised when searching for a duplicated username."""
        setup_add_ldap_person(self.ldap_backend, {
            'first_name': 'Jane',
            'surname': 'Doe',
            'email': 'jdoe@example.org',
            'username': 'jane',
            'password': ('$6$jOKS9rH/B2hK.6SK$kc3TQJ4AbcJGFzAJZD5yLXL.EiI4eJmdjlK5YHGIu9P2vP7GGj6P4'
                         's88nHB.SQWY8sNYoRCAEEeK4JR7iwEyJ1'),
        })
        with self.assertRaises(AssertionError):
            with self.ldap_backend.admin_connection() as ldap_conn:
                self.ldap_backend.person_by_email('jdoe@example.org', ldap_conn)


class TestAddPerson(unittest.TestCase):
    """Check adding a person in LDAP directory."""

    def setUp(self):
        super(TestAddPerson, self).setUp()
        self.app = create_app(TEST_CONFIG)
        self.ldap_backend = LDAPBackend(self.app, fake=True)
        # Create a sample person in fake LDAP server
        setup_add_ldap_person(self.ldap_backend, {
            'first_name': 'John',
            'surname': 'Doe',
            'email': 'jdoe@example.org',
            'username': 'jdoe',
            'password': ('$6$jOKS9rH/B2hK.6SK$kc3TQJ4AbcJGFzAJZD5yLXL.EiI4eJmdjlK5YHGIu9P2vP7GGj6P4'
                         's88nHB.SQWY8sNYoRCAEEeK4JR7iwEyJ1'),
        })

    def tearDown(self):
        """Empty the LDAP tree after each test function."""
        super(TestAddPerson, self).tearDown()
        clean_people_tree(self.ldap_backend)

    def test_add_person(self):
        """Check that a new person can be added to the directory tree."""
        jane = new_person(**{
            'first_name': 'Jane',
            'surname': u'Doé',
            'email': 'jane.doe@example.org',
            'username': 'jane',
            'password': 'jdoe1234',
        })
        # Check first that there is no jane in the directory
        with self.ldap_backend.admin_connection() as ldap_conn:
            self.assertFalse(self.ldap_backend.username_exists(jane.username, ldap_conn))
        # Add jane and check that there is now one jane
        with self.ldap_backend.admin_connection() as ldap_conn:
            self.ldap_backend.add_person(jane, ldap_conn)
        with self.ldap_backend.admin_connection() as ldap_conn:
            self.assertTrue(self.ldap_backend.username_exists(jane.username, ldap_conn))
            p = self.ldap_backend.person_by_username(jane.username, ldap_conn)
        self.assertEqual(p, jane)
        self.assertTrue(p.check_password(jane.password))

    def test_cannot_add_same_username(self):
        """Check that a new person cannot be added if username already exists."""
        john = new_person(**{
            'first_name': 'John',
            'surname': u'Doé',
            'email': 'john.doe@example.org',
            'username': 'jdoe',
            'password': 'jdoe1234',
        })
        with self.assertRaises(LDAPEntryAlreadyExistsResult):
            with self.ldap_backend.admin_connection() as ldap_conn:
                self.ldap_backend.add_person(john, ldap_conn)

    def test_cannot_add_same_email(self):
        """Check that a new person cannot be added if email already exists."""
        john = new_person(**{
            'first_name': 'John',
            'surname': u'Doé',
            'email': 'jdoe@example.org',
            'username': 'john',
            'password': 'jdoe1234',
        })
        with self.assertRaises(LDAPEntryAlreadyExistsResult):
            with self.ldap_backend.admin_connection() as ldap_conn:
                self.ldap_backend.add_person(john, ldap_conn)


class TestUpdatePerson(unittest.TestCase):
    """Check updating a person in LDAP directory."""

    def setUp(self):
        super(TestUpdatePerson, self).setUp()
        self.app = create_app(TEST_CONFIG)
        self.ldap_backend = LDAPBackend(self.app, fake=True)
        # Create a sample person in fake LDAP server
        self.jdoe = {
            'first_name': 'John',
            'surname': 'Doe',
            'username': 'jdoe',
        }
        setup_add_ldap_person(self.ldap_backend, self.jdoe)

    def tearDown(self):
        """Empty the LDAP tree after each test function."""
        super(TestUpdatePerson, self).tearDown()
        clean_people_tree(self.ldap_backend)

    def test_update_text_attributes(self):
        """Check that first_name, surname, email, display_name are updated correctly."""
        for attr, new_value in (
                ('first_name', 'Johnny'),
                ('surname', u'Doé'),
                ('email', u'john.doe@example.org'),
                ('display_name', u'J. Doe'),
        ):
            john = self.jdoe.copy()
            john[attr] = new_value
            with self.ldap_backend.admin_connection() as ldap_conn:
                self.ldap_backend.update_person(new_person(**john), ldap_conn)
            with self.ldap_backend.admin_connection() as ldap_conn:
                p = self.ldap_backend.person_by_username(self.jdoe['username'], ldap_conn)
            self.assertEqual(getattr(p, attr), new_value)

    def test_update_password(self):
        """Check that password is updated correctly."""
        john = self.jdoe.copy()
        john['password'] = 'foobar1234'
        with self.ldap_backend.admin_connection() as ldap_conn:
            self.ldap_backend.update_person(new_person(**john), ldap_conn)
        with self.ldap_backend.admin_connection() as ldap_conn:
            p = self.ldap_backend.person_by_username(self.jdoe['username'], ldap_conn)
        self.assertTrue(p.check_password('foobar1234'))

    def test_cannot_update_new_person(self):
        """Check that a person cannot be updated if it does not exists in database."""
        john = self.jdoe.copy()
        john['username'] = 'john'
        with self.assertRaises(LDAPNoSuchObjectResult):
            with self.ldap_backend.admin_connection() as ldap_conn:
                self.ldap_backend.update_person(new_person(**john), ldap_conn)


if __name__ == '__main__':
    unittest.main()

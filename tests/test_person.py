# -*- coding: utf-8 -*-

"""Tests regarding the Person class."""

import unittest

from six import text_type

from aliquis.person import person


class TestPersonFactory(unittest.TestCase):
    """Check the ``person`` factory function that creates ``Person`` instances."""

    def setUp(self):
        super(TestPersonFactory, self).setUp()
        self.jdoe = {
            'first_name': 'John',
            'surname': u'Doé',
            'display_name': u'J. Doé',
            'email': 'john.doe@priv.example.org',
            'username': 'jdoe',
            'password': 'jdoe01234',
        }

    def test_person(self):
        """Check that ``person`` creates a correct ``Person`` instance."""
        p = person(**self.jdoe)
        for attr_name in ('first_name', 'surname', 'display_name', 'email', 'username'):
            self.assertEqual(getattr(p, attr_name), self.jdoe[attr_name])
        self.assertTrue(p.check_password(self.jdoe['password']))

    def test_person_minimal(self):
        """Check that ``person`` creates a correct ``Person`` instance withtout optional values."""
        minimal_attributes = ('first_name', 'surname', 'username')
        minimal_jdoe = dict((k, v) for k, v in self.jdoe.items() if k in minimal_attributes)
        p = person(**minimal_jdoe)
        for attr_name in minimal_attributes:
            self.assertEqual(getattr(p, attr_name), minimal_jdoe[attr_name])
        self.assertEqual(p.display_name, u'{0} {1}'.format(minimal_jdoe['first_name'],
                                                           minimal_jdoe['surname']))

    def test_person_wrong_values(self):
        """Check that ``person`` cannot create a ``Person`` instance if needed values are wrong."""
        for empty_attr_name in ('first_name', 'surname'):
            wrong_jdoe = self.jdoe.copy()
            wrong_jdoe[empty_attr_name] = u''
            with self.assertRaises(ValueError):
                person(**wrong_jdoe)
        for none_attr_name in ('first_name', 'surname'):
            wrong_jdoe = self.jdoe.copy()
            wrong_jdoe[none_attr_name] = None
            with self.assertRaises(ValueError):
                person(**wrong_jdoe)
        for wrong_attr_name, wrong_value in (
                ('email', u'john.doé@priv.example.org'),
                ('email', 'john.doe@priv_example.org'),
                ('email', 'john.doe.priv.example.org'),
                ('username', u'jdoé'),
                ('username', '0jdoe'),
        ):
            wrong_jdoe = self.jdoe.copy()
            wrong_jdoe[wrong_attr_name] = wrong_value
            with self.assertRaises(ValueError):
                person(**wrong_jdoe)


class TestPersonDisplayName(unittest.TestCase):
    """Check a person's display name behavior."""

    def setUp(self):
        super(TestPersonDisplayName, self).setUp()
        self.jdoe = person(**{
            'first_name': 'John',
            'surname': u'Doé',
            'email': 'john.doe@priv.example.org',
            'username': 'jdoe',
            'password': 'jdoe01234',
        })

    def test_default_display_name(self):
        """Check that a default display name is returned if no one is provided."""
        self.assertEqual(self.jdoe.display_name, u'{0} {1}'.format(self.jdoe.first_name,
                                                                   self.jdoe.surname))
        self.assertEqual(text_type(self.jdoe), self.jdoe.display_name)

    def test_display_name_override(self):
        """Check that the display name can be overriden."""
        self.jdoe.display_name = u'J. Doé'
        self.assertEqual(self.jdoe.display_name, u'J. Doé')
        self.assertEqual(text_type(self.jdoe), self.jdoe.display_name)
        self.jdoe.display_name = u'Doé John'
        self.assertEqual(self.jdoe.display_name, u'Doé John')
        self.assertEqual(text_type(self.jdoe), self.jdoe.display_name)

    def test_display_name_not_empty(self):
        """Check that the display name cannot be empty (returns the default value)."""
        self.jdoe.display_name = ''
        self.assertEqual(self.jdoe.display_name, u'{0} {1}'.format(self.jdoe.first_name,
                                                                   self.jdoe.surname))
        self.jdoe.display_name = u'J. Doe'
        self.jdoe.display_name = None
        self.assertEqual(self.jdoe.display_name, u'{0} {1}'.format(self.jdoe.first_name,
                                                                   self.jdoe.surname))


class TestPersonUsername(unittest.TestCase):
    """Check a person's username."""

    def test_cannot_update_username(self):
        jdoe = person(**{
            'first_name': 'John',
            'surname': u'Doé',
            'username': 'jdoe',
        })
        with self.assertRaises(AttributeError):
            jdoe.username = 'john.doe'


class TestPersonPassword(unittest.TestCase):
    """Check a person's password."""

    def setUp(self):
        super(TestPersonPassword, self).setUp()
        self.jdoe_password = 'jdoe01234'
        self.jdoe = person(**{
            'first_name': 'John',
            'surname': u'Doé',
            'email': 'john.doe@priv.example.org',
            'username': 'jdoe',
            'password': self.jdoe_password,
        })

    def test_password_stored_hashed(self):
        """Check that a password is not stored in clear text."""
        self.assertNotEqual(self.jdoe.password, self.jdoe_password)
        self.assertTrue(self.jdoe.password.startswith('$6$'))

    def test_password_check(self):
        """Check that a password is correctly checked."""
        self.assertTrue(self.jdoe.check_password(self.jdoe_password))
        self.assertFalse(self.jdoe.check_password('jdoe01233'))

    def test_password_change(self):
        """Check that a password can be changed."""
        self.jdoe.password = 'jdoe01233'
        self.assertFalse(self.jdoe.check_password(self.jdoe_password))
        self.assertTrue(self.jdoe.check_password('jdoe01233'))

    def test_cannot_set_empty_password(self):
        """Check that a password can be set to None."""
        with self.assertRaises(ValueError):
            self.jdoe.password = ''
        with self.assertRaises(ValueError):
            self.jdoe.password = None


class TestPersonComparison(unittest.TestCase):
    """Check comparison between ``Person`` instances."""

    def setUp(self):
        super(TestPersonComparison, self).setUp()
        self.jdoe = {
            'first_name': 'John',
            'surname': u'Doé',
            'email': 'jdoe@priv.example.org',
            'username': 'jdoe',
            'password': 'jdoe01234',
        }

    def test_person_equality(self):
        """Check that two persons are equal even if passwords and display names are different."""
        john = {
            'display_name': 'J. Doe',
            'password': 'jdoe9876',
        }
        for attr_name in ('first_name', 'surname', 'username', 'email'):
            john[attr_name] = self.jdoe[attr_name]
        self.assertEqual(person(**self.jdoe), person(**john))

    def test_person_difference(self):
        """Check that two persons are not equal even if passwords and display names are equal."""
        john = self.jdoe.copy()
        john['first_name'] = 'Johnn'
        self.assertNotEqual(person(**self.jdoe), person(**john))
        john = self.jdoe.copy()
        john['surname'] = 'Doe'
        self.assertNotEqual(person(**self.jdoe), person(**john))
        john = self.jdoe.copy()
        john['username'] = 'john'
        self.assertNotEqual(person(**self.jdoe), person(**john))
        john = self.jdoe.copy()
        john['email'] = 'john@priv.example.org'
        self.assertNotEqual(person(**self.jdoe), person(**john))

    def test_person_equality_no_email(self):
        """Check that two persons can be equal if email address is missing."""
        john1 = dict((k, v) for k, v in self.jdoe.items() if k in ('first_name', 'surname',
                                                                   'username'))
        john2 = dict((k, v) for k, v in self.jdoe.items() if k in ('first_name', 'surname',
                                                                   'username'))
        self.assertEqual(person(**john1), person(**john2))

    def test_person_difference_no_email(self):
        """Check that two persons are not equal if both have no email address and different first
        names."""
        john = dict((k, v) for k, v in self.jdoe.items() if k in ('first_name', 'surname',
                                                                  'username'))
        jane = dict((k, v) for k, v in self.jdoe.items() if k in ('first_name', 'surname',
                                                                  'username'))
        jane['first_name'] = 'Jane'
        self.assertNotEqual(person(**john), person(**jane))


if __name__ == '__main__':
    unittest.main()

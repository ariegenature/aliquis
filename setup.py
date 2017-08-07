"""aliquis setup module."""

from codecs import open
from setuptools import setup, find_packages
import os

project_name = 'aliquis'
root_path = os.path.abspath(os.path.dirname(__file__))

# Get the version from the VERSION file
with open(os.path.join(root_path, project_name, 'VERSION'),
          encoding='utf-8') as f:
    version = f.read().strip()

# Get the long description from the README file
with open(os.path.join(root_path, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name=project_name,
    version=version,
    description='A web service allowing to manage users in a LDAP directory.',
    long_description=long_description,
    url='https://github.com/ygversil/aliquis',
    author='Yann Voté',
    author_email='ygversil@openmailbox.org',
    license='LGPLv3+',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'Framework :: Flask',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU Lesser General Public License v3 or '
        'later (LGPLv3+)',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Database :: Front-Ends',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
        'Topic :: System :: Systems Administration :: '
        'Authentication/Directory :: LDAP',
    ],
    keywords='ldap directory authentication system flask wsgi web',
    packages=find_packages(exclude=['docs', 'tests']),
    install_requires=['flask', 'konfig', 'ldap3', 'six'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    extras_require={
        'codestyle': ['check-manifest', 'readme_renderer', 'flake8'],
        'dev': ['Sphinx'],
        'test': ['pytest'],
    },
    package_data={
        project_name: ['VERSION'],
    },
    data_files=[],
    entry_points={},
)

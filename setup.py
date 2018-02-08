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

# Collect package data to be installed (and in particular i18n messages and Vue.js client source)
package_data = [
    'VERSION',
    'static/*',
]
for root, _, fnames in os.walk(os.path.join(project_name, 'i18n')):
    for fname in fnames:
        _, ext = os.path.splitext(fname)
        if ext == '.mo':
            package_data.append(os.path.join(
                root.replace('{0}/'.format(project_name), '', 1),
                fname
            ))
for root, dirs, fnames in os.walk(os.path.join(project_name, 'aliquisjs')):
    for fname in fnames:
        package_data.append(os.path.join(root.replace('{0}/'.format(project_name), '', 1), fname))
    if 'node_modules' in dirs:
        dirs.remove('node_modules')
    if 'coverage' in dirs:
        dirs.remove('coverage')
print(package_data)


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
    install_requires=[
        'Flask-Babel',
        'Flask-Celery-Helper',
        'Flask-Login',
        'Flask-WTF',
        'chaussette',
        'celery',
        'flask',
        'flask-ldap3-login',
        'itsdangerous',
        'konfig',
        'ldap3',
        'redis',  # XXX: make this configurable in optional 'redis' target
        'requests',  # XXX: make this configurable in optional 'sendgrid' target
        'six',
        'xdg',
    ],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    extras_require={
        'codestyle': ['check-manifest', 'readme_renderer', 'flake8'],
        'dev': [
            'Sphinx',
            'bumpversion',
        ],
        'test': ['pytest'],
    },
    package_data={
        project_name: package_data,
    },
    data_files=[
        ('examples', ['aliquis.ini.example', 'circus.ini.example'])
    ],
    entry_points={
        'console_scripts': ['aliquis=aliquis.__main__:main'],
    },
)

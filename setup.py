import os
import sys
from setuptools import setup, find_packages
from django.core import management

with open(os.path.join(os.path.dirname(__file__), 'README.markdown')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

# compile django.po files (translations)
curdir = os.getcwd()
os.chdir('paiji2_carpooling')
management.call_command('compilemessages', stdout=sys.stdout)
os.chdir(curdir)

setup(
    name='django-paiji2-carpooling',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    description='A simple carpooling app',
    long_description=README,
    url='https://github.com/rezometz/django-paiji2-carpooling',
    author='Supelec Rezo Metz',
    author_email='paiji-dev@rezometz.org',
    license='Affero GPL v3+',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    install_requires=[
        'django-bootstrap3>=6',
        'django-modular-blocks',
        'django-paiji2-utils>=0.1',
    ]
)

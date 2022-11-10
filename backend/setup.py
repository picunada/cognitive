
# -*- coding: utf-8 -*-
from setuptools import setup

long_description = None
INSTALL_REQUIRES = [
    'django>=4.1.2',
    'djangorestframework>=3.14.0',
    'django-filter>=22.1',
    'pip>=22.3',
    'django-model-utils>=4.2.0',
    'setuptools>=65.5.0',
    'djangorestframework-api-key>=2.2.0',
    'djangorestframework-simplejwt>=5.2.1',
    'regex>=2022.9.13',
    'drf-yasg>=1.21.4',
    'cryptography>=38.0.1',
]

setup_kwargs = {
    'name': '',
    'version': '',
    'description': '',
    'long_description': long_description,
    'license': 'None',
    'author': '',
    'author_email': 'Daniil Bezuglov <daniil.bezuglov@lockerbot.io>',
    'maintainer': None,
    'maintainer_email': None,
    'url': '',
    'packages': [
        'cognitive',
        'cognitive.apps.organization',
        'cognitive.apps.core',
        'cognitive.apps.user',
        'cognitive.apps.organization.migrations',
        'cognitive.apps.core.migrations',
        'cognitive.apps.user.migrations',
    ],
    'package_data': {'': ['*']},
    'install_requires': INSTALL_REQUIRES,
    'python_requires': '>=3.10',

}


setup(**setup_kwargs)

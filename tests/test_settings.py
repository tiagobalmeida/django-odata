import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#sys.path.append(
#	os.path.join(
#		os.path.dirname(os.path.realpath(__file__)),
#		'../'))

SECRET_KEY = 'fake-key'

INSTALLED_APPS = [
    'django_odata',
    'tests'
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
import os
import sys

sys.path.append(
	os.path.join(
		os.path.dirname(os.path.realpath(__file__)),
		'../'))

SECRET_KEY = 'fake-key'
INSTALLED_APPS = [
    'django_odata',
    'tests'
]
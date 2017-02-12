def pytest_configure():
	from django.conf import settings

	MIDDLEWARE = (
			'django.middleware.common.CommonMiddleware',
			'django.contrib.sessions.middleware.SessionMiddleware',
			'django.contrib.auth.middleware.AuthenticationMiddleware',
			'django.contrib.messages.middleware.MessageMiddleware',
	)

	settings.configure(
			DEBUG_PROPAGATE_EXCEPTIONS=True,
			DATABASES={
					'default': {
							'ENGINE': 'django.db.backends.sqlite3',
							'NAME': ':memory:'
					}
			},
			SITE_ID=1,
			SECRET_KEY='some key',
			USE_I18N=True,
			USE_L10N=True,
			STATIC_URL='/static/',
			ROOT_URLCONF='tests.urls',
			TEMPLATES=[
					{
							'BACKEND': 'django.template.backends.django.DjangoTemplates',
							'APP_DIRS': True,
					},
			],
			MIDDLEWARE=MIDDLEWARE,
			MIDDLEWARE_CLASSES=MIDDLEWARE,
			INSTALLED_APPS=(
					'django.contrib.auth',
					'django.contrib.contenttypes',
					'django.contrib.sessions',
					'django.contrib.sites',
					'django.contrib.staticfiles',
					'django_odata',
					'tests',
			),
			PASSWORD_HASHERS=(
					'django.contrib.auth.hashers.MD5PasswordHasher',
			),
			# django odata settings
			DJANGO_ODATA={
					'app': 'tests', # TODO, redundant
					'models': {
						'tests': [
							'tests.Post',
							'tests.Tag',
							'tests.Author'
						]
					}
			}
	)

	try:
			import django
			import sys
			print(sys.path)
			django.setup()
	except AttributeError:
			pass

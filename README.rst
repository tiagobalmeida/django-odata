============
Django-Odata
============

Django-Odata exposes your models via the Odata protocol.


Quick start for django users
------------------------------

1. Add "django_odata" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'django_odata',
    ]

2. Include the polls URLconf in your project urls.py like this::

    url(r'^odata/', include('django_odata.urls')),


Quick start for django-odata developers
------------------------------------------
```
git clone https://github.com/jumpifzero/django-odata.git
cd django-odata
python3 -m venv env
source env/bin/activate
```

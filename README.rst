============
Django-Odata
============

Django-Odata exposes your models via the Odata protocol.


Quick start
-----------

1. Add "django_odata" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'django_odaya',
    ]

2. Include the polls URLconf in your project urls.py like this::

    url(r'^odata/', include('django_odata.urls')),


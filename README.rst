============
Django-Odata
============

Django-Odata exposes your models via the Odata protocol.

*Warning!* This code is still under development and has not reached production-grade quality. In terms of features it currently supports the following:

- Reading an Entity Set
- Complex $filter expressions
- Reading an Entity

All features are implemented with a large quantity of automated tests.

Aim of the project
------------------

- Full OData V2 support in json
- Investigate if we can support odata push messages.

All code is still on the dev branch.


Quick start
-----------

1. Add "django_odata" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'django_odata',
    ]

2. Include the polls URLconf in your project urls.py like this::

    url(r'^odata/', include('django_odata.urls')),



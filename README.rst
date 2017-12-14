============
Django-OData
============

Django-Odata exposes your models via the OData V4 protocol.

OData is an open protocol built on top of HTTP that allows full CRUD of remote objects as well as a powerfull query language.

This project is meant to be a plug and play Django application. 
You install it on your Django project and it will *automagically* provide
an OData endpoint to interact with your Django models instances.

Project status:
 - Under development. Delete and update functionality is not yet implemented.
 - $filter of entity sets seems to work and passes basic unit tests but a lot more work is still required
 - $top and $skip are working.
 - Only basic data types are implemented (integers/strings) no support yet for dates and more advanced ones like Geo coordinates.
 - Reading an entity is working but requires more tests.


Roadmap
--------

v0.9: 
 - Full OData V4 support (read/write) with minimal metadata. 
 - No Function imports. 
 - Support for exposing models of one django app only (not multiple apps' models under the same endpoint)


v1.0:
 - Support for configuring which models are readable and which are writable by allowing a class to be specified by the end user as the authorizer of those operations.


v1.1:
 - Support for multiple django apps under the same endpoint.


Things this project will probably never support:
OData V2/V3 as this requires implementing serialization into XML. V2 is also more complex than V4 in some ways.


Quick start for django-odata users
------------------------------
1. Install it::

	pip install django-odata


2. Add "django_odata" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'django_odata',
    ]

3. Include the polls URLconf in your project urls.py like this::

    path('odata/', include('django_odata.urls'))


4. Configure it on you settings.py file.
   Minimal configuration is a DJANGO_ODATA dict on your settings.py,
   with an 'app' key whose value is the appname and a 'sets' key whose value
   is a dict with all the Models to expose. Check /samples/backend/backend/settings.py for an example.

5. That's it! Your project will now allow full read and write of all your specified models under url /odata.

If you want to run a sample UI5 project locally, connected to a local django-odata server, do the following:
```
git clone https://github.com/jumpifzero/django-odata.git
cd django-odata
python3 -m venv env
source env/bin/activate
pip3 install -r requirements.txt
cd samples/fullstack
# Create a resources link pointing to a local installation of openui5. For example:
ln -s -T /home/tiago/lib/ui5/sapui5-1.40.12/resources ./resources
# Run django-odata server
# Run a server for the index.html
python3 -m http.server
# Open browser in http://localhost:8000
# To run the backend
# On another session
cd samples/fullstack/backend
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py loaddata Suppliers
```
   

Quick start for django-odata developers
------------------------------------------

```
git clone https://github.com/jumpifzero/django-odata.git
cd django-odata
python3 -m venv env
source env/bin/activate
pip3 install -r requirements.txt
```

You can run the automated tests with
```
./runTests.sh
```

About the code
------------------------------------------
Changes that need to be done are marked with the string TODO

The tag MULTIPLE_APPS marks changes for version 2 when we want
	to support exposing models from multiple django applications.

The tag PERFORMANCE marks future changes so that it performs faster.


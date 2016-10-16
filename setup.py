import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 
					'README.rst')) as readme:
	README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), 
																				os.pardir)))

setup(
    name='django-odata',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    license='MIT License',  # example license
    description=
    	'A Django app to expose your models via the OData protocol.',
    long_description=README,
    url='https://www.example.com/',
    author='Tiago Almeida',
    author_email='tiago.b.almeida@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.10',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
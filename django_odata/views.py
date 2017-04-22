# ============================================================
# OData requests handling
#
# (C) Tiago Almeida 2016
#
#
#
# ============================================================
import re
import json
from django.apps import apps
from django.conf import settings as djsettings
from django.core import serializers
from django.http import HttpResponse, HttpResponseNotAllowed
from django.template.response import TemplateResponse
from django.urls import reverse
from django.core.serializers.python import Serializer
from django.core.serializers.json import DjangoJSONEncoder
from .odata import *
from .urlparser import ResourcePath, QueryOptions
from .odata_to_django import *
from .serialization import GenericOdataJsonSerializer
import django_odata.odata_to_django as o2d
import django_odata.urlparser as urlparser
import django_odata.metadata


def metadata(request):
  """
  Handles request to /$metadata
  """
  current_app = djsettings.DJANGO_ODATA['app']
  django_models = o2d.get_app_models_names(current_app)
  metadata_schema = django_odata.metadata.MetadataSchema.from_django_models(
  	current_app, django_models)
  #pdb.set_trace()
  metadata_ctx = {
	  'namespace': 'django',
	  'entities': metadata_schema.entities,
	  'associations': metadata_schema.associations,
	  'entitysets': metadata_schema.entitysets 
  }
  return TemplateResponse(request, 
    'django_odata/metadata.xml',
    context=metadata_ctx,
    content_type='application/xml;charset=utf-8')


def root_get_response(request, query_options):
  # type: (object, ResourcePath, QueryOptions) -> object
  """
  Handles get request to the root of the service.
  This returns an object with a collections list.
  E.g.:
  http://services.odata.org/V2/Northwind/Northwind.svc/
  """
  current_app = djsettings.DJANGO_ODATA['app']
  root_response_data = o2d.get_root_response_data(current_app)
  import pdb
  #pdb.set_trace()
  response_content = root_response_data
  return HttpResponse(
    GenericOdataJsonSerializer.serialize(response_content),
    content_type='application/json')



def service_root(request):
  """
  Handles requests to the root of the service.
  """
  q  = urlparser.QueryOptions(request.GET)
  if request.method == 'GET':
    return root_get_response(request, q)



def handle_get_request(request, resource_path, query_options):
  # type: (object, ResourcePath, QueryOptions) -> object
  """
  Handles get requests. The response is also
  affected by the Query Options (as defined on the spec below)

  For info on what this should comply with, read:
  http://www.odata.org/documentation/odata-version-2-0/uri-conventions/

  """
  if not resource_path:
    return root_get_response(request,
    resource_path, query_options)
  orm_query = OrmQuery.from_resource_path(resource_path)
  result = orm_query.execute(query_options)
  return HttpResponse(result.serialize(query_options.format),
    content_type=
      'application/json;'
      'odata.metadata=minimal;'
      'odata.streaming=true;'
      'IEEE754Compatible=false;'
      'charset=utf-8')


def handle_post_request(request, resource_path, query_options):
  # type: (object, ResourcePath, QueryOptions) -> object
  """
  Handles POST requests which creates objects.
  The request must be targetting a collection, must contain a well-formed
  entity in the body .
  For info on what this should comply with, read:
  http://www.odata.org/getting-started/basic-tutorial/

  """
  rp = ResourcePath(resource_path)
  if rp.addresses_collection


def handle_request(request, odata_path): # type: (Object) -> Object
    """
    Handles all requests and delegates on sub methods based on the http
    method.
    """
    rp = ResourcePath(odata_path)
    q  = QueryOptions(request.GET)
    if not rp.statically_valid():
        return HttpResponse(status=404)
    if request.method == 'GET':
        return handle_get_request(request, rp, q)
    elif request.method == 'DELETE':
        return handle_delete_request(request, rp, q)
    elif request.method == 'PATCH':
        return handle_patch_request(request, rp, q)
    # TODO other methods
    return HttpResponseNotAllowed(['GET','DELETE','PATCH'])

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
from .urlparser import ResourcePath
from .odata_to_django import *
from .serialization import GenericOdataJsonSerializer
import odata_to_django as o2d

def root_get_response(request, resource_path, query_options):
    # type: (object, ResourcePath, QueryOptions) -> object
    """
    Handles get request to the root of the service.
    This returns an object with a collections list.
    E.g.:
    http://services.odata.org/V2/Northwind/Northwind.svc/
    """
    current_app = 'app' # TODO: deal with multiple apps
    root_response_data = o2d.get_root_response_data(current_app)
    response_content = {'EntitySets':list(root_response_data)}
    return GenericOdataJsonSerializer.serialize(response_content)


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
    return result.serialize(query_options.format)



def handle_request(request): # type: (Object) -> Object
    """
    Handles all requests and delegates on sub methods based on the http 
    method.
    """
    rp = ResourcePath(request.path_info)
    q  = QueryOptions(request.GET)
    if not rp.statically_valid():
      return HttpResponse(status=404)
    if request.method == 'GET':
      return handle_get_request(request, rp, q)
    # TODO non get requests
    pass
    return HttpResponseNotAllowed(['GET']) # only allow gets for now


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
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.urls import reverse
from django.core.serializers.python import Serializer
from django.core.serializers.json import DjangoJSONEncoder
from .odata import *
from .urlparser import ResourcePath
from .odata_to_django import *


def handle_get_collection(request, resource_path, query_options):
    """
    Handles get requests to collections. The response is also
    affected by the Query Options (as defined on the spec below)

    For info on what this should comply with, read:
    http://www.odata.org/documentation/odata-version-2-0/uri-conventions/
    
    Only works when the request is addressing a collection, Example:
    /Authors or /Publisher(1)/Books
    """
    orm_query = odata_resource_path_to_orm(resource_path)
    result = orm_query.execute(query_options)
    return result.serialize() # TODO format
    pass



def handle_get_request(request, resource_path, query_options):
    """
    Handles GET Requests
    """
    if resource_path.address_collection():
        return handle_get_collection(request, resource_path)
    pass



def handle_request(request): # type: (Object) -> Object
    """
    Handles all requests and delegates on sub methods based on the http 
    method.
    """
    rp = ResourcePath(request.path_info)
    q  = QueryOptions(request.GET)
    if not rp.statically_valid():
        return HttpResponse(status=404)
    if request.method = 'GET':
        return handle_get_request(request, rp, q)
    # if valid, result = execute request
    # serialize result
    pass


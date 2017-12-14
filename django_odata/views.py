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
import simplejson as sjson
from django.apps import apps
from django.conf import settings as djsettings
from django.core import serializers
from django.http import HttpResponse, HttpResponseNotAllowed
from django.http import HttpResponseBadRequest
from django.template.response import TemplateResponse
from django.urls import reverse
from django.core.serializers.python import Serializer
from django.core.serializers.json import DjangoJSONEncoder
from .odata import *
from .urlparser import ResourcePath, QueryOptions
from .odata_to_django import *
import django_odata.odata_to_django as o2d
import django_odata.urlparser as urlparser
import django_odata.metadata
import django_odata.serialization as serialization


def metadata(request):
    """
    Handles request to /$metadata
    """
    current_app = djsettings.DJANGO_ODATA['app']
    django_models = o2d.get_app_models_names(current_app)
    metadata_schema = django_odata.metadata.MetadataSchema.from_django_models(
        current_app, django_models)
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
    current_app = djsettings.DJANGO_ODATA['app'] # MULTIPLE_APPS
    root_response_data = o2d.get_root_response_data(current_app)
    import pdb
    #pdb.set_trace()
    response_content = root_response_data
    return HttpResponse(
        serialization.GenericOdataJsonSerializer.serialize(response_content),
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
                        content_type='application/json;'
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
    meta = django_odata.metadata
    current_app = djsettings.DJANGO_ODATA['app'] # MULTIPLE_APPS
    if resource_path.addresses_collection():
        req_body_json = sjson.loads(request.body.decode('utf-8'))
        # TODO: malformed json
        collection = resource_path.components()[0].collection_name()
        # TODO: A successful POST request to a navigation property's references 
        # collection adds a relationship to an existing entity. 
        # For the moment assuming the entityset is the
        # first and only component in the path.
        model = meta.get_django_model_by_name_for_app(current_app, collection)
        new_instance = model(**req_body_json)
        new_instance.save()
        # Serialize the new_instance and send it back. To do it, we build a query
        # for this specific object and serialize it the same way as the get
        # request. PERFORMANCE: Do not do a second query.
        query = model.objects.filter(id=new_instance.id)
        response_body = serialization.OrmQueryResult(query).serialize()
        return HttpResponse(response_body, 
            status=201,
            content_type=
                'application/json;'
                'odata.metadata=minimal;'
                'odata.streaming=true;'
                'IEEE754Compatible=false;'
                'charset=utf-8')
    else:
        return HttpResponseBadRequest()



def handle_patch_or_put_request(request, resource_path, query_options):
    # type: (object, ResourcePath, QueryOptions) -> object
    """
    Handles requests to update entities. (Method PATCH or PUT)

    For info on what this should comply with, read:
    http://www.odata.org/getting-started/basic-tutorial/

    Implementation is similar to getting an object by key but then changing
    the fields which are present in the request json.
    """
    meta = django_odata.metadata
    current_app = djsettings.DJANGO_ODATA['app'] # MULTIPLE_APPS
    if resource_path.addresses_entity_or_property():
        last_component = resource_path.components()[-1]
        components = resource_path.components()
        collection_name = last_component.collection_name()
        # Translate external collection name to model name
        collection_name = o2d.model_from_external_name(collection_name)
        model = meta.get_django_model_by_name_for_app(current_app, 
            collection_name)
        try:
            instance = model.objects.get(pk=last_component.key())
            req_body_json = sjson.loads(request.body.decode('utf-8'))
            # TODO: Handle malformed json
            # Update every property in the instance
            for item in req_body_json.items():
                instance.__setattr__(item[0], item[1])
            instance.save()
        except model.DoesNotExist as e:
            raise e # TODO - we should be sending a 404
        # 
        return HttpResponse('', 
            status=204,
            content_type=
                'IEEE754Compatible=false;'
                'charset=utf-8')
    else:
        return HttpResponseBadRequest()




def handle_delete_request(request, resource_path, query_options):
    # type: (object, ResourcePath, QueryOptions) -> object
    """
    Handles DELETE requests which deletes objects.
    The request must be targetting an entity, must contain a well-formed
    entity in the body .
    For info on what this should comply with, read:
    http://www.odata.org/getting-started/basic-tutorial/
    """
    meta = django_odata.metadata
    current_app = djsettings.DJANGO_ODATA['app'] # MULTIPLE_APPS
    if resource_path.addresses_entity_or_property():
        last_component = resource_path.components()[-1]
        components = resource_path.components()
        collection_name = last_component.collection_name()
        # Translate external collection name to model name
        collection_name = o2d.model_from_external_name(collection_name)
        model = meta.get_django_model_by_name_for_app(current_app, 
            collection_name)
        try:
            instance = model.objects.get(pk=last_component.key())
            instance.delete()
        except model.DoesNotExist as e:
            raise e # TODO
        # 
        return HttpResponse('', 
            status=204,
            content_type=
                'IEEE754Compatible=false;'
                'charset=utf-8')
    else:
        return HttpResponseBadRequest()


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
        # Reading entities
        return handle_get_request(request, rp, q)
    elif request.method == 'DELETE':
        # Delete an entity
        return handle_delete_request(request, rp, q)
    elif request.method == 'PATCH' or request.method == 'PUT':
        # Update an entity
        return handle_patch_or_put_request(request, rp, q)
    elif request.method == 'POST':
        # Create entity
        return handle_post_request(request, rp, q)        
    # TODO other methods
    return HttpResponseNotAllowed(['GET','DELETE','PATCH'])

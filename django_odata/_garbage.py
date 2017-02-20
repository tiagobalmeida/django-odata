# =====================
# Old code







def get_set(request, set_name):
  """
  Handles an odata request for an EntitySet get.
  Applies $filter, $top, $skip, $order_by

  For info on what this should comply with, read:
  http://www.odata.org/documentation/odata-version-2-0/uri-conventions/
  """
  # Odata installation config
  app = djsettings.DJANGO_ODATA['app']
  # TODO: Raise improperly configured
  # TODO: Multiple apps
  # URL Query Options
  q_order_by  = request.GET.get('$order_by', False)
  q_filter_by = request.GET.get('$filter', False)
  q_skip =  request.GET.get('$skip', False)
  q_top  =  request.GET.get('$top', False)
  # Query
  EntityModel = apps.get_model(app, set_name)
  query_result = EntityModel.objects.all()
  if q_filter_by:
    query_result = set_filter(query_result, q_filter_by)
  if q_order_by:
    query_result = _order_by(query_result, q_order_by)
  service_root = reverse('odata_service_root')
  s = OdataJsonSerializer(service_root, set_name)
  if q_top and q_skip:
    query_result = query_result[int(q_skip):int(q_skip)+int(q_top)]
  return HttpResponse(s.serialize(query_result),
    content_type="application/json")


def handle(request, odata_path):
  return get_set(request, odata_path)


# ===================================================================
# Garbage code
# ===================================================================

def deleteme():
  # take odata_path split by /
  # components = odata_path.split('/')
  # odata_filter = request.GET.get('$filter', None)
  # is this a query for an entity?
  if re.search('\w+\(.*\)', components[0]):
    entity_query = components[0] 
  else: 
    entityset_query = components[0] 
  settings = djsettings.DJANGO_ODATA
  # app_base_path = djsettings.base_path
  # Try to understand what kind of request is this
  # import pdb; pdb.set_trace()
  #import importlib
  #module_name = ".DjangoGenerator"
  #class_name = "DjangoGenerator"
  #Generator = getattr(importlib.import_module(module_name), class_name)
  #generator = Generator(models)
  from django.apps import apps
  MyModel = apps.get_model('webapp', 'Author')
  query_result = MyModel.objects.all()
  return TemplateResponse(request, 'django_odata/debug.html',
    {
      'components': components
    })
  return HttpResponse(odata_query)


def service_root(request):
  return TemplateResponse(request, 
    'django_odata/debug.html',
    {
      'objects': []
    })
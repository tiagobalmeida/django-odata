# ============================================================
# OData requests handling
#
# (C) Tiago Almeida 2016
#
# Set of function to map the Odata layer to django ORM queries
#
# ============================================================
import pdb
import django.db.models as models
from django.apps import apps
from django.conf import settings as djsettings
from .serialization import OrmQueryResult
from .odata import set_filter
import django_odata.config as config




def model_from_external_name(col_name):
  return col_name # TODO


def get_app_models_names(app_name):
  """
  Given the name of a django app, returns an
  iterator with the names of its Models
  """
  app_config = apps.get_app_config(app_name)
  app_models_iter = app_config.get_models()
  # app_models_iter is an iterable of Model(s)
  model_names_iter = map(lambda m:m.__name__, app_models_iter)
  return model_names_iter


def get_root_response_data(app_name):
  """
  Given a django app name, will fetch the list of its models
  and return them in an object.
  This is usually the root of a service's response and is a 
  list of the EntitySets available on the service

  AppConfig
  https://docs.djangoproject.com/en/1.10/ref/applications/#django.apps.AppConfig
  Model
  https://docs.djangoproject.com/en/1.10/ref/models/instances/#django.db.models.Model
  """
  return { 'EntitySets' : list(config.get_entity_sets_list()) }


class OrmQuery(object):
  def __init__(self, resource_path=None, dj_query=None):
    """
    resource_path is an instance of ResourcePath
    dj_query is a django QuerySet
    """
    self._resource_path = resource_path
    self._dj_query = dj_query
  

  def execute(self, query_options=None):
    """
    Executes the current orm query with the query options.
    Returns an object with the result that knows how to 
      serialize itself.
    """
    if query_options and query_options.has_filter():
      self._dj_query = set_filter(self._dj_query,
        query_options.filter())            
    return OrmQueryResult(self._dj_query) # TODO query_options?


  @staticmethod
  def from_resource_path(resource_path): # type: (object) -> object
    """
    Translates a ResourcePath instance (urlparser.ResourcePath) into
    a django ORM query.

    The ResourcePath needs to address a collection as we assume that.

    A few examples of what might be in the resource_path:

    Path -> components
    -------------------
    /Categories -> ['Categories']
    /Categories(1)/Products -> ['Categories(1)', 'Products']
    
    We use the _meta api on a django Model to get its 
    properties dynamically.
    https://docs.djangoproject.com/en/1.10/ref/models/meta/#module-django.db.models.options
    TODO 
    """
    rp = resource_path # make this shorter
    components = rp.components() # type: List[ResourcePathComponent]
    if len(components) > 0:
      root_model_name = model_from_external_name(
        components[0].collection_name())
    # TODO: deal with multiple apps
    app = djsettings.DJANGO_ODATA['app']
    root_model = apps.get_model(app, root_model_name)        
    dj_query = root_model.objects.all()
    if components[0].has_key():
      # pdb.set_trace()
      dj_query = dj_query.get(pk=components[0].key())
    # For each of the components, check if it 
    # is a collection or instance.
    for comp in components[1:]:
      dj_query = dj_query.__getattribute__(
        comp.collection_name()) # navigate          
      if comp.has_key():
        dj_query = dj_query.get(comp.key()) # get an instance
    newOrmQuery = OrmQuery(resource_path, dj_query)
    return newOrmQuery
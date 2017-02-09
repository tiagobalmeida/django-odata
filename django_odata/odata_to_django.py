# ============================================================
# OData requests handling
#
# (C) Tiago Almeida 2016
#
# Set of function to map the Odata layer to django ORM queries
#
# ============================================================
from .serialization import OrmQueryResult


def model_from_external_name(col_name):
    return col_name # TODO


class OrmQuery(object):
    def __init__(self, resource_path=None, dj_query=None):
        self._resource_path = resource_path
        self._dj_query = dj_query
    

    def execute(self, query_options):
        """
        Executes the current orm query with the query options.
        Returns an object with the result that knows how to 
            serialize itself.
        """
        return OrmQueryResult(self._dj_query.get()) # TODO query_options?


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
            root_model = model_from_external_name(
                collection_name(components[0]))
        dj_query = root_model.objects.all()
        # For each of the components, check if it is a collection or instance.
        for comp in components:
            if comp.has_key():
                dj_query = dj_query.get(comp.key()) # get an instance
            else:
                dj_query = dj_query[comp.collection_name()] # navigate          
        newOrmQuery = OrmQuery(resource_path, dj_query)
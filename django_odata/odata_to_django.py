# ============================================================
# OData requests handling
#
# (C) Tiago Almeida 2016
#
# Set of function to map the Odata layer to django ORM queries
#
# ============================================================

class OrmQuery(object):
    def __init__(self, resource_path=None):
        self._resource_path = resource_path
    

    def execute(self, query_options):
        """
        Executes the current orm query with the query options
        """
        pass


    @staticmethod
    def from_resource_path(resource_path): # type: (object) -> object
        """
        Translates a ResourcePath instance (urlparser.ResourcePath) into
        a django ORM query.

        The ResourcePath needs to address a collection as we assume that.

        A few examples of what might me in the resource_path:

        Path -> components
        -------------------
        /Categories -> ['Categories']
        /Categories(1)/Products -> ['Categories(1)', 'Products']
        
        To get this from the ORM we read right to left following the relantionship
        backwards. We use the _meta api on a django Model to get its 
        properties dynamically.
        https://docs.djangoproject.com/en/1.10/ref/models/meta/#module-django.db.models.options

        """
        rp = resource_path # make this shorter
        components = rp.components() # type: List[ResourcePathComponent]
        orm_query = OrmQuery(rp)
        # For each of the components, check if it is a collection or instance.
        for comp in components:
            if comp.key():
                
        pass

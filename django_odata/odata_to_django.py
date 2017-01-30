# ============================================================
# OData requests handling
#
# (C) Tiago Almeida 2016
#
# Set of function to map the Odata layer to django ORM queries
#
# ============================================================

def odata_resource_path_to_orm(resource_path): # type: (object) -> object
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
    # For each of the components, check if it is a collection or instance.
    pass

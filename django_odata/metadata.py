import pdb
import django.db.models as models
from django.apps import apps
import django_odata.odata_to_django as o2d


def _map_django_type_to_odata(dj_field):
    """
    Odata primitive types:
    http://www.odata.org/documentation/odata-version-2-0/overview/
    Django field types:
    https://docs.djangoproject.com/en/1.10/ref/models/fields/
    """
    type_map = {
        models.AutoField:     'Edm.Int32',
        models.IntegerField:  'Edm.Int32',
        models.CharField:     'Edm.String',
        models.TextField:     'Edm.String',
        models.DateField:     'Edm.Date'
        # TODO: More types
    }
    for dj_field_type, edm_type in type_map.items():
        if isinstance(dj_field, dj_field_type):
            return edm_type
    return None


class ODataEntityField(object):
    """
    ODataEntityField is used to represent both properties of entities
    and associations in the of the edmx model
    """
    def __init__(self, django_field):
        f = django_field
        self.name = f.name
        self.edm_type = _map_django_type_to_odata(django_field)
        self.nullable = django_field.null
        self.is_relation = django_field.is_relation
        if self.is_relation:
            self.related_model = django_field.related_model()
            self.related_model_name = self.related_model.__class__.__name__
            # TODO - This doesn't work for multiple apps!
            # For those cases we'll probably need to go through 
            # self.related_model._meta.app_label: 'e.g. webapp' 
            # and self.related_model._meta.label: 'e.g. webapp.Customer'
            self.many = django_field.one_to_one or django_field.many_to_many


class ODataEntity(object):
    def __init__(self, name, odata_entity_fields):
        # split the fields between relations and non
        self.fields = list(
          filter(lambda f:not f.is_relation, 
            odata_entity_fields))
        self.relationships = list(filter(lambda f:f.is_relation, 
            odata_entity_fields))
        self.name = name
        self.key_name = 'id' #TODO-V2 support other keys


def get_django_model_by_name_for_app(app_name, model_name):
    return apps.get_model(app_name, model_name)


def get_odata_entity_by_model_name(app_name, model_name):
    """
    Returns an ODataEntity instance representing
    the Django model
    https://docs.djangoproject.com/en/1.10/ref/models/meta/
    """
    model = apps.get_model(app_name, model_name)
    fields = model._meta.get_fields()
    fields = list(map(lambda f : ODataEntityField(f), fields))
    # todo...
    return ODataEntity(model_name, fields)


def build_sets(django_models, odata_entities):
    """
    Returns a list of OdataEntitySet representing each set.
    For now we assume the sets have the same name as the entity
    on a future revision we should have a configurable mapping.
    """
    return []


def build_associations(django_models, odata_entities):
    """
    Given a list of django models and corresponding 
    ODataEntity instances, builds a list of associations.
    """
    associations = list()
    model_entity_lst = list(zip(django_models, odata_entities))
    for model_entity in model_entity_lst:
        dj_model = model_entity[0]
        od_entity = model_entity[1]
        # get a list of fields of type relationship
        dj_model_relation_fields = list(filter(lambda f:f.is_relation,
            dj_model._meta.get_fields()))
        for rel_field in dj_model_relation_fields:
            # Relation is a field - Check type of relationship
            one2one = rel_field.one_to_one
            one2many = rel_field.one_to_many
            many2one = rel_field.many_to_one
            many2many = rel_field.many_to_many
            related = rel_field.related_model()
            model = rel_field.model()
            associations.append(Association(model, rel_field, related))
    return associations


def association_name(model, field, related_model):
    """
    Returns the name of the association that links model, through field field
    to related_model. Field is needed because there may be multiple
    associations between the same two models.
    """
    model_name = model._meta.label # e.g. 'webapp.Post'
    relat_name = related_model._meta.label 
    name = model_name + '-' + field.name
    return name


class Association(object):
    def __init__(self, model, field):
        self.name = association_name(model, field, related_model)


class MetadataSchema(object):
    def __init__(self, app_name, django_models):
        self.associations = []
        self.entities = []
        self.entitysets = []
        self.namespace = 'django'
        # TODO use dotmap (pip install dotmap)
        self._django = {
            'app' : app_name,
            'models' : django_models
        }

    @staticmethod
    def from_django_models(app_name, django_model_names):
        metadata = MetadataSchema(app_name, django_model_names)
        def odata_entity_by_model_name(model_name):
            return get_odata_entity_by_model_name(app_name,
                model_name)
        def get_django_model_by_name(model_name):
            return get_django_model_by_name_for_app(app_name, model_name)
        # Convert list of model names to ODataEntity(s)
        odata_entities = list(map(odata_entity_by_model_name,
            django_model_names))
        # Convert list of model names to actual django models
        django_models = list(map(get_django_model_by_name,
            django_model_names))
        associations = build_associations(django_models, odata_entities)
        entitysets = build_sets(django_models, odata_entities)
        metadata.entities = odata_entities
        metadata.associations = associations
        metadata.entitysets = entitysets
        return metadata

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

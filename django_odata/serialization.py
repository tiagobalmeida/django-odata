# ============================================================
# django-odata response serialization
#
# (C) Tiago Almeida 2017
#
# 
#
# ============================================================
import json
import pprint
import django_odata.metadata as metadata
from django.core.serializers.python import Serializer
from django.core.serializers.json import DjangoJSONEncoder


# TODO: _entity_to_json should be called (django model) instance_to_json


class GenericOdataJsonSerializer(object):
	@staticmethod
	def serialize(obj):
		"""
		Inserts obj as the value of property "d" in an 
		outer object and converts this to a json.
		"""
		wrapped = {'d':obj}
		result = json.dumps(wrapped, separators=(',', ':'))
		return result


class OdataJsonSerializer(Serializer):
    def __init__(self, service_root, set_name):
        super().__init__()
        self._set_name = set_name
        self._svc_root = service_root

    def _get_obj_uri(self, obj):
        return self._svc_root + self._set_name +  '(%s)/' % obj.pk

    def _get_obj_type(self, obj):
        return self._set_name

    def get_dump_object(self, obj):
        data = self._current
        if not self.selected_fields or 'id' in self.selected_fields:
          data['id'] = obj.id
        # Inject the odata metadata info
        data['__metadata'] = {
          'uri': self._get_obj_uri(obj),
          'type': self._get_obj_type(obj)
        }
        return data

    def end_object(self, obj):
        if not self.first:
          self.stream.write(', ')
        json.dump(self.get_dump_object(obj), self.stream,
            cls=DjangoJSONEncoder)
        self._current = None

    def start_serialization(self):
        """
        Starts output by wrapping the array in a
        d.results object
        """
        self.stream.write('{"d":{"results":[')

    def end_serialization(self):
        self.stream.write("]}}")

    def getvalue(self):
        return super(Serializer, self).getvalue()



class ODataV4JSONSerializer(object):
    """
    For entitysets we need to return an object with
    @odata.context and value. Value is an array of serialized entries
    For entity we need to return the object with an injected
    property @odata.context
    """
    @staticmethod
    def from_django_query(django_query):
        """
        Initializes an ODataV4JSONSerializer from the result of a django query.
        """
        serializer = ODataV4JSONSerializer()
        serializer.django_query = django_query
        return serializer
    

    def entity_odata_context(self, model_name):
        """
        Needs to return a string with the value of odata.context property of
        an entity.
        e.g.
        http://services.odata.org/V4/Northwind/Northwind.svc/$metadata#Categories/$entity
        """
        return 'TODO'


    def entityset_odata_context(self, model_name):
        """
        Needs to return a string with the value of odata.context property when 
        an entity set is returned.
        e.g.
        "http://services.odata.org/V4/Northwind/Northwind.svc/$metadata#Employees"
        """
        return 'TODO'


    @staticmethod
    def _entity_to_json(metadata, entity):
        """
        Converts an entity into a json string
        """
        result = ODataV4JSONSerializer._django_model_instance_to_dict(metadata, entity)
        return json.dumps(result)


    @staticmethod
    def _django_model_instance_to_dict(metadata, entity):
        """
        Converts a Django model instance into a dict with only the fields specified in the
        metadata and with each value already serialized
        """
        result = {}
        for f in metadata.fields:
            result[f.name] = entity.__getattribute__(f.name) # TODO Serialize based on type
        return result


    def entity_to_json(self):
        """
        Are we returning an entity or an entity set?
        TODO we assume an entity for now.
        """
        app = 'webapp' # TODO!
        obj = self.django_query.get()
        # Get the model name of this object 
        model_name = obj.__class__.__name__ # TODO
        meta = metadata.get_odata_entity_by_model_name(app, model_name)
        # We need to map each field of the meta to the obj.
        # meta is an instande of ODataEntity
        result = ODataV4JSONSerializer._entity_to_json(meta, obj)
        result['@odata.context'] = self.entity_odata_context(model_name)
        return json.dumps(result)


    def entityset_to_json(self):
        entities_serialized = ""
        # Change this logic to support MULTIPLE_APPS
        app = djsettings.DJANGO_ODATA['app']
        # Get the model name of this object 
        model_name = "Tag" # TODO
        meta = metadata.get_odata_entity_by_model_name(app, model_name)
        q = self.django_query
        def _instance_to_dict(django_model_instance):
            return ODataV4JSONSerializer._django_model_instance_to_dict(meta,
                django_model_instance) 
        instances = list(q) # list of django model instances
        entities = list(map(_instance_to_dict, instances))
        result = {
            '@odata.context': self.entityset_odata_context(model_name),
            'value' : entities
        }
        return json.dumps(result)
               


    def to_json(self):
        """
        Are we returning an entity or an entity set?
        TODO we assume an entity for now.
        """
        q = self.django_query
        if len(q) == 0:
            pass #TODO 404
        elif len(q) == 1:
            return self.entity_to_json()
        else:
            return self.entityset_to_json()


class OrmQueryResult(object):
    def __init__(self, django_query):
        self._django_query = django_query
    
    def serialize(self, format=None):
        """
        Serializes the query result according to format
        """
        serializer = ODataV4JSONSerializer.from_django_query(self._django_query) 
        return serializer.to_json()
        #return pprint.pprint(self._django_query)
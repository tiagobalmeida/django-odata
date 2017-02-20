# ============================================================
# django-odata response serialization
#
# (C) Tiago Almeida 2017
#
# 
#
# ============================================================
import pprint
from django.core.serializers.python import Serializer
from django.core.serializers.json import DjangoJSONEncoder

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


class OrmQueryResult(object):
    def __init__(self, django_query):
        self._django_query = django_query
    
    def serialize(self, format):
        """
        Serializes the query result according to format
        """

        return pprint.pprint(self._django_query)
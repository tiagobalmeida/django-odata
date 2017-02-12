# ============================================================
# django-odata response serialization
#
# (C) Tiago Almeida 2017
#
# 
#
# ============================================================
import pprint

class OrmQueryResult(object):
    def __init__(self, django_query):
        self._django_query = django_query
    
    def serialize(self, format):
        """
        Serializes the query result according to format
        """
        return pprint.pprint(self._django_query)
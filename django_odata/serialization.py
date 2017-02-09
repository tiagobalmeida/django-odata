# ============================================================
# django-odata response serialization
#
# (C) Tiago Almeida 2017
#
# 
#
# ============================================================

class OrmQueryResult(object):
    def __init__(self, orm_query):
        self._orm_query = orm_query
        pass
    
    def serialize(self, format):
        """
        Serializes the query result according to format
        """
        pass
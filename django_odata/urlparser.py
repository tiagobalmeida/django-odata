# ============================================================
# OData requests handling
#
# (C) Tiago Almeida 2016
#
#
#
# ============================================================
from .filterparser import Constraint, BinaryOperator
from .filterparser import parse as filter_parser

class ResourcePath(object):
    def __init__(self, string):
        pass

    def components(self): # type: () -> List[ResourcePathComponent]
        """Returns a list of ResourcePathComponents"""
        pass

    def statically_valid(self): # type: () -> bool
        "Check if Resource path is syntactically valid"
        pass

    def addresses_collection(self): # type: () -> bool
        "Checks if the whole resource path is addressing a collection."
        pass

    def addresses_entity_or_property(self): # type: () -> bool
        """
        Checks if the whole resource path is addressing an entity
        or a property of an entity.
        """
        pass


class ResourcePathComponent(object):
    def __init__(self, string):
        pass

    def is_count(self):
        "Is this a $count?"
        pass

    def is_value(self):
        "Is this a $value?"
        pass



class QueryOptions(object):
    def __init__(self, request_get_options): # type: (django.http.QueryDict) -> QueryOptions
        self._parsed_filter = None
        self.request_get_options = request_get_options

    def has_filter(self):
        "Does this have a $filter?"
        return bool(self.request_get_options.get('$filter'))

    def filter(self):
        """
        Returns the $filter query parsed into a tree of filterparser.Constraint
         or filterparser.BinaryOperator
        """
        if not self._parsed_filter:
            self._parsed_filter = filter_parser(self.filter_raw())
        return self._parsed_filter

    def filter_raw(self):
        "Returns actual $filter query or None"
        return self.request_get_options.get('$filter')

    def has_orderby(self):
        "Is this a $order_by?"
        pass

    def orderby(self):
        "Return the $orderby query."
        pass

    def has_skip(self):
        "Is this a $skip?"
        pass

    def skip(self):
        "Return the $skip query."
        pass

    def has_top(self):
        "Is this a $top?"
        pass

    def top(self):
        "Return the $top query."
        pass

    def format(self)
        "Return the format specified in $format or a default"
        pass

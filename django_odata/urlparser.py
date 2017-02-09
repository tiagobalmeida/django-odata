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
        self._resource_path = string
        self._components = False

    def components(self): # type: () -> List[ResourcePathComponent]
        """Returns a list of ResourcePathComponents"""
        if not self._components:
            self._components = [ResourcePath(_) for _ in 
                self._resource_path.split('/')]
        return self._components

    def statically_valid(self): # type: () -> bool
        "Check if Resource path is syntactically valid"
        return True #TODO

    def addresses_collection(self): # type: () -> bool
        "Checks if the whole resource path is addressing a collection."
        pass

    def addresses_entity_or_property(self): # type: () -> bool
        """
        Checks if the whole resource path is addressing an entity
        or a property of an entity.
        """
        pass


def compile_key_regex():
    import re
    return re.compile(r'\w+\((\d+)\)')


class ResourcePathComponent(object):
    key_regex = compile_key_regex()

    def __init__(self, string):
            self._component = string

    def is_count(self):
            "Is this a $count?"
            return self._component == '$count'

    def is_value(self):
            "Is this a $value?"
            return self._component == '$value'

    def has_key(self):
        """
        Is this component a key based addressing?
        These are in the form Collection(key)
        """
        return bool(self.key())

    def key(self):
        "Returns the key that is in the component, or None"
        m = self.key_regex.match(self._component)
        return m.group(0)


class QueryOptions(object):
    def __init__(self, request_get_options, DEFAULT_FORMAT=None): 
        # type: (django.http.QueryDict) -> QueryOptions
        self._parsed_filter = None
        self.request_get_options = request_get_options
        if not DEFAULT_FORMAT:
            self.DEFAULT_FORMAT = 'json'
        else:
            self.DEFAULT_FORMAT = DEFAULT_FORMAT

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
            "Does this have an $order_by?"
            return bool(self.request_get_options.get('$order_by'))
            
    def orderby(self):
        "Return the $orderby query."
        return self.request_get_options.get('$order_by', None)

    def has_skip(self):
        "Does this have a $skip?"
        return bool(self.request_get_options.get('$skip'))

    def skip(self):
        "Return the $skip query."
        return self.request_get_options.get('$skip',None)

    def has_top(self):
        "Does this have a $top?"
        return bool(self.request_get_options.get('$top'))

    def top(self):
        "Return the $top query."
        return self.request_get_options.get('$top',None)

    def format(self):
        "Return the format specified in $format or a default"
        return self.request_get_options.get('$format', 
            self.DEFAULT_FORMAT)

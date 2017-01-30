# ============================================================
# OData requests handling
#
# (C) Tiago Almeida 2016
#
#
#
# ============================================================

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
     def __init__(self, request_get_options):
        pass

    def is_filter(self):
        "Is this a $filter?"
        pass

    def filter(self):
        "Return the $filter query."
        pass

    def is_orderby(self):
        "Is this a $order_by?"
        pass

    def orderby(self):
        "Return the $orderby query."
        pass

    def is_skip(self):
        "Is this a $skip?"
        pass

    def skip(self):
        "Return the $skip query."
        pass

    def is_top(self):
        "Is this a $top?"
        pass

    def top(self):
        "Return the $top query."
        pass

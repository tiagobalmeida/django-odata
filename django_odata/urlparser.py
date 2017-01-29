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

    def addresses_collection(self, string): # type: () -> bool
        "Checks if the whole resource path is addressing a collection."
        pass

    def addresses_entity_or_property(self, string): # type: () -> bool
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

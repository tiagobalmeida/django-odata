import re

def odata_sort_direction_to_django(odata_orderby_criteria_tok):
	"""
	Given an odata orderby criteria, returns a string
	with either '+' , '-' or '' as this is what django
	expects to define the sorting direction.
	
	Example inputs:
	'name asc'
	'name desc'
	'name'
	'Item/id asc'

	The function returns based on the following logic
	<path> 			-> ''
	<path> asc 	-> '+'
	<path> desc -> '-'
	"""
	s = odata_orderby_criteria_tok
	tokens = s.split(' ')
	if len(tokens) == 2:
		if re.search('asc',tokens[1]):
			return tokens[0]
		elif re.search('desc',tokens[1]):
			return '-' + tokens[0]
		else:
			pass # error - TODO
	elif len(tokens) == 1:
		return tokens[0]
	else:
		pass # error - TODO


def is_path_expression(s):
	return True # TODO


def set_order_by(orm_queryset, odata_orderby):
	"""
	Takes a django ORM query and applies an ordering constraint
	if the odata_orderby contains a valid $order_by odata get param.
	Below you can find some examples of what it needs to handle.
	The ordering is done by supplying the proper parameters
	to the .order_by method of the QuerySet

	Order by examples:
	------------------
	http://example.com/OData/OData.svc/Products?$orderby=Rating
		All Product Entries returned in ascending order when sorted
		by the Rating Property.
	
	http://example.com/OData/OData.svc/Products?$orderby=Rating asc
		Same as the example above.
	
	http://example.com/OData/OData.svc/Products?$orderby=...
		...Rating,Category/Name desc
		Same as the URI above except the set of Products is subsequently
		 sorted (in descending order) by the Name property of the
		 related Category Entry.
	"""
	result = orm_queryset
	if odata_orderby:
		django_order_tuple = tuple()
		# Break the odata query by ,
		for criteria in odata_orderby.split(','):
			# criteria can be:
			# - A simple property ( e.g.: name )
			# - A path for subobjects ( e.g.: Author/name )
			# It can also optionally end with 'asc' or 'desc'
			if is_path_expression(criteria):
				pass
				#TODO - convert to path in django's terms
			django_orderby = odata_sort_direction_to_django(criteria)
			django_order_tuple += (django_orderby,) 
		return result.order_by(*django_order_tuple)
	return result
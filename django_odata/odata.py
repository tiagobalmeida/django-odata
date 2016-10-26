import re

# TODO:
# $filter supports ands/ors and parenthesis
# $filter startswith,cp etc
# Break the url get query into the constituents


def odata_sort_direction_to_django(odata_orderby_criteria_tok):
	"""
	Given an odata orderby criteria, returns a string
	with either '-' or '' as this is what django
	expects to define the sorting direction.
	
	Example inputs:
	'name asc'
	'name desc'
	'name'
	'Item/id asc'

	The function returns based on the following logic
	<path> 			-> ''<fieldname>
	<path> asc 	-> ''<fieldname>
	<path> desc -> '-'<fieldname>
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


def odata_sort_property_path_to_django(criteria):
	return criteria.replace('/','__')


def is_path_expression(s):
	return '/' in s


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
				criteria = odata_sort_property_path_to_django(criteria)
				#TODO - convert to path in django's terms
			django_orderby = odata_sort_direction_to_django(criteria)
			django_order_tuple += (django_orderby,) 
		return result.order_by(*django_order_tuple)
	return result


def odata_filter_parse(odata_filter):
	pattern = (
		'(?P<path>[a-zA-Z0-9_/]+)' # property path
		'\s'
		'(?P<op>(eq|ne|gt|lt|ge|le))' # operator
		'\s'
		'(?P<val>-*[a-zA-Z0-9_/]+)' # value
	)
	# pattern = ( '(?P<path>[a-zA-Z0-9_/]+)' )
	regex = re.compile(pattern)
	return regex.match(odata_filter)


def odata_filter_operator_to_django(odata_operator):
	# TODO 'startswidth', contains, iexact,endswidth,
	# notequal
	mapping = {
		'gt':'gt',
		'lt':'lt',
		'ge':'gte',
		'le':'lte',
		'eq':''
	}
	return mapping[odata_operator]


def set_filter(orm_queryset, odata_filter):
	"""
	Takes a django ORM query and applies filtering.
	
	Filter examples:
	------------------
	http://example.com/OData/OData.svc/Products?$filter=Rating eq 2
		All Product Entries that have a Rating == 2

	Available comparison operators: eq, ne, gt, lt, le, ge, ?

	# TODO: This function is messy and lots of scenarios are missing
	"""
	parsed_od_filter = odata_filter_parse(odata_filter)
	if not parsed_od_filter:
		pass # TODO
		return
	dj_filter_params = {}
	dj_operator = odata_filter_operator_to_django(
		parsed_od_filter.group('op')
	)
	dj_param = parsed_od_filter.group('path') 
	if dj_operator:
		dj_param = dj_param + '__' + dj_operator
	dj_filter_params[dj_param] = parsed_od_filter.group('val')	
	return orm_queryset.filter(**dj_filter_params)
 
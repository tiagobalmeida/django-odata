

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
		for criteria in odata_orderby.split(',')
			django_order_tuple += (criteria,) 
		return result.order_by(*django_order_tuple)
	return result
import re
import json
from django.apps import apps
from django.conf import settings as djsettings
from django.core import serializers
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.urls import reverse
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





def get_set(request, set_name):
	"""
	Returns a set of objects.
	For help on what this should comply with, read:
	http://www.odata.org/documentation/odata-version-2-0/uri-conventions/
	
	

	"""
	# System Query Options
	q_order_by = request.GET.get('$order_by', False)
	EntityModel = apps.get_model('webapp', set_name)
	query_result = EntityModel.objects.all()
	if q_order_by:
		query_result = _order_by(query_result, q_order_by)
		
	service_root = reverse('odata_service_root')
	s = OdataJsonSerializer(service_root, set_name)
	#return HttpResponse(s.serialize(response_obj))
	return HttpResponse(s.serialize(EntityModel.objects.all()),
		content_type="application/json")


def handle(request, odata_path):
	return get_set(request, odata_path)
	# take odata_path split by /
	components = odata_path.split('/')
	odata_filter = request.GET.get('$filter', None)
	# is this a query for an entity?
	if re.search('\w+\(.*\)', components[0]):
		entity_query = components[0] 
	else: 
		entityset_query = components[0] 
	settings = djsettings.DJANGO_ODATA
	# app_base_path = djsettings.base_path
	# Try to understand what kind of request is this
	# import pdb; pdb.set_trace()
	#import importlib
	#module_name = ".DjangoGenerator"
	#class_name = "DjangoGenerator"
	#Generator = getattr(importlib.import_module(module_name), class_name)
	#generator = Generator(models)
	from django.apps import apps
	MyModel = apps.get_model('webapp', 'Author')
	query_result = MyModel.objects.all()
	return TemplateResponse(request, 'django_odata/debug.html',
		{
			'components': components
		})
	return HttpResponse(odata_query)


def service_root(request):
	return TemplateResponse(request, 
		'django_odata/debug.html',
		{
			'objects': []
		})
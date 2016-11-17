# ============================================================
# Tests for the django-odata reusable app
#
# (C) Tiago Almeida 2016
#
# 
#
# ============================================================
import unittest
from django.test import TestCase
from tests.models import *
import django_odata.odata as odata


class TopSkipTestCase(TestCase):
	" Tests for $top and $skip "

	def setUp(self):
		for x in range(0,10):
			Number.objects.create(value=x)

	def test(self):
		num_set = Number.objects.all().order_by('value')
		self.assertEquals(len(num_set), 10)
		reduced_set = odata.set_top_skip(num_set, 10, 0) 
		self.assertEquals(len(reduced_set), 10)
		reduced_set = odata.set_top_skip(num_set, 2, 2)
		self.assertEquals(len(reduced_set), 2)
		self.assertEquals(reduced_set[1].value, 3)
		reduced_set = odata.set_top_skip(num_set, 2, 0) 
		self.assertEquals(len(reduced_set), 2)
		reduced_set = odata.set_top_skip(num_set, 2, 4)  
		self.assertEquals(len(reduced_set), 2)
		self.assertEquals(reduced_set[1].value, 5)

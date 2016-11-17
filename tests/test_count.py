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
	" Tests for $count "

	def setUp(self):
		for x in range(0,10):
			Number.objects.create(value=x)

	def test(self):
		num_set = Number.objects.all()
		self.assertEquals(odata.count(num_set), 10)
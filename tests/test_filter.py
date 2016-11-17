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


class FilterParseTestCase(TestCase):
	"""
	Makes sure we can parse all $filter expressions
	"""

	def _parse_validate(self, expression, exp_path, exp_op, exp_val):
		m = odata.odata_filter_parse(expression)
		self.assertEquals( m.group('val'), exp_val )
		self.assertEquals( m.group('op'), exp_op )
		self.assertEquals( m.group('path'), exp_path )

	def test1(self):
		return self._parse_validate('id eq 2', 'id', 'eq', '2')
	def test2(self):
		return self._parse_validate('id ne 2', 'id', 'ne', '2')
	def test3(self):
		return self._parse_validate('id gt 4', 'id', 'gt', '4')
	def test4(self):
		return self._parse_validate('id lt 3', 'id', 'lt', '3')
	def test5(self):
		return self._parse_validate('id le 6', 'id', 'le', '6')
	def test6(self):
		return self._parse_validate('id ge -1', 'id', 'ge', '-1')
	def test7(self):
		return self._parse_validate('id ge -14', 'id', 'ge', '-14')
	def test8(self):
		return self._parse_validate('id ge 23', 'id', 'ge', '23')
	def test9(self):
		return self._parse_validate('id ge field', 'id', 'ge', 'field')
	# TODO: test cases for failure/invalid filters


class FilterTestCase(TestCase):
	" Tests for $filter "

	def setUp(self):
		Tag.objects.create(name="tag2")
		Tag.objects.create(name="tag1")
		Tag.objects.create(name="tag3")
		Tag.objects.create(name="tag3")
		self.tags_count = 4
		for x in range(0,10):
			Number.objects.create(value=x)

	def test(self):
		"""
		"""
		tag_set = odata.set_filter(Tag.objects.all(), 
			'name eq tag3')
		self.assertEquals(len(tag_set), 2)
		self.assertEquals(tag_set[0].name, 'tag3')

	def testNumericEquality(self):
		num_set = odata.set_filter(Number.objects.all(), 
			'value eq 1')
		self.assertEquals(len(num_set), 1)
		self.assertEquals(num_set[0].value, 1)

	def testNumericGreaterThan(self):
		num_set = odata.set_filter(Number.objects.all(), 
			'value gt 2')
		self.assertEquals(len(num_set), 7)

	def testNumericLessThan(self):
		num_set = odata.set_filter(Number.objects.all(), 
			'value lt 2')
		self.assertEquals(len(num_set), 2)

	def testNumericGreaterThanOrEqual(self):
		num_set = odata.set_filter(Number.objects.all(), 
			'value ge 2')
		self.assertEquals(len(num_set), 8)

	def testNumericLessThanOrEqual(self):
		num_set = odata.set_filter(Number.objects.all(), 
			'value le 2')
		self.assertEquals(len(num_set), 3)

	def testNumericLessThanOrEqual(self):
		num_set = odata.set_filter(Number.objects.all(), 
			'value ne 2')
		self.assertEquals(len(num_set), 9)

	def testNumericOr1(self):
		num_set = odata.set_filter(Number.objects.all(), 
			'value ne 2 or value eq 2')
		self.assertEquals(len(num_set), 10)

	def testNumericOr2(self):
		num_set = odata.set_filter(Number.objects.all(), 
			'value lt 3 or value gt 8')
		values = map(lambda x: x.value, num_set)
		self.assertTrue(0 in values)
		self.assertTrue(1 in values)
		self.assertTrue(2 in values)
		self.assertTrue(9 in values)
		self.assertEquals(len(num_set), 4)

	def testNumericAnd(self):
		num_set = odata.set_filter(Number.objects.all(), 
			'value lt 3 and value gt 8')
		self.assertEquals(len(num_set), 0)
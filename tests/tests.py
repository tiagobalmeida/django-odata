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
from .models import Post, Author, Tag
import django_odata.odata as odata


class OrderByTestCase(TestCase):
	def setUp(self):
		Tag.objects.create(name="tag2")
		Tag.objects.create(name="tag1")
		Tag.objects.create(name="tag3")
		Tag.objects.create(name="tag3")
		self.tags_count = 4

	
	def test_orderby_simple(self):
		"""
		Tests $order_by=<property name>
		"""
		set_sorted_name = odata.set_order_by(Tag.objects.all(), 'name')
		self.assertEquals(len(set_sorted_name), self.tags_count)
		self.assertEquals(set_sorted_name[0].name, 'tag1')

	
	def test_orderby_desc(self):
		"""
		Tests $order_by=<property name> desc
		"""
		set_rsorted_name = odata.set_order_by(Tag.objects.all(), 
			'name desc')
		self.assertEquals(len(set_rsorted_name), self.tags_count)
		self.assertEquals(set_rsorted_name[0].name, 'tag3')


	def test_orderby_asc(self):
		"""
		Tests $order_by=<property name> asc
		"""
		set_rsorted_name = odata.set_order_by(Tag.objects.all(), 
			'name asc')
		self.assertEquals(len(set_rsorted_name), self.tags_count)
		self.assertEquals(set_rsorted_name[0].name, 'tag1')
		self.assertEquals(set_rsorted_name[1].name, 'tag2')


	def test_orderby_multiple1(self):
		"""
		Tests $order_by=<property name> asc,<property name> desc
		"""
		set_rsorted_name = odata.set_order_by(Tag.objects.all(), 
			'name asc,id desc')
		self.assertEquals(set_rsorted_name[2].name, 'tag3')
		self.assertEquals(set_rsorted_name[2].id, 4)
		self.assertEquals(set_rsorted_name[3].name, 'tag3')
		self.assertEquals(set_rsorted_name[3].id, 3)	


class OrderBySubobjectTestCase(TestCase):
	def setUp(self):
		Tag.objects.create(name="tag2")
		Tag.objects.create(name="tag1")
		Tag.objects.create(name="tag3")
		Tag.objects.create(name="tag3")
		self.tags_count = 4

	
	def test_orderby_simple(self):
		"""
		Tests $order_by=<property name>/<property name>
		"""
		set_sorted_name = odata.set_order_by(Tag.objects.all(), 'name')
		self.assertEquals(len(set_sorted_name), self.tags_count)
		self.assertEquals(set_sorted_name[0].name, 'tag1')
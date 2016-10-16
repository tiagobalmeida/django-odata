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


class AnimalTestCase(TestCase):
	def setUp(self):
		Tag.objects.create(name="tag1")
		Tag.objects.create(name="tag2)

	def test_orderby_simple(self):
		"""
		"""
		odata.set_order_by(Tag.objects.all(),
			'$order_by=name')
# ============================================================
# Tests for the django-odata reusable app
#
# (C) Tiago Almeida 2016
#
# Tests for module urlparser
#
# ============================================================
import unittest
from django.test import TestCase
from tests.models import *
import django_odata.urlparser as urlparser


class ComponentTestCase(TestCase):
    "Tests for class ResourcePathComponent"

    def setUp(self):
        pass

    def test(self):
        "Test ResourcePathComponent"
        rpc = urlparser.ResourcePathComponent('Collection')
        self.assertFalse(rpc.has_key())
        entity = urlparser.ResourcePathComponent('Collection(1)')
        self.assertTrue(entity.has_key())
        self.assertEquals(entity.key(),'1')


class ResourcePathTestCase(TestCase):
    "Tests for class ResourcePath"

    def setUp(self):
        pass

    def test(self):
        "Test ResourcePathComponent"

        col_path = urlparser.ResourcePath('Collection')
        self.assertEquals(len(col_path.components()), 1)
        self.assertTrue(col_path.statically_valid())
        self.assertTrue(col_path.addresses_collection())
        self.assertFalse(col_path.addresses_entity_or_property())

        ent_path = urlparser.ResourcePath('Collection(2)') 
        self.assertEquals(len(ent_path.components()), 1)
        self.assertTrue(ent_path.statically_valid())
        self.assertFalse(ent_path.addresses_collection())
        self.assertTrue(ent_path.addresses_entity_or_property())

        sub_col_path = urlparser.ResourcePath('Collection(1)/items')
        self.assertEquals(len(sub_col_path.components()), 2)
        self.assertTrue(sub_col_path.statically_valid())
        self.assertTrue(sub_col_path.addresses_collection())
        self.assertFalse(sub_col_path.addresses_entity_or_property())

        sub_ent_path = urlparser.ResourcePath('Collection(1)/items(2)')
        self.assertEquals(len(sub_ent_path.components()), 2)
        self.assertTrue(sub_ent_path.statically_valid())
        self.assertFalse(sub_ent_path.addresses_collection())
        self.assertTrue(sub_ent_path.addresses_entity_or_property())
        # TODO tests for collection_name
# ============================================================
# Tests for the django-odata reusable app
#
# (C) Tiago Almeida 2017
# ============================================================
from django.test import Client, TestCase
from tests.models import Tag
import simplejson as s

class PostTestCase(TestCase):
    """ 
    Tests for POST requests 
    """

    def test(self):
        """
        Test creation of a Tag object
        """
        c = Client()
        json_data = s.dumps({'name': 'tag1'})
        response = c.post('/Tag', 
            json_data,
            content_type='application/json')
        self.assertEquals(response.status_code, 201)
        # parse the response
        body = s.loads(response.content)
        self.assertEquals(body['name'],'tag1')
        self.assertTrue('id' in body)


class PostDeleteTestCase(TestCase):
    """ 
    Tests for both creation and deletions  
    """

    def test(self):
        """
        Create a Tag object via the serivice and then delete it.
        """
        c = Client()
        json_data = s.dumps({'name': 'tag1'})
        response = c.post('/Tag', 
            json_data,
            content_type='application/json')
        self.assertEquals(response.status_code, 201)
        # Confirm there is one Tag in the DB
        from tests.models import Tag
        self.assertEquals(len(Tag.objects.all()),1)
        # Issue a delete request for it
        response = c.delete('/Tag(1)')
        self.assertEquals(response.status_code, 204)
        self.assertEquals(len(Tag.objects.all()),0)


class UpdateTestCase(TestCase):
    """ 
    Tests for updating instances  
    """

    def testUpdateNameOfTag(self):
        # Create a tag
        NEW_VALUE = 'changed'
        t = Tag(name='tochange')
        t.save()
        # Confirm there is one Tag in the DB
        self.assertEquals(len(Tag.objects.all()),1)
        # Update the tag via the service
        c = Client()
        json_data = s.dumps({'name': NEW_VALUE})
        response = c.patch('/Tag(1)', 
            json_data,
            content_type='application/json')
        self.assertEquals(response.status_code, 204)
        # Confirm there is still one Tag in the DB
        self.assertEquals(len(Tag.objects.all()),1)
        # Confirm the name was changed
        k = Tag.objects.get(pk=1)
        self.assertEquals(k.name, NEW_VALUE)

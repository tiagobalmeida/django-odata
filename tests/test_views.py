# ============================================================
# Tests for the django-odata reusable app
#
# (C) Tiago Almeida 2017
# ============================================================
from django.test import Client, TestCase
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

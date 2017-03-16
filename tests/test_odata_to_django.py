# ============================================================
# Tests for the django-odata reusable app
#
# (C) Tiago Almeida 2016
#
# Tests for module odata_to_django
#
# ============================================================
import datetime
import unittest
from django.test import TestCase
from tests.models import *
import django_odata.odata_to_django as odata2django
import django_odata.urlparser as urlparser

class OrmQueryTestCase(TestCase):
  "Tests for class OrmQuery"

  def setUp(self):
    # Create a few objects
    # Author Newton with 2 posts
    # Author Hooke with 1 post
    a = Author.objects.create(name="Newton",
        dateOfBirth=datetime.datetime.now())
    b = Author.objects.create(name="Hooke",
        dateOfBirth=datetime.datetime.now())
    self.author_key = a.id
    t1 = Tag.objects.create(name="tag1")
    t2 = Tag.objects.create(name="tag2")
    Post.objects.create(title='t1', body='b1',
        author=a, publishDate=datetime.datetime.now())
    Post.objects.create(title='t2', body='b2',
        author=a, publishDate=datetime.datetime.now())
    Post.objects.create(title='t3', body='b3',
        author=b, publishDate=datetime.datetime.now())

  def testQueryAuthor(self):
    "Test OrmQuery"
    # Query Author
    rp = urlparser.ResourcePath('Author')
    orm_query = odata2django.OrmQuery.from_resource_path(rp)
    orm_query_result = orm_query.execute()
    result = list(orm_query_result._django_query)
    self.assertEquals(len(result), 2)
    self.assertTrue(type(result[0])==Author)
  
  def testQueryPosts(self):
    # Query Post(s)
    rp = urlparser.ResourcePath('Post')
    orm_query = odata2django.OrmQuery.from_resource_path(rp)
    orm_query_result = orm_query.execute()
    result = list(orm_query_result._django_query)
    self.assertEquals(len(result), 3)
    self.assertTrue(type(result[0])==Post)
  
  def testQueryAuthor1(self):
    # Query Author(1)
    rp = urlparser.ResourcePath('Author(%s)' % self.author_key)
    orm_query = odata2django.OrmQuery.from_resource_path(rp)
    orm_query_result = orm_query.execute()
    result = orm_query_result._django_query
    self.assertEquals(type(result),Author)
    self.assertEquals(result.name, 'Newton')
  
  def testQueryAuthor1Posts(self):
    # Query Author(1)/posts
    rp = urlparser.ResourcePath('Author(%s)/posts' % self.author_key)
    orm_query = odata2django.OrmQuery.from_resource_path(rp)
    orm_query_result = orm_query.execute()
    result = list(orm_query_result._django_query.all())
    self.assertEquals(len(result), 2)
    self.assertTrue(type(result[0])==Post)

  def _buildQueryOptions(self, query_string):
    """
    We need to return a QueryOptions object.
    Its constructor expects a dict whose keys are the 
    url query string parameters. Django does this
    automatically in a real world but in here we 
    havo to parse it manually.
    """
    full_url = 'http://example.com/?' + query_string 
    from urllib import parse as urlparse 
    parsed_query = urlparse.parse_qs(
      urlparse.urlsplit(full_url).query)
    parsed_query['$filter'] = parsed_query['$filter'][0]
    return urlparser.QueryOptions(parsed_query)


  def testTagsWithNameFilter(self):
    # Set the URL
    rp = urlparser.ResourcePath('Tag')
    # Set the query options
    qo = self._buildQueryOptions("$filter=name eq 'tag1'")
    orm_query = odata2django.OrmQuery.from_resource_path(rp)
    orm_query_result = orm_query.execute(qo)
    result = list(orm_query_result._django_query.all())
    # Should only bring one object.
    self.assertEquals(len(result), 1)
    self.assertTrue(type(result[0])==Tag)

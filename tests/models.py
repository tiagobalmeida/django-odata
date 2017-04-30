# ============================================================
# Models needed to test the django-odata reusable app
# 
# (C) Tiago Almeida 2016
#
# 
#
# ============================================================
from django.db import models


class TestModel(models.Model):
	"""
	Base for test models that sets app_label.
	"""
	class Meta:
		app_label = 'tests'
		abstract = True


class Post(TestModel):
	title = models.CharField(max_length=1024)
	author = models.ForeignKey('Author', blank=True, 
		related_name='posts')
	body = models.TextField()
	publishDate = models.DateField()
	tags = models.ManyToManyField('Tag', blank=False)


class Tag(TestModel):
	name = models.CharField(max_length=1024)


class Author(TestModel):
	name = models.CharField(max_length=1024)
	dateOfBirth = models.DateField()


class Main(TestModel):
	name = models.CharField(max_length=1024)
	rel = models.ForeignKey('Sub', blank=True)


class Sub(TestModel):
	name = models.CharField(max_length=1024)


class Number(TestModel):
	value = models.IntegerField()


# --------------------
# Northwind model
class CustomerDemographic(TestModel):
	CustomerDesc = models.CharField(max_length=40)
	Customers = models.ManyToManyField('Customer', 
		related_name='CustomerDemographics')

class Customer(TestModel):
	CompanyName = models.CharField(max_length=40)
	ContactName = models.CharField(max_length=30)
	# TODO.. more fields
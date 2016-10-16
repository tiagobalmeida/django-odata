# ============================================================
# Models needed to test the django-odata reusable app
#
# (C) Tiago Almeida 2016
#
# 
#
# ============================================================
from django.db import models

class Post(models.Model):
	title = models.CharField(max_length=1024)
	author = models.ForeignKey('Author', blank=True)
	body = models.TextField()
	publishDate = models.DateField()
	tags = models.ManyToManyField('Tag', blank=False)

class Tag(models.Model):
	name = models.CharField(max_length=1024)

class Author(models.Model):
	name = models.CharField(max_length=1024)
	dateOfBirth = models.DateField()
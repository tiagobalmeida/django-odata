from django.db import models


class Person(models.Model):
    name = models.CharField(max_length=1024)


class Supplier(models.Model):
    SupplierID = models.IntegerField(unique=True)
    CompanyName = models.CharField(max_length=40)
    ContactName = models.CharField(max_length=30)
    ContactTitle = models.CharField(max_length=30)
    Address = models.CharField(max_length=60)
    City = models.CharField(max_length=15)
    Region = models.CharField(max_length=15)
    PostalCode = models.CharField(max_length=10)
    Country = models.CharField(max_length=15)

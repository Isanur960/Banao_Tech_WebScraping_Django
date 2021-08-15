from django.db import models

# Create your models here.

class interesting_url(models.Model):
    id = models.BigAutoField(primary_key= True)
    url = models.URLField(max_length=200)

class non_interesting_url(models.Model):
    id = models.BigAutoField(primary_key= True)
    url = models.URLField(max_length=200)

class Categories(models.Model):
    id = models.BigAutoField(primary_key= True)
    name = models.CharField(max_length=50)
    syn = models.CharField(max_length=100, null= True, blank= True)

class JobDB(models.Model):
    id = models.BigAutoField(primary_key=True)
    url = models.URLField(max_length=200)
    title = models.TextField(max_length=200)
    description = models.TextField(max_length=2500)
    salary = models.TextField(max_length=50)
    datePosted = models.TextField(max_length=50)
    validThrough = models.TextField(max_length=50)
    hiringOrganization = models.TextField(max_length=50)
    category = models.TextField(max_length=50)
    place = models.TextField(max_length=50)

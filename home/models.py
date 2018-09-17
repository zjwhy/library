# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Library(models.Model):
    name = models.CharField(max_length=20)
    curator = models.CharField(max_length=20)
    tel = models.IntegerField(max_length=30)
    address = models.CharField(max_length=30)
    email = models.CharField(max_length=20)
    url = models.CharField(max_length=20)
    create_date = models.CharField(max_length=20)
    introduce = models.TextField()

    class Meta:
        db_table = 't_library'

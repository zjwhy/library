# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Manager(models.Model):
    id = models.AutoField(primary_key=True,unique=True)
    name = models.CharField(max_length=30,unique=True)
    pwd = models.CharField(max_length=30,unique=True)

    def __unicode__(self):
        return u'Manage:%s,%s'%(self.name,self.pwd)

    class Meta:
        db_table='t_manager'





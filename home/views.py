# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
#系统设置
def modify_view(request):
    return render(request,'modify.html')


def index_view(request):
    return render(request,'index.html')

#管理员设置
def manager_view(request):
    return render(request,'manager.html')

#参数设置
def parameter_view(request):
    return render(request,'parameter_c.html')

#书架设置
def bookcase_view(request):
    return render(request,'')
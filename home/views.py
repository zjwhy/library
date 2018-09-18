# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.shortcuts import render
from .models import *


# Create your views here.

# 系统设置
def modify_view(request):
    if request.method == 'GET':
        con = Library.objects.first()
        return render(request, 'modify.html', {'con': con})
    else:
        # print '1111'
        name = request.POST.get("libraryname", "")
        curator = request.POST.get('curator', '')
        tel = request.POST.get("tel", "")
        address = request.POST.get("address", "")
        email = request.POST.get("email", "")
        url = request.POST.get("url", "")
        createDate = request.POST.get("createDate", "")
        introduce = request.POST.get("introduce", "")
        if Library.objects.first():
            Library.objects.update(name=name, curator=curator, tel=tel, address=address, email=email, url=url,
                                   createdate=createDate, introduce=introduce)
        else:
            Library.objects.create(name=name, curator=curator, tel=tel, address=address, email=email, url=url,
                                   createdate=createDate,introduce=introduce)
        # print '执行到这'
        con = Library.objects.first()
        return render(request, 'modify.html',{"con":con})


def index_view(request):
    return render(request, 'index.html')


# 管理员设置
def manager_view(request):
    managers = Manager.objects.all()
    return render(request, 'manager.html',{"managers":managers})


# 参数设置
def parameter_view(request):
    return render(request, 'parameter_c.html')


# 书架设置
def bookcase_view(request):
    bookcase = Bookcase.objects.all()
    return render(request, 'bookcase.html',{'bookcase':bookcase})

# #添加管理员系统
# def add_managerview(request):
#     return None

#添加书架
def add_case_view(request):
    if request.method == 'GET':
        return render(request, 'add_case.html')
    else:
        add_name = request.POST.get('add_name','')
        search_name = Bookcase.objects.filter(name=add_name)
        if search_name:
            return render(request,'no_add.html')
        else:
            Bookcase.objects.create(name=add_name)
            return render(request,'add.html')

#修改书架
def up_case_view(request):
    if request.method == 'GET':
        id = request.GET.get('id','')
        print id
        up_case = Bookcase.objects.get(id=id)
        # for i in up_case:
        print up_case.name
        return render(request, 'up_case.html',{'up_case':up_case})
    else:
        # print '111111'
        nid = request.GET.get('id','')
        # print nid
        nid = int(nid)
        up_name = request.POST.get('up_name','')
        Bookcase.objects.filter(id=nid).update(name=up_name)
        return HttpResponse('123')

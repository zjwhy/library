# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import *


# Create your views here.
# 系统设置
def modify_view(request):
    if request.method == 'GET':
        con = Library.objects.first()
        return render(request, 'modify.html', {'con': con})
    else:
        print '1111'
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
                                   create_date=createDate, introduce=introduce)
        else:
            Library.objects.create(name=name, curator=curator, tel=tel, address=address, email=email, url=url,
                                   create_date=createDate,introduce=introduce)
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

    return render(request, 'bookcase.html')


def home_view(request):
    return HttpResponse('123')

def login_view(request):
    if request.method=='GET':
        return render(request, 'login.html')
    else:
        #接受数据
        name = request.POST.get('name','')
        pwd = request.POST.get('password','')
        # print name,password

        #判断是否登录成功

        count= Manager.objects.filter(name=name,pwd=pwd).count()

        if count == 1:
            return redirect('/home/')

        else:
            return redirect('/login/')



def register_view(request):
    if request.method=='GET':
        return render(request,'register.html')
    else:
        #接受数据
        name = request.POST.get('name','')
        pwd = request.POST.get('password','')

        # print name,password

        try:
            manage = Manager.objects.get(name=name,pwd=pwd)
        except Manager.DoesNotExist:
            manage = Manager.objects.create(name=name,pwd=pwd)

        # manageInfo = Manager.objects.create(manage=manage)

        return HttpResponse('注册成功')



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



# 读者类型
def reader_type(request):
    reader_types = ReaderType.objects.all()
    # print reader_types
    return render(request,'reader_type.html',{"reader_types": reader_types})
    # if request.method == "GET":
    # # number 可借数  name读者类型
    #     return render(request, "reader_type.html")
    # else:
    #     number = request.POST.get("number","")
    #     name = request.POST.get('name', '')
    #
    #     if number and name:
    #         return render(request,"reader_type.html")
    #     else:
    #         ReaderType = ReaderType(number=number,name=name).save()
    #         return render(request,"reader_type.html",{"ReaderType": ReaderType})


def reader_view(request):
    # name 读者姓名，barcode 条形码，created 创建日期
    if request.method == "GET":
        barcode = request.GET.get("barcode","")
        name = request.GET.get("name","")
        return render(request,"reader.html",{"barcode": barcode,"name": name})


        readers = []
        try:
            reader = Reader.objects.get(barcode=barcode,name=name)
        except Reader.DoesNotExist:
            reader = Reader.objects.create(barcode=barcode,name=name)
            readers.append(reader)
        return render(request,"reader.html")
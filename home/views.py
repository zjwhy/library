# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.paginator import Paginator
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

    return render(request, 'bookcase.html')

# 分页
def page(num=1):
    size = 1
    paginator = Paginator(BookInfo.objects.all().order_by('-count'),size)
    if num <= 0:
        num = 1
    if num > paginator.num_pages:
        num = paginator.num_pages
    current_page = num
    total_page = paginator.num_pages
    page_list = [current_page,total_page]
    return paginator.page(num), page_list

# 主页
def home_view(request,num=1):
    # num = request.GET.get('num','1')
    num = int(num)
    global username
    # print username
    books,page_list = page(num)
    return render(request,'index.html',{'books':books,'page_list':page_list})


username = 'admin'
# 登录
def login_view(request):
    global username
    if request.method=='GET':
        username = 'admin'
        return render(request, 'login.html')
    else:
        #接受数据
        name = request.POST.get('name','')
        pwd = request.POST.get('password','')
        # print name,pwd

        #判断是否登录成功

        count= Manager.objects.filter(name=name,pwd=pwd).count()

        if count == 1:

            username = name
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

        return redirect('/login/')



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


#添加更改口令功能
def pwd_modify_view(request):
    if request.method == 'GET':
        return render(request,'pwd_modify.html')

    else:
        name = request.POST.get('name','')
        pwd = request.POST.get('oldpwd','')
        newpwd = request.POST.get('pwd','')
        newpwd1 = request.POST.get('pwd1','')


        if newpwd==newpwd1:
            manager = Manager.objects.filter(name=name, pwd=pwd)
            print manager
            if newpwd:
                manager.update (pwd=newpwd)  #如果用户名、原密码匹配则更新密码
                return redirect('/login/')
        else:
            return HttpResponse('请检查原密码是否输入正确!')
        # elif len(name) == 0:
        #     return  HttpResponse('请检查用户名是否正确!')





#图书借阅
def borrow_view(request):

    return render(request,'borrow.html')


def renew_view(request):
    return render(request,'renew.html')


def book_back_view(request):
    return render(request,'book_back.html')
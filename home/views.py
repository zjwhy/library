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
    books,page_list = page(num)
    return render(request,'index.html',{'books':books,'page_list':page_list})

def login_view(request):
    if request.method=='GET':
        return render(request, 'login.html')
    else:
        #接受数据
        name = request.POST.get('name','')
        pwd = request.POST.get('password','')
        print name,pwd

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

# 图书字段查询函数封装
def select(select,search):
    if select == 'barcode':
        book_infos = BookInfo.objects.filter(barcode__contains=search)
    elif select == 'bookname':
        book_infos = BookInfo.objects.filter(bookname__contains=search)
    elif select == 'author':
        book_infos = BookInfo.objects.filter(author__contains=search)
    elif select == 'booktype':
        id = BookType.objects.get(typename__contains=search).id
        book_infos = BookInfo.objects.filter(booktype=id)
    elif select == 'bookcase':
        id = Bookcase.objects.get(name__contains=search).id
        book_infos = BookInfo.objects.filter(bookcase=id)
    elif select == 'bookpub':
        id = Publishing.objects.get(name__contains=search).id
        book_infos = BookInfo.objects.filter(bookpub=id)
    return book_infos
# 图书档案查询
def book_info_search_view(request):
    if request.method == 'GET':
        books = BookInfo.objects.order_by('-count').first()
        return render(request,'book_info_search.html',{'books':books})
    else:
        select = request.POST.get('select','')
        search = request.POST.get('search','')
        # print select,search
        book_infos = select(select,search)
        return  render(request,'book_info_search.html',{'book_infos':book_infos})


def borrow_search_view(request):
    if request.method == 'GET':
        return render(request,'borrow_search.html')
    else:
        select = request.POST.get('select', '')
        search = request.POST.get('search', '')
        # book_infos = select(select,search)
        borrows = Borrow.objects.all()
        print borrows
        return render(request,'borrow_search.html',{'borrows':borrows})


def borrow_remind_view(request):
    return render(request,'borrow_remind.html')
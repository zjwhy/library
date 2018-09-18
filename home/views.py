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
    bookcase = Bookcase.objects.all()
    return render(request, 'bookcase.html',{'bookcase':bookcase})

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
        seach_name = Bookcase.objects.filter(name=up_name)
        if seach_name:
            return render(request,'up_ok.html',{'no_ok':'修改的名字已经存在'})
        else:
            Bookcase.objects.filter(id=nid).update(name=up_name)
            return render(request,'up_ok.html',{'no_ok':'修改成功'})

#删除书架
def del_case_view(request):
        id = request.GET.get('id','')
        print id
        id=int(id)
        all_book = Bookcase.objects.get(id=id).bookinfo_set.all()
        if all_book:
            return render(request, 'del_case.html',{"no_ok":'请先清空书架上的书籍在删除'} )
        else:
            Bookcase.objects.filter(id=id).delete()
            return render(request, 'del_case.html', {'no_ok': '删除成功'})


        # print del_case.name
        # del_case[0].delete()
        # for i in up_case:
        # print up_case.name


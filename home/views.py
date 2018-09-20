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
                                   createdate=createDate, introduce=introduce)
        # print '执行到这'
        con = Library.objects.first()
        return render(request, 'modify.html', {"con": con})


def index_view(request):
    return render(request, 'index.html')


# 管理员设置
def manager_view(request):
    managers = Manager.objects.all()
    return render(request, 'manager.html', {"managers": managers})


# 参数设置
def parameter_view(request):
    return render(request, 'parameter_c.html')


# 书架设置
def bookcase_view(request):
    return render(request, 'bookcase.html')


# 分页
def page(num=1):
    size = 1
    paginator = Paginator(BookInfo.objects.all().order_by('-count'), size)
    if num <= 0:
        num = 1
    if num > paginator.num_pages:
        num = paginator.num_pages
    current_page = num
    total_page = paginator.num_pages
    page_list = [current_page, total_page]
    return paginator.page(num), page_list


# 主页
def home_view(request, num=1):
    # num = request.GET.get('num','1')
    num = int(num)
    books, page_list = page(num)
    return render(request, 'index.html', {'books': books, 'page_list': page_list})


def login_view(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        # 接受数据
        name = request.POST.get('name', '')
        pwd = request.POST.get('password', '')
        print name, pwd

        # 判断是否登录成功

        count = Manager.objects.filter(name=name, pwd=pwd).count()

        if count == 1:
            return redirect('/home/')

        else:
            return redirect('/login/')


def register_view(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    else:
        # 接受数据
        name = request.POST.get('name', '')
        pwd = request.POST.get('password', '')

        # print name,password

        try:
            manage = Manager.objects.get(name=name, pwd=pwd)
        except Manager.DoesNotExist:
            manage = Manager.objects.create(name=name, pwd=pwd)

        # manageInfo = Manager.objects.create(manage=manage)

        return redirect('/login/')


# #添加管理员系统
# def add_managerview(request):
#     return None

# 添加书架
def add_case_view(request):
    if request.method == 'GET':
        return render(request, 'add_case.html')
    else:
        add_name = request.POST.get('add_name', '')
        search_name = Bookcase.objects.filter(name=add_name)
        if search_name:
            return render(request, 'no_add.html')
        else:
            Bookcase.objects.create(name=add_name)
            return render(request, 'add.html')


# 读者类型,删除读者类型,修改
def reader_type(request, id=0):
    if request.method == "GET":
        if not id:
            # print id, type(id)
            reader_types = ReaderType.objects.all()
            return render(request, 'reader_type.html', {"reader_types": reader_types})
        else:
            del_re_ty_id = ReaderType.objects.filter(id=id)
            del_re_ty_id.delete()
            reader_types = ReaderType.objects.all()
            return render(request, 'reader_type.html', {"reader_types": reader_types})
    else:
        new_name = request.POST.get("name", "")
        new_number = request.POST.get('number', '')
        # print new_name, new_number,id
        readertype_id = ReaderType.objects.filter(id=id)
        try:
            if new_name and new_number:
                readertype_id.update(name=new_name, number=new_number)
        except:
            pass
        reader_types = ReaderType.objects.all()
        return render(request, 'reader_type.html', {"reader_types": reader_types})


# 添加读者类型
def add_reader_type(request):
    if request.method == 'GET':
        return render(request, 'add_reader_type.html')
    else:
        add_name = request.POST.get('add_name', '')
        add_number = request.POST.get('add_number', '')
        search_name = ReaderType.objects.filter(name=add_name)
        try:
            if not add_name:
                return redirect("/add_reader_type/")
            if not add_number:
                return redirect("/add_reader_type/")
        except:
            return redirect("/add_reader_type/")

        if search_name:
            return render(request, 'no_add_reader_type.html')

        ReaderType.objects.create(name=add_name, number=add_number)
        return redirect('/reader_type/')


# 修改读者类型
def modify_reader_type(request, id=0):
    if request.method == 'GET':
        con = ReaderType.objects.get(id=id)
        return render(request, 'modify_reader_type.html', {'con': con})


# 读者信息,修改，删除
def reader_view(request, id=0):
    # name 读者姓名，barcode 条形码，created 创建日期

    # 在python2的字符编码问题时常会遇到类似
    # “UnicodeEncodeError: 'ascii'codec can't encode characters
    # in position 0-5: ordinal not in range(128)”的编码错误。
    # 以下三行解决此问题
    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8')

    if request.method == 'GET':
        if not id:
            readers = Reader.objects.all()
            return render(request, "reader.html", {"readers": readers})
        else:
            reader_id = Reader.objects.filter(id=id)
            reader_id.delete()
            readers = Reader.objects.all()
            return render(request, "reader.html", {"readers": readers})
    else:
        new_name = request.POST.get("name", "")
        new_sex = request.POST.get("sex", "")
        new_barcode = request.POST.get("barcode", "")
        new_tel = request.POST.get("tel", "")
        new_email = request.POST.get("email", "")
        new_created = request.POST.get("created", "")
        new_readertype = request.POST.get("readertype", "")

        reader_id = Reader.objects.filter(id=id)
        try:
            reader_id.update(name=new_name, sex_id=new_sex, barcode=new_barcode, tel=new_tel, email=new_email,
                             created=new_created, readertype_id=new_readertype)
        except:
            pass
        return redirect("/reader/")


# 添加读者信息
def add_reader(request):
    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8')

    if request.method == "GET":
        return render(request, "add_readerinfo.html")
    else:
        add_name = request.POST.get("add_name", "")
        add_sex = request.POST.get("add_sex", "")
        add_barcode = request.POST.get("add_barcode", "")
        add_tel = request.POST.get("add_tel", "")
        add_email = request.POST.get("add_email", "")
        add_created = request.POST.get("add_created", "")
        add_readertype = request.POST.get("add_readertype", "")

        try:
            search_barcode = Reader.objects.filter(barcode=add_barcode)
        except:
            search_barcode = []

        if not search_barcode:
            try:
                Reader.objects.create(name=add_name, sex_id=add_sex, barcode=add_barcode, tel=add_tel, email=add_email,
                                  created=add_created, readertype_id=add_readertype)
            except:
                return render(request," not_bug.html")
        return redirect("/reader/")


# 修改读者
def modify_reader(request, id=0):
    if request.method == 'GET':
        Re_ids = Reader.objects.get(id=id)
        return render(request, 'modify_reader.html', {'Re_ids': Re_ids})

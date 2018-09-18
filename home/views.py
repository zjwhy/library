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
    if request.method == 'GET':
        con = Parameter.objects.first()
        # print con
        return render(request, 'parameter_c.html',{'con':con})
    else:
        cost = request.POST.get('cost','')
        # print cost
        validity = request.POST.get('validity','')
        # print validity
        new_con = Parameter.objects.first()
        if new_con:
            Parameter.objects.filter(id=1).update(cost=cost,validity=validity)
            con = Parameter.objects.first()
            return render(request, 'parameter_c.html',{'con':con})
        else:
            Parameter.objects.create(cost=cost,validity=validity)
            con = Parameter.objects.first()
            return render(request, 'parameter_c.html',{'con':con})

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
            return redirect('/bookcase/')

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
#修改书架
def up_case_view(request):
    if request.method == 'GET':
        id = request.GET.get('id','')
        # print id
        up_case = Bookcase.objects.get(id=id)
        # for i in up_case:
        # print up_case.name
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
            return redirect('/bookcase/')



#图书类型管理
def booktype_view(request):
    con_type = BookType.objects.all()
    return render(request,'book_type.html',{'con_type':con_type})

#图书类型添加
def add_booktype_view(request):
    if request.method == 'GET':
        return render(request,'add_booktype.html')
    else:
        name = request.POST.get('add_name','')
        day = request.POST.get('add_day','')
        search_name = BookType.objects.filter(typename=name)
        if search_name:
            return HttpResponse('<script>alert("添加的类型已经存在");location.href="/booktype/"</script>')
        else:
            BookType.objects.create(typename=name,days=day)
            return redirect('/booktype/')

#修改类型
def up_type_view(request):
    if request.method=='GET':
        id = request.GET.get('id', '')
        return render(request,'up_type.html',{'id':id})
    else:
        id = request.GET.get('id','')
        id = int(id)
        up_name = request.POST.get('up_name','')
        up_days = request.POST.get('up_days','')
        search_name = BookType.objects.filter(typename=up_name)
        if search_name:
            return HttpResponse('<script>alert("输入的类型已经存在");location.href="/booktype/"</script>')
        else:
            BookType.objects.filter(id=id).update(typename=up_name,days=up_days)
            return HttpResponse('<script>alert("修改成功");location.href="/booktype/"</script>')

#删除图书类型
def del_type_view(request):
        id = request.GET.get('id', '')
        id = int(id)
        search_name = BookType.objects.get(id=id).bookinfo_set.all()
        if search_name:
            return HttpResponse('<script>alert("请清空当前类型的书籍在做删除");location.href="/booktype/"</script>')
        else:
            BookType.objects.filter(id=id).delete()
            return HttpResponse('<script>alert("删除成功");location.href="/booktype/"</script>')

#图书档案管理
def book_view(request):
    all_book = BookInfo.objects.all()
    return render(request,'book.html',{'all_book':all_book})

#图书添加功能
def add_book_view(request):
    if request.method == 'GET':
        all_type = BookType.objects.all()
        all_case = Bookcase.objects.all()
        all_pub = Publishing.objects.all()
        return render(request, 'add_book.html', {'all_type': all_type, 'all_case': all_case, 'all_pub': all_pub})
    else:
        barcode = request.POST.get('barcode','')
        bookname = request.POST.get('bookname','')
        author = request.POST.get('author','')
        price = request.POST.get('price','')
        number = request.POST.get('number','')
        number=int(number)
        type = request.POST.get('type','')
        case = request.POST.get('case','')
        pub = request.POST.get('pub','')
        search_name = BookInfo.objects.filter(bookname=bookname)
        if search_name:
            return HttpResponse('<script>alert("添加的图书已经存在");location.href="/add_book/"</script>')
        else:
            booktype=BookType.objects.get(typename=type)
            bookcase=Bookcase.objects.get(name=case)
            bookpub=Publishing.objects.get(name=pub)
            # for i in lista:
            #     print i
            # BookInfo.objects.create(bookpub=bookpub, booktype=booktype, bookcase=bookcase,**lista)
            BookInfo.objects.create(barcode=barcode, bookname=bookname, author=author, price=price, number=number,
                                    bookpub=bookpub, booktype=booktype, bookcase=bookcase)
            return HttpResponse('<script>alert("添加成功");location.href="/add_book/"</script>')

#修改图书
def up_book_view(request):
    if request.method=='GET':
        id = request.GET.get('id','')
        all_type = BookType.objects.all()
        all_case = Bookcase.objects.all()
        all_pub = Publishing.objects.all()
        return render(request,'up_book.html',{'id':id,'all_type': all_type, 'all_case': all_case, 'all_pub': all_pub})
    else:
        id = request.GET.get('id','')
        barcode = request.POST.get('barcode', '')
        bookname = request.POST.get('bookname', '')
        author = request.POST.get('author', '')
        price = request.POST.get('price', '')
        type = request.POST.get('type', '')
        case = request.POST.get('case', '')
        pub = request.POST.get('pub', '')
        number = request.POST.get('number', '')
        number = int(number)
        search_name = BookInfo.objects.filter(bookname=bookname)
        if search_name:
            return HttpResponse('<script>alert("修改的图书已经存在");location.href="/book/"</script>')
        else:
            booktype = BookType.objects.get(typename=type)
            bookcase = Bookcase.objects.get(name=case)
            bookpub = Publishing.objects.get(name=pub)
            BookInfo.objects.filter(id=id).update(barcode=barcode, bookname=bookname, author=author, price=price,
                                                  number=number,bookpub=bookpub,booktype=booktype, bookcase=bookcase)
            return HttpResponse('<script>alert("修改成功");location.href="/book/"</script>')

#删除图书
# 图书借阅查询
def borrow_search_view(request):
    if request.method == 'GET':
        return render(request, 'borrow_search.html')
    else:
        select = request.POST.get('select', '')
        search = request.POST.get('search', '')
        # book_infos = select(select,search)
        borrows = Borrow.objects.all()
        print borrows
        return render(request, 'borrow_search.html', {'borrows': borrows})
# 借阅到期提醒
def borrow_remind_view(request):
    return render(request,'borrow_remind.html')


#图书借阅
def borrow_view(request):

    return render(request,'borrow.html')

#图书续借
def renew_view(request):
    return render(request,'renew.html')

#图书归还
def book_back_view(request):
    return render(request,'book_back.html')


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

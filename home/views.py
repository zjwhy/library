# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import date, datetime, timedelta
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import *


# Create your views here.

# 设置用户session
def __set_session(request,name):
    request.session["username"] = name
    request.session["is_login"] = True
    if request.POST.get("rmb", None) == "1":
        # 设置超时时间
        request.session.set_expiry(10)
    # 设置生效时间
    request.session.set_expiry(1 * 60)
# 获取用户名session
def get_userName(request):
    return request.session.get("username", None)
#  获取用户登录session
def get_session(request):
    is_login = request.session.get("is_login", None)
    print is_login
    return is_login
# 退出系统，清除session
def logout_view(request):
    # 删除用户session
    request.session.clear()
    # 注销
    return redirect("/login")

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

# 直接首页
def index_view(request):
    if not get_session(request):
        return redirect('/login')
    else:
        return redirect('/home/')

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
def __page(num=1):
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
    # 获取用户session,并判断是否正确，正确则继续运行，否则重定向登录页面
    if not get_session(request):
        return redirect('/login')
    num = int(num)
    books,page_list = __page(num)
    return render(request,'index.html',{'books':books,'page_list':page_list})

# 登录
def login_view(request):
    # global username
    if request.method=='GET':
        # username = ''
        # __del_session(request)
        return render(request, 'login.html')
    else:
        #接受数据
        name = request.POST.get('name','')
        pwd = request.POST.get('password','')
        # print name,pwd

        #判断是否登录成功

        count= Manager.objects.filter(name=name,pwd=pwd).count()

        if count == 1:
            # session中设置值
            __set_session(request,name)

            return redirect('/')

        else:
            return redirect('/login')


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

        return redirect('/login')



# #添加管理员系统
# def add_managerview(request):
#     return None

#添加书架
def add_case_view(request):
    if not get_session(request):
        return redirect('/login')
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
def selectAll(select,search):
    if select == 'barcode':
        book_infos = BookInfo.objects.filter(barcode__contains=search)
    elif select == 'bookname':
        book_infos = BookInfo.objects.filter(bookname__contains=search)
    elif select == 'author':
        book_infos = BookInfo.objects.filter(author__contains=search)
    elif select == 'booktype':
        try:
            id = BookType.objects.get(typename__contains=search).id
            book_infos = BookInfo.objects.filter(booktype=id)
        except:
            book_infos = []
    elif select == 'bookcase':
        try:
            id = Bookcase.objects.get(name__contains=search).id
            book_infos = BookInfo.objects.filter(bookcase=id)
        except:
            book_infos = []
    elif select == 'bookpub':
        try:
            id = Publishing.objects.get(name__contains=search).id
            book_infos = BookInfo.objects.filter(bookpub=id)
        except:
            book_infos = []
    print book_infos
    return book_infos
# 图书档案查询
def book_info_search_view(request):
    if not get_session(request):
        return redirect('/login')
    if request.method == 'GET':
        book_infos = []
    else:
        select = request.POST.get('select','')
        search = request.POST.get('search','')
        book_infos = selectAll(select,search)
    return  render(request,'book_info_search.html',{'book_infos':book_infos})
# 图书借阅查询
def borrowAll(timeFrom,timeTo):
    try:
        borrow = Borrow.objects.filter(borrowtime__gte=timeFrom).filter(borrowtime__lte=timeTo)
    except ValidationError:
        try:
            borrow = Borrow.objects.filter(borrowtime__gte=timeFrom)
        except ValidationError:
            borrow = Borrow.objects.filter(borrowtime__lte=timeTo)
    return borrow
# 图书借阅查询
def borrow_search_view(request):
    if not get_session(request):
        return redirect('/login')
    if request.method == 'GET':
        return render(request, 'borrow_search.html')
    else:
        select = request.POST.get('select', '')
        search = request.POST.get('search', '')
        timeFrom = request.POST.get('timeFrom','')
        timeTo = request.POST.get('timeTo','')
        borrows = []
        if timeFrom or timeTo:
            if select and search:
                books = selectAll(select, search)
                if books:
                    borrow = borrowAll(timeFrom, timeTo)
                    for book in books:
                        try:
                            bors = borrow.filter(book=book.id)
                            for bor in bors:
                                borrows.append(bor)
                        except:
                            continue
            else:
                borrow = borrowAll(timeFrom,timeTo)
                return render(request,'borrow_search.html',{'borrows':borrow})
        else:
            books = selectAll(select,search)
            if books:
                for book in books:
                    try:
                        borrow = Borrow.objects.filter(book=book)
                        for bo in borrow:
                            borrows.append(bo)
                    except:
                        continue

        return render(request,'borrow_search.html',{'borrows':borrows})
# 借阅到期提醒
def borrow_remind_view(request):
    if not get_session(request):
        return redirect('/login')
    now_time = datetime.now()
    remind_time = now_time + timedelta(days=14)
    remind_day = remind_time.strftime('%Y-%m-%d')
    reminds = Borrow.objects.filter(backtime__lte=remind_day)
    return render(request,'borrow_remind.html',{'reminds':reminds})

#图书借阅
def borrow_view(request):
    if not get_session(request):
        return redirect('/login')
    reader = None
    books = None
    success = None
    count = ''
    if request.method == 'POST':
        reader_barcode = request.POST.get('reader_barcode','')
        book = request.POST.get('book','')
        success = request.POST.get('success',None)
        current_day = date.today()#.strftime('%Y-%m-%d')
        try:
            reader = Reader.objects.get(barcode=reader_barcode)
            reader_number = reader.readertype.number
            reader_id = reader.id
            count = Borrow.objects.filter(reader_id=reader_id).count()
        except:
            pass
        try:
            books = BookInfo.objects.get(barcode=book)
            book_number = books.number
            borrow_number = books.borrownumber
            total_number = books.count
            print total_number
        except:
            pass
        # 判断是否借阅来完成读者与图书之间的借阅关系
        if success:
            # 1.先判断是否存在读者和图书
            if reader and books:
                book_id = books.id
                if book_number > borrow_number and count < reader_number:
                    borrow_number += 1
                    total_number += 1
                    print total_number
                    back_time = current_day + timedelta(days=books.booktype.days)
                    Borrow.objects.create(reader=reader,book=books,borrowtime=current_day,backtime=back_time)
                    BookInfo.objects.filter(id=book_id).update(borrownumber=borrow_number,count=total_number)
                    books = BookInfo.objects.get(barcode=book)
    return render(request,'borrow.html',{'reader':reader,'books':books,'success':success,'count':count})

#图书续借
def renew_view(request):
    return render(request,'renew.html')

#图书归还
def book_back_view(request):
    if not get_session(request):
        return redirect('/login')
    reader = None
    borrows = None
    checkbox = ''
    count = ''
    current_day = date.today()
    if request.method == 'POST':
        reader_barcode = request.POST.get('reader_barcode','')
        checkbox = request.POST.get('checkbox','')
        confirm = request.POST.get('confirm','')
        try:
            reader = Reader.objects.get(barcode=reader_barcode)
            reader_id = reader.id
            count = Borrow.objects.filter(reader_id=reader_id).count()
        except:
            reader = None
        if not checkbox and reader:
            borrows = Borrow.objects.filter(reader=reader)
        elif checkbox and reader:
            if not confirm:
                book = Borrow.objects.get(id=checkbox).book
                book_id = book.id
                borrow_number = Borrow.objects.get(id=checkbox).book.borrownumber - 1
                Borrow.objects.filter(reader=reader).filter(id=checkbox).delete()
                BookInfo.objects.filter(id=book_id).update(borrownumber=borrow_number)
                count = count - 1
                Giveback.objects.create(backtime=current_day,operator=get_userName(request),book=book,reader=reader)
            borrows = Borrow.objects.filter(reader=reader)
    return render(request,'book_back.html',{'reader':reader,'borrows':borrows,'count':count})


#添加更改口令功能
def pwd_modify_view(request):
    if not get_session(request):
        return redirect('/login')
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
                return redirect('/login')
        else:
            return HttpResponse('请检查原密码是否输入正确!')
        # elif len(name) == 0:
        #     return  HttpResponse('请检查用户名是否正确!')


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
    # if request.POST.get("rmb", None) == "1":
    #     # 设置超时时间
    #     request.session.set_expiry(10)
    # 设置生效时间
    request.session.set_expiry(60 * 60*10)
# 获取用户名session
def get_userName(request):
    return request.session.get("username", None)
# 获取用户登录session
def get_session(request):
    is_login = request.session.get("is_login", None)
    return is_login
# 退出系统，清除session
def logout_view(request):
    # 删除用户session
    # request.session.clear()
    request.session.set_expiry(-1)
    # 注销
    return redirect("/login")
# 用户权限
def purview_set(request,num=1):
    current_user = get_userName(request)
    manager = Manager.objects.get(name=current_user)
    if num == 1:
        if Purview.objects.get(manager=manager).sysset == 0:
            return False
        else:
            return True
    elif num == 2:
        if Purview.objects.get(manager=manager).readerset == 0:
            return False
        else:
            return True
    elif num == 3:
        if Purview.objects.get(manager=manager).bookset == 0:
            return False
        else:
            return True
    elif num == 4:
        if Purview.objects.get(manager=manager).borrowback == 0:
            return False
        else:
            return True
    elif num == 5:
        if Purview.objects.get(manager=manager).sysquery == 0:
            return False
        else:
            return True
# 系统设置
def modify_view(request):
    if not get_session(request):
        return redirect('/login')
    if not purview_set(request, 1):
        return HttpResponse('<script>alert("您没有权限进行访问");location.href="/home/"</script>')
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
        try:
            if Library.objects.first():
                Library.objects.update(name=name, curator=curator, tel=tel, address=address, email=email, url=url,
                                       createdate=createDate, introduce=introduce)
            else:
                Library.objects.create(name=name, curator=curator, tel=tel, address=address, email=email, url=url,
                                       createdate=createDate,introduce=introduce)
            return HttpResponse('<script>alert("修改成功");location.href="/modify/"</script>')
        except Exception:
            return HttpResponse('<script>alert("填写内容有误请重新填写");location.href="/modify/"</script>')
        # print '执行到这'
        # con = Library.objects.first()
        # return render(request, 'modify.html',{"con":con})


# 直接首页
def index_view(request):
    if not get_session(request):
        return redirect('/login')
    else:
        return redirect('/home/')

# 管理员设置
def manager_view(request):
    if not get_session(request):
        return redirect('/login')
    if not purview_set(request,1):
        return HttpResponse('<script>alert("您没有权限进行访问");location.href="/home/"</script>')
    id = request.GET.get('id', '')
    sysset = request.GET.get('sysset', '')
    readerset = request.GET.get('readerset', '')
    bookset = request.GET.get('bookset', '')
    borrowback = request.GET.get('borrowback', '')
    sysquery = request.GET.get('sysquery', '')
    # if sysset and readerset and bookset and borrowback and sysquery:
    #     print id, sysset, readerset, bookset, borrowback, sysquery
    #     print Manager.objects.filter(id=id)
    managers = Manager.objects.all()
    purviews = Purview.objects.all()
    if purviews.count() != managers.count():
        for manager in managers:
            if not purviews.filter(manager=manager):
                Purview.objects.create(manager=manager)
    # manager = Manager.objects.filter(id=id)
    try:
        man = Manager.objects.get(id=id)
        if man.name == get_userName(request):
            return HttpResponse('<script>alert("禁止修改已登录用户的权限");location.href="/manager/"</script>')
    except:
        pass
    if sysset and readerset and bookset and borrowback and sysquery and id:
        # if Purview.objects.all().order_by('id').first()
        try:
            pur = Purview.objects.all().order_by('id').first()
            if '%s'%pur.id == '%s'%id:
                return HttpResponse('<script>alert("禁止修改超级管理员的权限");location.href="/manager/"</script>')
        except:
            pass
        Purview.objects.filter(manager_id=id).update(sysset=sysset,readerset=readerset,bookset=bookset,borrowback=borrowback,sysquery=sysquery)
    return render(request, 'manager.html',{"managers":managers})
#删除管理员
def del_manager_view(request):
    if not get_session(request):
        return redirect('/login')
    if not purview_set(request, 1):
        return HttpResponse('<script>alert("您没有权限进行访问");location.href="/home/"</script>')
    id = request.GET.get('id','')
    if Manager.objects.get(id=id).name == get_userName(request):
        return HttpResponse('<script>alert("禁止操作当前登录用户");location.href="/manager/"</script>')
    Manager.objects.filter(id=id).delete()
    return HttpResponse('<script>alert("删除成功");location.href="/manager/"</script>')

# 参数设置
def parameter_view(request):
    if not get_session(request):
        return redirect('/login')
    if not purview_set(request, 1):
        return HttpResponse('<script>alert("您没有权限进行访问");location.href="/home/"</script>')
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
        try:
            if new_con:
                Parameter.objects.filter(id=1).update(cost=cost,validity=validity)
                return HttpResponse('<script>alert("保存成功");location.href="/parameter"</script>')
            else:
                Parameter.objects.create(cost=cost,validity=validity)
                return HttpResponse('<script>alert("保存成功");location.href="/parameter"</script>')
        except Exception:
                return HttpResponse('<script>alert("填写的类型有误请重写");location.href="/parameter"</script>')
# 书架设置
def bookcase_view(request):
    if not get_session(request):
        return redirect('/login')
    if not purview_set(request, 3):
        return HttpResponse('<script>alert("您没有权限进行访问");location.href="/home/"</script>')
    bookcase = Bookcase.objects.all()
    return render(request, 'bookcase.html',{'bookcase':bookcase})

# 分页
def __page(num=1):
    size = 3
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
            return HttpResponse('<script>alert("请输入正确用户名和密码");location.href="/login"</script>')


def register_view(request):
    if request.method=='GET':
        return render(request,'register.html')
    else:
        #接受数据
        name = request.POST.get('name','')
        pwd = request.POST.get('password','')

        # print name,password
        if name and pwd:
            try:
                manage = Manager.objects.get(name=name,pwd=pwd)
            except Manager.DoesNotExist:
                manage = Manager.objects.create(name=name,pwd=pwd)

            # manageInfo = Manager.objects.create(manage=manage)

            return HttpResponse('<script>alert("注册用户已存在");location.href="/login"</script>')
        else:
            return HttpResponse('<script>alert("注册用户不合法");location.href="/register"</script>')


# #添加管理员系统
# def add_managerview(request):
#     return None

#添加书架
def add_case_view(request):
    if not get_session(request):
        return redirect('/login')
    if not purview_set(request, 3):
        return HttpResponse('<script>alert("您没有权限进行访问");location.href="/home/"</script>')
    if request.method == 'GET':
        return render(request, 'add_case.html')
    else:
        add_name = request.POST.get('add_name','')
        search_name = Bookcase.objects.filter(name=add_name)
        if search_name:
            return HttpResponse('<script>alert("添加的书架已经存在");location.href="/bookcase/"</script>')
        else:
            Bookcase.objects.create(name=add_name)
            return HttpResponse('<script>alert("添加成功");location.href="/bookcase/"</script>')

#出版社设置
def pub_view(request):
    if not get_session(request):
        return redirect('/login')
    if not purview_set(request, 3):
        return HttpResponse('<script>alert("您没有权限进行访问");location.href="/home/"</script>')
    all_pub = Publishing.objects.all()
    return render(request,'pub.html',{'all_pub':all_pub})
#出版社添加
def add_pub_view(request):
    if not get_session(request):
        return redirect('/login')
    if not purview_set(request, 3):
        return HttpResponse('<script>alert("您没有权限进行访问");location.href="/home/"</script>')
    if request.method=='GET':
        return render(request,'add_pub.html')
    else:
        name = request.POST.get('add_name','')
        search_name = Publishing.objects.filter(name=name)
        if search_name:
            return HttpResponse('<script>alert("添加的出版社已经存在");location.href="/pub/"</script>')
        else:
            Publishing.objects.create(name=name)
            return HttpResponse('<script>alert("添加成功");location.href="/pub/"</script>')
#删除出版社
def del_pub_view(request):
    if not get_session(request):
        return redirect('/login')
    if not purview_set(request, 3):
        return HttpResponse('<script>alert("您没有权限进行访问");location.href="/home/"</script>')
    id = request.GET.get('id','')
    all_pub = Publishing.objects.get(id=id).bookinfo_set.all()
    if all_pub:
        return HttpResponse('<script>alert("请先将当前出版社书籍清空在做删除");location.href="/pub/"</script>')
    else:
        Publishing.objects.get(id=id).delete()
        return HttpResponse('<script>alert("删除成功");location.href="/pub/"</script>')
#修改出版社
def up_pub_view(request):
    if not get_session(request):
        return redirect('/login')
    if not purview_set(request, 3):
        return HttpResponse('<script>alert("您没有权限进行访问");location.href="/home/"</script>')
    if request.method=='GET':
        id = request.GET.get('id','')
        up_pub = Publishing.objects.get(id=id)
        return render(request,'up_pub.html',{'up_pub':up_pub})
    else:
        id = request.GET.get('id','')
        name = request.POST.get('up_name','')
        search_up = Publishing.objects.filter(name=name)
        if search_up:
            return HttpResponse('<script>alert("修改的出版社名已经存在");location.href="/pub/"</script>')
        else:
            Publishing.objects.filter(id=id).update(name=name)
            return HttpResponse('<script>alert("修改成功");location.href="/pub/"</script>')
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
    if not purview_set(request, 5):
        return HttpResponse('<script>alert("您没有权限进行访问");location.href="/home/"</script>')
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

#修改书架
def up_case_view(request):
    if not get_session(request):
        return redirect('/login')
    if not purview_set(request, 3):
        return HttpResponse('<script>alert("您没有权限进行访问");location.href="/home/"</script>')
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
            return HttpResponse('<script>alert("修改的书架名已经存在");location.href="/bookcase/"</script>')
        else:
            Bookcase.objects.filter(id=nid).update(name=up_name)
            return HttpResponse('<script>alert("修改成功");location.href="/bookcase/"</script>')

#删除书架
def del_case_view(request):
    if not get_session(request):
        return redirect('/login')
    if not purview_set(request, 3):
        return HttpResponse('<script>alert("您没有权限进行访问");location.href="/home/"</script>')
    id = request.GET.get('id','')
    print id
    id=int(id)
    all_book = Bookcase.objects.get(id=id).bookinfo_set.all()
    if all_book:
        return HttpResponse('<script>alert("请先清空书架在做删除");location.href="/bookcase/"</script>')
    else:
        Bookcase.objects.filter(id=id).delete()
        return HttpResponse('<script>alert("删除成功");location.href="/bookcase/"</script>')



#图书类型管理
def booktype_view(request):
    if not get_session(request):
        return redirect('/login')
    if not purview_set(request, 3):
        return HttpResponse('<script>alert("您没有权限进行访问");location.href="/home/"</script>')
    con_type = BookType.objects.all()
    return render(request,'book_type.html',{'con_type':con_type})

#图书类型添加
def add_booktype_view(request):
    if not get_session(request):
        return redirect('/login')
    if not purview_set(request, 3):
        return HttpResponse('<script>alert("您没有权限进行访问");location.href="/home/"</script>')
    if request.method == 'GET':
        return render(request,'add_booktype.html')
    else:
        name = request.POST.get('add_name','')
        day = request.POST.get('add_day','')
        search_name = BookType.objects.filter(typename=name)
        try:
            if search_name:
                return HttpResponse('<script>alert("添加的类型已经存在");location.href="/booktype/"</script>')

            else:
                BookType.objects.create(typename=name,days=day)
                return HttpResponse('<script>alert("添加成功");location.href="/booktype/"</script>')
        except Exception:
            return HttpResponse('<script>alert("输入的类型有误请重新添加");location.href="/add_booktype/"</script>')
#修改类型
def up_type_view(request):
    if not get_session(request):
        return redirect('/login')
    if not purview_set(request, 3):
        return HttpResponse('<script>alert("您没有权限进行访问");location.href="/home/"</script>')
    if request.method=='GET':
        id = request.GET.get('id', '')
        return render(request,'up_type.html',{'id':id})
    else:
        id = request.GET.get('id','')
        id = int(id)
        up_name = request.POST.get('up_name','')
        up_days = request.POST.get('up_days','')
        search_name = BookType.objects.filter(typename=up_name)
        try:
            if search_name:
                return HttpResponse('<script>alert("输入的类型已经存在");location.href="/booktype/"</script>')
            else:
                BookType.objects.filter(id=id).update(typename=up_name,days=up_days)
                return HttpResponse('<script>alert("修改成功");location.href="/booktype/"</script>')
        except Exception:
            return HttpResponse('<script>alert("修改的类型有误请重新修改");location.href="/booktype/"</script>')
#删除图书类型
def del_type_view(request):
    if not get_session(request):
        return redirect('/login')
    if not purview_set(request, 3):
        return HttpResponse('<script>alert("您没有权限进行访问");location.href="/home/"</script>')
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
    if not get_session(request):
        return redirect('/login')
    if not purview_set(request, 3):
        return HttpResponse('<script>alert("您没有权限进行访问");location.href="/home/"</script>')
    all_book = BookInfo.objects.all()
    return render(request,'book.html',{'all_book':all_book})


#图书添加功能
def add_book_view(request):
    if not get_session(request):
        return redirect('/login')
    if not purview_set(request, 3):
        return HttpResponse('<script>alert("您没有权限进行访问");location.href="/home/"</script>')
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
        type = request.POST.get('type','')
        case = request.POST.get('case','')
        pub = request.POST.get('pub','')
        search_name = BookInfo.objects.filter(bookname=bookname)
        try:
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
        except:
            return HttpResponse('<script>alert("添加的类型有误请重新添加");location.href="/add_book/"</script>')
#修改图书
def up_book_view(request):
    if not get_session(request):
        return redirect('/login')
    if not purview_set(request, 3):
        return HttpResponse('<script>alert("您没有权限进行访问");location.href="/home/"</script>')
    if request.method=='GET':
        id = request.GET.get('id','')
        all_type = BookType.objects.all()
        all_case = Bookcase.objects.all()
        all_pub = Publishing.objects.all()
        up_con = BookInfo.objects.get(id=id)
        return render(request,'up_book.html',{'id':id,'all_type': all_type, 'all_case': all_case, 'all_pub': all_pub,'up_con':up_con})
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
        search_name = BookInfo.objects.filter(bookname=bookname)
        try:
            # if search_name:
            #     return HttpResponse('<script>alert("修改的图书已经存在");location.href="/book/"</script>')
            # else:
            booktype = BookType.objects.get(typename=type)
            bookcase = Bookcase.objects.get(name=case)
            bookpub = Publishing.objects.get(name=pub)
            BookInfo.objects.filter(id=id).update(barcode=barcode, bookname=bookname, author=author, price=price,
                                                  number=number,bookpub=bookpub,booktype=booktype, bookcase=bookcase)
            return HttpResponse('<script>alert("修改成功");location.href="/book/"</script>')
        except Exception:
            return HttpResponse('<script>alert("修改的类型有误请重新修改");location.href="/book/"</script>')
#删除图书
def del_book_view(request):
    if not get_session(request):
        return redirect('/login')
    if not purview_set(request, 3):
        return HttpResponse('<script>alert("您没有权限进行访问");location.href="/home/"</script>')
    id = request.GET.get('id','')
    BookInfo.objects.filter(id=id).delete()
    return HttpResponse('<script>alert("删除成功");location.href="/book/"</script>')



# 图书借阅查询
def borrow_search_view(request):
    if not get_session(request):
        return redirect('/login')
    if not purview_set(request, 5):
        return HttpResponse('<script>alert("您没有权限进行访问");location.href="/home/"</script>')
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
    if not purview_set(request, 5):
        return HttpResponse('<script>alert("您没有权限进行访问");location.href="/home/"</script>')
    now_time = datetime.now()
    remind_time = now_time + timedelta(days=14)
    remind_day = remind_time.strftime('%Y-%m-%d')
    reminds = Borrow.objects.filter(backtime__lte=remind_day)
    return render(request,'borrow_remind.html',{'reminds':reminds})

#图书借阅
def borrow_view(request):
    if not get_session(request):
        return redirect('/login')
    if not purview_set(request, 4):
        return HttpResponse('<script>alert("您没有权限进行访问");location.href="/home/"</script>')
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
    if not get_session(request):
        return redirect('/login')
    if not purview_set(request, 4):
        return HttpResponse('<script>alert("您没有权限进行访问");location.href="/home/"</script>')
    if request.method=='GET':
        up = request.GET.get('up','')
        # print up
        if up:
            search_id = Borrow.objects.get(id=up)
            days = search_id.book.booktype.days
            new_backtime = search_id.backtime+timedelta(days=days)
            search_id.backtime=new_backtime
            search_id.save()
            search_rid = search_id.reader.id
            search_all = Reader.objects.get(id=search_rid)
            new_all = Borrow.objects.filter(reader_id=search_rid).all()
            # 总借阅数量
            count = Borrow.objects.filter(reader_id=search_rid).count()
            return render(request,'renew.html',{'search_code':search_all,'b_all':new_all,'count':count})
        else:
            return render(request, 'renew.html')
    else:
        code = request.POST.get('readercode','')
        try:
            search_code = Reader.objects.get(barcode=code)
            if search_code:
                b_all = search_code.borrow_set.all()
                # 总借阅数量
                count = Borrow.objects.filter(reader_id=search_code.id).count()
                return render(request,'renew.html',{'search_code':search_code,'b_all':b_all,'count':count})
            else:
                return HttpResponse('<script>alert("查无此人记录");location.href="/renew/"</script>')
        except:
            return HttpResponse('<script>alert("查无此人记录");location.href="/renew/"</script>')
#图书归还
def book_back_view(request):
    if not get_session(request):
        return redirect('/login')
    if not purview_set(request,4):
        return HttpResponse('<script>alert("您没有权限进行访问");location.href="/home/"</script>')
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

# 读者类型,删除读者类型,修改
def reader_type(request, id=0):
    if not get_session(request):
        return redirect('/login')
    if not purview_set(request, 2):
        return HttpResponse('<script>alert("您没有权限进行访问");location.href="/home/"</script>')
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
    if not get_session(request):
        return redirect('/login')
    if not purview_set(request, 2):
        return HttpResponse('<script>alert("您没有权限进行访问");location.href="/home/"</script>')
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
    if not get_session(request):
        return redirect('/login')
    if not purview_set(request, 2):
        return HttpResponse('<script>alert("您没有权限进行访问");location.href="/home/"</script>')
    if request.method == 'GET':
        con = ReaderType.objects.get(id=id)
        return render(request, 'modify_reader_type.html', {'con': con})


# 读者信息,修改，删除
def reader_view(request, id=0):
    if not get_session(request):
        return redirect('/login')
    if not purview_set(request, 2):
        return HttpResponse('<script>alert("您没有权限进行访问");location.href="/home/"</script>')
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
    if not get_session(request):
        return redirect('/login')
    if not purview_set(request, 2):
        return HttpResponse('<script>alert("您没有权限进行访问");location.href="/home/"</script>')
    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8')

    if request.method == "GET":
        sex = Sex.objects.all()
        if not sex:
            Sex.objects.create(id=1,sex='男')
            Sex.objects.create(id=2,sex='女')
        reader_types = ReaderType.objects.all()
        if not reader_types:
            return HttpResponse("<script>alert('没有可选的读者类型，请添加');location:href='/add_reader_type/';</script>")
        sexs = Sex.objects.all()
        return render(request, "add_readerinfo.html",{'sexs':sexs,'reader_types':reader_types})
    else:
        add_name = request.POST.get("add_name", "")
        add_sex = request.POST.get("add_sex", "")
        add_barcode = request.POST.get("add_barcode", "")
        add_tel = request.POST.get("add_tel", "")
        add_email = request.POST.get("add_email", "")
        add_created = request.POST.get("add_created", "")
        add_readertype = request.POST.get("add_readertype", "")
        print add_barcode,add_name,add_created,add_email,add_sex,add_readertype,add_tel
        try:
            search_barcode = Reader.objects.filter(barcode=add_barcode)
        except:
            search_barcode = []

        if not search_barcode:

            try:
                Reader.objects.create(name=add_name, sex_id=add_sex, barcode=add_barcode, tel=add_tel, email=add_email,
                                  created=add_created, readertype_id=add_readertype)
            except:
                pass
        return redirect("/reader/")


# 修改读者
def modify_reader(request, id=0):
    if not get_session(request):
        return redirect('/login')
    if not purview_set(request, 2):
        return HttpResponse('<script>alert("您没有权限进行访问");location.href="/home/"</script>')
    if request.method == 'GET':
        Re_ids = Reader.objects.get(id=id)
        return render(request, 'modify_reader.html', {'Re_ids': Re_ids})

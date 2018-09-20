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
    if not get_session(request):
        return redirect('/login')
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
    managers = Manager.objects.all()
    return render(request, 'manager.html',{"managers":managers})
#删除管理员
def del_manager_view(request):
    if not get_session(request):
        return redirect('/login')
    id = request.GET.get('id','')
    Manager.objects.filter(id=id).delete()
    return HttpResponse('<script>alert("删除成功");location.href="/manager/"</script>')

# 参数设置
def parameter_view(request):
    if not get_session(request):
        return redirect('/login')
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
    bookcase = Bookcase.objects.all()
    return render(request, 'bookcase.html',{'bookcase':bookcase})

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
    if not get_session(request):
        return redirect('/login')
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

#修改书架
def up_case_view(request):
    if not get_session(request):
        return redirect('/login')
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
    con_type = BookType.objects.all()
    return render(request,'book_type.html',{'con_type':con_type})

#图书类型添加
def add_booktype_view(request):
    if not get_session(request):
        return redirect('/login')
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
    all_book = BookInfo.objects.all()
    return render(request,'book.html',{'all_book':all_book})

#图书添加功能
def add_book_view(request):
    if not get_session(request):
        return redirect('/login')
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
            if search_name:
                return HttpResponse('<script>alert("修改的图书已经存在");location.href="/book/"</script>')
            else:
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
    id = request.GET.get('id','')
    BookInfo.objects.filter(id=id).delete()
    return HttpResponse('<script>alert("删除成功");location.href="/book/"</script>')



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
    if not get_session(request):
        return redirect('/login')
    if request.method=='GET':
        up = request.GET.get('up','')
        # print up
        if up:
            search_id = Borrow.objects.get(id=up)
            days = search_id.book.booktype.days
            new_backtime = search_id.backtime+timedelta(days=days)
            search_id.backtime=new_backtime
            search_id.save()
            new_all = Borrow.objects.all()
            search_rid = search_id.reader.id
            search_all = Reader.objects.get(id=search_rid)
            return render(request,'renew.html',{'search_code':search_all,'b_all':new_all})
        else:
            return render(request, 'renew.html')
    else:
        code = request.POST.get('readercode','')
        try:
            search_code = Reader.objects.get(barcode=code)
            if search_code:
                b_all = search_code.borrow_set.all()
                return render(request,'renew.html',{'search_code':search_code,'b_all':b_all})
            else:
                return HttpResponse('<script>alert("查无此人记录");location.href="/renew/"</script>')
        except:
            return HttpResponse('<script>alert("查无此人记录");location.href="/renew/"</script>')
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


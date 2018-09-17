#coding=utf-8
from django.shortcuts import render


def index(request):
    return render(request,'index.html')


def login(request):
    return render(request, 'login.html')


def pwd_modify(request):
    return render(request, 'pwd_modify.html')


def library_modify(request):
    return render(request,'library_modify.html')


def manage(request):
    return render(request,'manager.html')


def parameter(request):
    return render(request,'parameter_modify.html')


def bookcase(request):
    return render(request,'bookcase.html')


def reader_type(request):

    return render(request,'nav.html')


def reader(request):
    return render(request,'nav.html')


def book_type(request):
    return render(request,'book_type.html')


def book(request):
    return render(request,'book.html')


def borrow(request):
    return render(request,'borrow.html')


def renew(request):
    return render(request,'renew.html')


def book_back(request):
    return render(request,'book_back.html')


def book_query(request):
    return render(request,'book_query.html')


def borrow_query(request):
    return render(request,'borrow_query.html')


def bremind(request):
    return render(request,'bremind.html')


def base_html(request):
    return render(request,'base.html')
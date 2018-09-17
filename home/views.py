# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from home.models import Manager
from django.shortcuts import render, redirect
from .models import *

# Create your views here.


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


def home_view(request):
    return HttpResponse('123')
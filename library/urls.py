#coding=utf-8
"""library URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.static import serve

from library.settings import MEDIA_ROOT
from . import views
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # url(r'^base/',views.base_html),# base.html为基础模板，直接引用，已挖好{% block main_page %}
    url(r'^',include('home.urls')),

    # 以下是主路由测试html页面，用完请注释
    # url(r'^login/',views.login),
    # url(r'^index/',views.index),
    # url(r'^pwd/',views.pwd_modify),
    # url(r'^library/',views.library_modify),
    # url(r'^manage/',views.manage),
    # url(r'^parameter/',views.parameter),
    # url(r'^bookcase/',views.bookcase),
    # url(r'^reader_type/',views.reader_type),
    # url(r'^reader/',views.reader),
    # url(r'^book_type/',views.book_type),
    # url(r'^book/',views.book),
    # url(r'^borrow/',views.borrow),
    # url(r'^renew/',views.renew),
    # url(r'^book_back/',views.book_back),
    # url(r'^query/',views.book_query),
    # url(r'^bremind/',views.bremind),
    # url(r'^book_search/',views.borrow_query),

    url(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),#media的路由配置，应用路由请创建在上方
]

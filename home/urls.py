#coding=utf-8
from django.conf.urls import url

from home import views

urlpatterns=[
    url(r'^$',views.index_view),
    #系统设置
    url(r'^modify/$',views.modify_view),
    #管理员设置
    url(r'^manager/$',views.manager_view),
    #参数设置
    url(r'^parameter/$',views.parameter_view),
    #书架设置
    url(r'^bookcase/$',views.bookcase_view),
    #读者类型
    url(r'^reader_type/$', views.reader_type),
]
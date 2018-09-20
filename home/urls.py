#coding=utf-8
from django.conf.urls import url

from home import views

urlpatterns=[
    url(r'^login/',views.login_view),
    url(r'^register/',views.register_view),
    url(r'^home/$',views.home_view),
    url(r'^$',views.index_view),
    url(r'^home/(\d?)$',views.home_view),
    #系统设置
    url(r'^modify/$',views.modify_view),
    #管理员设置
    url(r'^manager/$',views.manager_view),
    #参数设置
    url(r'^parameter/$',views.parameter_view),
    #书架设置
    url(r'^bookcase/$',views.bookcase_view),
    #读者类型
    url(r'^reader_type/(\d*)$', views.reader_type),
    # 读者档案信息
    url(r'^reader/(\d*)$', views.reader_view),
    #添加书架
    url(r'^add_case/$',views.add_case_view),
    # 添加读者类型信息
    url(r'^add_reader_type/$', views.add_reader_type),
    # 修改读者类型
    url(r'^modify_reader_type/(\d*)$', views.modify_reader_type),
    # 添加读者
    url(r'^add_readerinfo/$', views.add_reader),
    # 修改读者
    url(r'^modify_reader/(\d*)$', views.modify_reader),
]
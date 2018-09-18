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
    #添加书架
    url(r'^add_case/$',views.add_case_view),
    #修改书架
    url(r'^up_case/$',views.up_case_view),
    #删除书架
    url(r'^del_case/$',views.del_case_view),
    #图书类型管理
    url(r'^booktype/$',views.booktype_view),
    #图书类型添加
    url(r'^add_booktype/$',views.add_booktype_view),
    #图书类型修改
    url(r'^up_type/$',views.up_type_view),
    #删除图书类型
    url(r'^del_type/$',views.del_type_view),
    #图书档案管理
    url(r'^book/$',views.book_view),
    #添加图书
    url(r'^add_book/$',views.add_book_view)

]
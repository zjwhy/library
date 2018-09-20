#coding=utf-8
from django.conf.urls import url

from home import views

urlpatterns=[
    url(r'^login/$',views.login_view),
    url(r'^logout/$',views.logout_view),
    url(r'^register/$',views.register_view),
    url(r'^home/$',views.home_view),
    url(r'^$',views.index_view),
    url(r'^home/(\d?)$',views.home_view),
    #系统设置
    url(r'^modify/$',views.modify_view),
    #管理员设置
    url(r'^manager/$',views.manager_view),
    #删除管理员
    url(r'^del_manager/$',views.del_manager_view),
    #参数设置
    url(r'^parameter/$',views.parameter_view),
    #书架设置
    url(r'^bookcase/$',views.bookcase_view),
    #读者类型
    url(r'^reader_type/(\d*)$', views.reader_type),
    # 读者档案信息
    url(r'^reader/(\d*)$', views.reader_view),
    # 添加读者类型信息
    url(r'^add_reader_type/$', views.add_reader_type),
    # 修改读者类型
    url(r'^modify_reader_type/(\d*)$', views.modify_reader_type),
    # 添加读者
    url(r'^add_readerinfo/$', views.add_reader),
    # 修改读者
    url(r'^modify_reader/(\d*)$', views.modify_reader),

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
    url(r'^add_book/$',views.add_book_view),
    #修改图书
    url(r'^up_book/$',views.up_book_view),
    #删除图书
    url(r'^del_book/$',views.del_book_view),
    #图书借阅
    url(r'^borrow/$',views.borrow_view),

    #图书续借
    url(r'^renew/$',views.renew_view),

    #图书归还
    url(r'^book_back/$',views.book_back_view),

    # 更改口令
    url(r'^pwd_modify/$', views.pwd_modify_view),

    # 系统查询
    # 图书信息查询
    url(r'^book_info_search/$', views.book_info_search_view),
    # 图书借阅查询
    url(r'^borrow_search/$', views.borrow_search_view),
    # 借阅到期提醒
    url(r'^borrow_remind/$', views.borrow_remind_view),


]
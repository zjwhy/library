#coding=utf-8
from django.conf.urls import url

from home import views

urlpatterns=[
    url(r'^login/',views.login_view),
    url(r'^register/',views.register_view),
    url(r'^home/$',views.home_view),
    url(r'^$',views.index_view),
    url(r'^home/$',views.home_view),
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

]
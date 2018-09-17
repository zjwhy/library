#coding=utf-8
from django.conf.urls import url
import views

urlpatterns=[
    url(r'^login/',views.login_view),
    url(r'^register/',views.register_view),
    url(r'^home/$',views.home_view),

]
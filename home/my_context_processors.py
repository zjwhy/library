#coding=utf-8

def myData(request):
    from .views import username



    return {'username':username}
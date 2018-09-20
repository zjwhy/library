#coding=utf-8

def myData(request):
    try:
        current_user = request.session["username"]
    except:
        current_user = ''
    return {'username':current_user}

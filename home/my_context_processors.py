#coding=utf-8

def __current_page():
    return ['首页','系统设置','图书馆信息','管理员设置','参数设置','书架设置',
            '读者管理','读者类型管理','读者档案管理',
            '图书管理','图书类型管理','图书档案管理',
            '图书借还','图书借阅','图书续借','图书归还',
            '系统查询','图书档案查询','图书借阅查询','借阅到期提醒',
            '更改口令',
            '退出系统'
            ]

def myData(request):
    try:
        current_user = request.session["username"]
    except:
        current_user = ''
    return {'username':current_user,'pages':__current_page()}

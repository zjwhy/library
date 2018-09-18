# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# 书架
class Bookcase(models.Model):
    id = models.AutoField(primary_key=True,unique=True)
    name = models.CharField(max_length=30,unique=True, blank=True, null=True)
    # column_3 = models.CharField(db_column='Column_3', max_length=10, blank=True, null=True)  # Field name made lowercase.
    class Meta:
        db_table = 't_bookcase'

# 图书类型
class BookType(models.Model):
    id = models.AutoField(primary_key=True,unique=True)
    typename = models.CharField(max_length=30, blank=True, null=True)
    days = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 't_booktype'

# 出版社
class Publishing(models.Model):
    id = models.AutoField(primary_key=True,unique=True)
    # isbn = models.CharField(db_column='ISBN', max_length=20, blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(max_length=30, blank=True, null=True,verbose_name='出版社名称')

    class Meta:
        db_table = 't_publishing'

# 图书信息
class BookInfo(models.Model):
    id = models.AutoField(primary_key=True,unique=True)
    barcode = models.CharField(max_length=30, blank=True, null=True,verbose_name='条形码')
    bookname = models.CharField(max_length=70, blank=True, null=True,verbose_name='书名')
    booktype = models.ForeignKey(BookType,on_delete=models.CASCADE)
    author = models.CharField(max_length=30, blank=True, null=True,verbose_name='作者')
    # isbn = models.CharField(db_column='ISBN', max_length=20, blank=True, null=True)  # Field name made lowercase.
    price = models.FloatField(blank=True, null=True,verbose_name='价格')
    # page = models.IntegerField(blank=True, null=True,verbose_name='书页')
    bookcase = models.ForeignKey(Bookcase,on_delete=models.CASCADE)
    bookpub = models.ForeignKey(Publishing,on_delete=models.CASCADE)
    # intime = models.DateField(db_column='inTime', blank=True, null=True,verbose_name='馆藏日期')  # Field name made lowercase.
    # operator = models.CharField(max_length=30, blank=True, null=True,verbose_name='操作者')
    # del_field = models.IntegerField(db_column='del', blank=True, null=True,verbose_name='撤管时间')  # Field renamed because it was a Python reserved word.
    number = models.IntegerField(blank=True,default=1,verbose_name='馆藏数量')
    borrownumber = models.IntegerField(blank=True,default=1,verbose_name='借出数量')
    count = models.IntegerField(blank=True,default=0,verbose_name='借阅次数')
    class Meta:
        db_table = 't_bookinfo'



# 图书馆
class Library(models.Model):
    id = models.AutoField(primary_key=True,unique=True)
    name = models.CharField(max_length=50, blank=True, null=True,verbose_name='图书馆名称')
    curator = models.CharField(max_length=10, blank=True, null=True,verbose_name='馆长')
    tel = models.CharField(max_length=20, blank=True, null=True,verbose_name='联系电话')
    address = models.CharField(max_length=100, blank=True, null=True,verbose_name='联系地址')
    email = models.CharField(max_length=100, blank=True, null=True,verbose_name='联系邮箱')
    url = models.CharField(max_length=100, blank=True, null=True,verbose_name='图书馆地址')
    createdate = models.DateField(db_column='createDate', blank=True, null=True,verbose_name='建管时间')  # Field name made lowercase.
    introduce = models.TextField(blank=True, null=True,verbose_name='图书馆简介')

    class Meta:
        db_table = 't_library'

# 性别
class Sex(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    sex = models.CharField(max_length=4, blank=True, null=True, verbose_name='性别')

    class Meta:
        db_table = 't_sex'

# 读者类型
class ReaderType(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=50, blank=True, null=True, verbose_name='读者类型')
    number = models.IntegerField(blank=True, null=True, verbose_name='可借数量')

    class Meta:
        db_table = 't_readertype'

# 读者信息
class Reader(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=20, blank=True, null=True, verbose_name='读者姓名')
    sex = models.ForeignKey(Sex, on_delete=models.CASCADE)
    barcode = models.CharField(max_length=30, blank=True, null=True, verbose_name='条形码')
    tel = models.CharField(max_length=20, blank=True, null=True, verbose_name='电话')
    email = models.CharField(max_length=100, blank=True, null=True, verbose_name='Email')
    created = models.DateField(blank=True, null=True, verbose_name='创建日期')
    readertype = models.ForeignKey(ReaderType, on_delete=models.CASCADE)

    class Meta:
        db_table = 't_reader'




# 管理员
class Manager(models.Model):
    id = models.AutoField(primary_key=True,unique=True)
    name = models.CharField(max_length=30, blank=True, null=True)
    pwd = models.CharField(db_column='PWD', max_length=30, blank=True, null=False)  # Field name made lowercase.

    class Meta:
        db_table = 't_manager'

# 参数
class Parameter(models.Model):
    id = models.AutoField(primary_key=True,unique=True)
    cost = models.IntegerField(blank=True, null=True,verbose_name='办证费')
    validity = models.IntegerField(blank=True, null=True,verbose_name='有效期限')

    class Meta:
        db_table = 't_parameter'

# 管理权限
class Purview(models.Model):
    id = models.AutoField(primary_key=True,unique=True)
    manager = models.ForeignKey(Manager,models.CASCADE)#管理员权限
    sysset = models.IntegerField(blank=True, null=True,verbose_name='系统设置')
    readerset = models.IntegerField(blank=True, null=True,verbose_name='读者管理')
    bookset = models.IntegerField(blank=True, null=True,verbose_name='图书管理')
    borrowback = models.IntegerField(blank=True, null=True,verbose_name='借还管理')
    sysquery = models.IntegerField(blank=True, null=True,verbose_name='系统查询')
    class Meta:
        db_table = 't_purview'




# 借阅表
class Borrow(models.Model):
    id = models.AutoField(primary_key=True,unique=True)
    reader = models.ForeignKey(Reader,on_delete=models.CASCADE)
    book = models.ForeignKey(BookInfo,on_delete=models.CASCADE)
    borrowtime = models.DateField(blank=True, null=True,verbose_name='借出日期')  # Field name made lowercase.
    backtime = models.DateField(blank=True, null=True,verbose_name='归还时间')  # Field name made lowercase.
    # operator = models.CharField(max_length=30, blank=True, null=True,verbose_name='操作者')
    # ifback = models.BooleanField(blank=True, null=True,verbose_name='是否归还')

    class Meta:
        db_table = 't_borrow'

# 归还表
class Giveback(models.Model):
    id = models.AutoField(primary_key=True,unique=True)
    reader = models.ForeignKey(Reader, on_delete=models.CASCADE)
    book = models.ForeignKey(BookInfo, on_delete=models.CASCADE)
    backtime = models.DateField(blank=True, null=True,verbose_name='归还时间')
    operator = models.CharField(max_length=30, blank=True, null=True,verbose_name='操作者')

    class Meta:
        db_table = 't_giveback'
#coding=utf-8

from django.template import Library

register = Library()

#自定义函数(参数为处理内容)
@register.filter
def md(value):
    import markdown
    # 解析内容
    return markdown.markdown(value)

@register.filter
def current_page(value,url):
    print value,url
    return url



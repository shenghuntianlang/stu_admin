# -*- coding:utf-8 -*-
from mingjia_admin.models import *
from django.http import HttpResponseRedirect, HttpResponse


def login(func):
    def login_fun(request,p=1, p1=2):
        if 'username' in request.COOKIES.keys():
            admin = Admin.objects.all().filter(name=request.COOKIES['username'])
            if admin.count() != 1:
                return HttpResponseRedirect('/user/')
        else:
            return HttpResponseRedirect('/user/')
        print ' func(request)被执行'
        return func(request)
    return login_fun

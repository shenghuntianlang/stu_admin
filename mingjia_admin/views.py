# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from mingjia_admin.models import *
from django.views.decorators.csrf import csrf_exempt
import json
from user import user_decorator

KEY = 'username'


# Create your views here.
@user_decorator.login
def test(request):
    cookie = request.COOKIES['username']
    print cookie
    admins = Admin.objects.all()
    admins.count()
    return HttpResponse(Course.objects.all().first().name)


@user_decorator.login
def index(request):
    return render_to_response('index.html')


def login(request):
    return render_to_response('login.html')


def log_out(request):
    """
    退出登录

    """

    response = HttpResponseRedirect(redirect_to='/login/')
    response.delete_cookie(KEY)
    return response


@csrf_exempt
def login_handle(request):
    # cookie的key
    # 处理用户登录的逻辑
    login_info = json.loads(request.body)
    username = login_info['user_name']
    password = login_info['password']

    print("username-> %s password-> %s" % (username, password))
    admins = Admin.objects.all().filter(name=username, password=password)
    resp = Response()
    resp.status = 200

    response = HttpResponse(content_type='application/json')
    if admins.count() > 0:
        print "登录成功"
        resp.result = 'success'
        response.set_cookie(KEY, username, max_age=60 * 60)

    else:
        print "登录失败"
        resp.result = 'failed'
        # unicode=  domian =
        response.delete_cookie(KEY)

    # 当遇到异常的时候返回500等错误代码
    resp_json = json.dumps(resp.__dict__)
    response.content = resp_json

    print resp_json

    return response


@user_decorator.login
def admin_add(request):
    return render_to_response('admin-add.html')


@csrf_exempt
def admin_add_handle(request):
    print request.body
    # 报名学生的相关信息
    student_info = json.loads(request.body)
    print student_info['student_name']
    student = Student()
    # 考虑出现重名的情况
    student.name = student_info['student_name']
    student.gender = student_info['sex']
    student.phone = student_info['phone']
    student.entrance_time = student_info['entrance_time']
    student.school_name = student_info['school_name']
    student.class_name = student_info['class_id']
    student.course_id = student_info['course_id']

    # student.register_date =
    student.remark = student_info['remark']
    student.save()
    resp = Response()
    resp.status = 200
    resp.result = 'success'
    return HttpResponse(json.dumps(resp.__dict__, encoding='utf-8'), content_type='application/json')


def admin_student_manager(reuqest):
    return render_to_response('admin-student.html')


def get_students(request, page=1):
    student_all = Student.objects.filter(is_delete=0)
    total = student_all.count()
    paginator = Paginator(student_all, 3)
    page = paginator.page(int(page))
    page_range = paginator.page_range
    print page_range
    context = {'page': page, 'total': total, 'page_range': page_range}
    return render(request, 'admin-student.html', context)


def admin_edit(request):
    return render_to_response('admin-edit.html')


class Response:
    def __init__(self):
        pass

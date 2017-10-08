# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals

from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from mingjia_admin.models import *
from django.views.decorators.csrf import csrf_exempt
import json
import datetime
from user import user_decorator

KEY = 'username'


# Create your views here.
@user_decorator.login
def test(request):
    cookie = request.COOKIES['username']
    print
    cookie
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
        print
        "登录成功"
        resp.result = 'success'
        response.set_cookie(KEY, username, max_age=60 * 60)

    else:
        print
        "登录失败"
        resp.result = 'failed'
        # unicode=  domian =
        response.delete_cookie(KEY)

    # 当遇到异常的时候返回500等错误代码
    resp_json = json.dumps(resp.__dict__)
    response.content = resp_json

    print
    resp_json

    return response


def get_courses():
    '''
    从数据库中获取班次信息
    :return:
    '''
    return Course.objects.filter(is_delete=0).order_by('-id')


@user_decorator.login
def admin_add(request):
    courses = get_courses()
    context = {'courses': courses}
    return render(request, 'admin-add.html', context=context)


@csrf_exempt
def admin_add_handle(request):
    # 报名学生的相关信息
    student_info = json.loads(request.body)
    student = Student()
    # 考虑出现重名的情况
    student.name = student_info['student_name']
    student.gender = student_info['sex']
    student.phone = student_info['phone']
    student.entrance_time = student_info['entrance_time']
    student.school_name = student_info['school_name']
    student.class_name = student_info['class_id']
    student.course_id = student_info['course_id']
    student.register_date = datetime.date.today()
    student.remark = student_info['remark']
    student.save()
    resp = Response()
    resp.status = 200
    resp.result = 'success'
    return HttpResponse(json.dumps(resp.__dict__, encoding='utf-8'), content_type='application/json')


def admin_student_manager(request, page_index=1):
    students = Student.objects.filter(is_delete=0)
    paginator = Paginator(students, 10)
    # 当前页面的内容
    page = paginator.page(int(page_index))
    for p in page:
        p.register_date = p.register_date.strftime("%Y-%m-%d")
    # 页面展示的范围
    page_range = paginator.page_range
    print(len(page_range))
    context = {'students': page,
               'courses': get_courses(),
               'total': students.count(),
               'page_index': page_index,
               'page_range': page_range,
               'max_page': len(page_range),
               'is_search': False}

    return render(request, 'admin-student.html', context=context)


def get_search_params(request):
    """
    获取查询学生信息时，传递过来的查询参数
    :param request:
    :return: search_params 封装查询参数的字典
    """
    search_params = {}

    for key in request.GET.keys():
        value = request.GET[key]
        if value.strip():
            if key != 'course_id':
                search_params[key + "__contains"] = value
            else:
                search_params[key] = value

    search_params['is_delete'] = 0
    return search_params


def get_students(request, page_index=1):
    students = None
    # 搜索
    # if not page_index.strip() and len(request.GET.keys()) > 0:
    search_params = get_search_params(request)
    # search_params1 = {'course_id': 1, 'name__contains': '王', 'is_delete': 0}
    students = Student.objects.filter(**search_params)
    search_params['course_id'] = long(search_params['course_id'])
    context = {'students': students,
               'courses': get_courses(),
               'search_params': search_params,
               'total': students.count(),
               'is_search': True}

    return render(request, 'admin-student.html', context)


def del_student(request, stu_id):
    """
    删除单个
    :param request:
    :param stu_id:
    :return:
    """
    resp = Response()
    resp.status = 200
    resp.result = 'success'
    resp_json = json.dumps(resp.__dict__)
    student = Student.objects.get(id=stu_id)
    # 删除
    student.is_delete = 1
    student.save()
    return HttpResponse(resp_json, content_type='application/json')


@csrf_exempt
def del_students(request):
    """
    批量删除
    :param request:
    :return:
    """
    del_list = json.loads(request.body)

    # 批量删除
    for stu_id in del_list:
        student = Student.objects.get(id=stu_id)
        student.is_delete = 1
        student.save()

    resp = Response();
    resp.status = 200
    resp.result = 'success'

    resp_json = json.dumps(resp.__dict__)
    return HttpResponse(resp_json, 'application/json')


def admin_student_edit(request, stu_id):
    student = Student.objects.get(id=stu_id)
    student.entrance_time = student.entrance_time.strftime("%Y-%m-%d")
    context = {'student_info': student,
               'courses': get_courses()
               }
    return render(request, 'admin-edit.html', context)


@csrf_exempt
def admin_student_edit_handle(request):
    student_info = json.loads(request.body, 'utf-8')

    student = Student.objects.all().get(id=student_info['student_id'])

    student.name = student_info['student_name']
    student.gender = student_info['sex']
    student.phone = student_info['phone']
    student.entrance_time = student_info['entrance_time']
    student.school_name = student_info['school_name']
    student.class_name = student_info['class_id']
    student.course_id = student_info['course_id']
    student.register_date = datetime.date.today()
    student.remark = student_info['remark']
    student.save()
    resp = Response()
    resp.status = 200
    resp.result = 'success'
    return HttpResponse(json.dumps(resp.__dict__), content_type='application/json')


def admin_teacher_add(request):
    return render_to_response('admin-teacher-add.html')


def get_birthday(identity):
    """
    从身份证号码中获取出生日期
    :param identity: 身份证号码
    :return: date -> 出生日期
    """
    year = int(identity[6:10])
    month = int(identity[10:12])
    day = int(identity[12:14])
    return datetime.date(year, month, day)


@csrf_exempt
def admin_teacher_add_handle(request):
    print(request.body)
    teacher_info = json.loads(request.body)

    teacher = Teacher()
    teacher.name = teacher_info['teacher_name']
    identity = teacher_info['identity']
    teacher.id_number = identity
    teacher.birthday = get_birthday(identity)
    teacher.gender = teacher_info['gender']
    teacher.edu = teacher_info['edu']
    teacher.english_level = teacher_info['english_level']
    teacher.entry_date = teacher_info['entrance_time']
    teacher.remark = teacher_info['remark']
    teacher.phone = teacher_info['phone']
    teacher.is_delete = 0
    teacher.save()

    resp = Response()
    resp.status = 200
    resp.result = 'success'
    resp_json = json.dumps(resp.__dict__)
    return HttpResponse(resp_json, content_type='application/json')


def admin_teacher_manager(request, page_index=1):
    return render_to_response('admin-teacher.html')


class Response:
    status = 200
    result = None

    def __init__(self):
        pass


class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)
            # {u'course_id': u'2', u'school_name__contains': u'\u51af', u'is_delete': 0}

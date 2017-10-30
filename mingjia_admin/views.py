# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals

import os
import xlwt
import xlrd
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect, StreamingHttpResponse
from django.shortcuts import render, render_to_response
from mingjia_admin.models import *
from django.views.decorators.csrf import csrf_exempt
import json
import datetime
import time
from user import user_decorator

KEY = 'username'
limit = 30


# Create your views here.
@user_decorator.login
def test(request):
    cookie = request.COOKIES['username']
    admins = Admin.objects.all()
    admins.count()
    return HttpResponse(Course.objects.all().first().name)


# ********************** 登录  **********************

@user_decorator.login
def index(request):
    username = request.COOKIES[KEY]
    context = {'username': username}
    return render(request, 'index.html', context)


def login(request):
    """
    返回登录对应的html页面
    :param request:
    :return:
    """
    return render_to_response('login.html')


@csrf_exempt
def login_handle(request):
    """
    处理登录逻辑
    :param request:
    :return:
    """
    # cookie的key
    # 处理用户登录的逻辑
    login_info = json.loads(request.body)
    username = login_info['user_name']
    password = login_info['password']

    admins = Admin.objects.all().filter(name=username, password=password)
    resp = Response()
    resp.status = 200

    response = HttpResponse(content_type='application/json')
    if admins.count() > 0:
        resp.result = 'success'
        response.set_cookie(KEY, username, max_age=60 * 60)

    else:
        resp.result = 'failed'
        response.delete_cookie(KEY)
    # 当遇到异常的时候返回500等错误代码
    resp_json = json.dumps(resp.__dict__)
    response.content = resp_json

    return response


def log_out(request):
    """
    退出登录
    :param request:
    :return:
    """
    response = HttpResponseRedirect(redirect_to='/user/')
    response.delete_cookie(KEY)
    return response


# ********************** 登录 **********************


# ********************** 学员管理 **********************

@user_decorator.login
def admin_add_stu(request):
    """
    学员添加
    :param request:
    :return: 返回班次和小学信息
    """
    courses = get_courses()
    schools = School.objects.all().filter(is_delete=2)
    context = {'courses': courses,
               'schools': schools
               }
    return render(request, 'admin-stu-add.html', context=context)


@csrf_exempt
def admin_add_stu_handle(request):
    """
    学员报名
    :param request:
    :return:
    """
    # 报名学生的相关信息
    student_info = json.loads(request.body)
    student = Student()

    # 考虑出现重名的情况
    student.name = student_info['student_name']
    student.gender = student_info['sex']
    student.phone = student_info['phone']
    student.entrance_time = student_info['entrance_time']
    print(student_info['school_name'])
    student.school_id = student_info['school_name']
    student.class_name = student_info['class_id']
    student.course_id = student_info['course_id']
    student.register_date = datetime.date.today()
    student.remark = student_info['remark']
    student.is_delete = 0
    student.save()

    resp = Response()
    resp.status = 200
    resp.result = 'success'

    # 班次id
    course_id = student_info['course_id']

    # 当选择的班级不是暂无安排的时候才进行人数的判断
    if int(course_id) != 1:
        course = Course.objects.get(id=course_id)

        # 当前人数
        curr_num = Student.objects.all().filter(course_id=course_id).count()
        # print('当前人数-->', curr_num)
        # 这个班次总共可容纳的人数
        if course.class_field != None:
            places = course.class_field.places
            if curr_num >= places:
                resp.remark = "注意！！！当前班次可容纳的总人数为: " + str(places) + "人, 当前的报名人数为: " + str(curr_num) + "人, 请注意是否继续报名!"

    return HttpResponse(json.dumps(resp.__dict__, encoding='utf-8'), content_type='application/json')


@user_decorator.login
def admin_stu_manager(request):
    """
    学员管理
    111
    :param request:
    :param page_index:
    :param is_new: 1->新生 0-> 普通学员 用于标记是否是新生(班次为暂无安排的被标记为新生)
    :return:
    """

    page_index = request.GET['page_index']
    is_new = request.GET['is_new']

    stu = admin_get_student(page_index, is_new)

    # 页面展示的范围
    page_range = stu[0].page_range

    context = {'students': stu[1],
               'courses': get_courses(),
               'limit': stu[2],
               'total': stu[3].count(),
               'page_index': page_index,
               'page_range': page_range,
               'max_page': len(page_range),
               'is_new': int(is_new),
               'is_search': False}

    return render(request, 'admin-stu.html', context=context)


def admin_get_student(page_index, is_new):
    """
    根据所在页获取学生信息
    :param page_index:
    :param is_new: 是否是新入学的学生
    :return: 返回一个元组包含与学生相关信息
    """
    if is_new == '1':
        students = Student.objects.filter(is_delete=0).filter(course_id=7)
    else:
        students = Student.objects.filter(is_delete=0)

    paginator = Paginator(students, limit)
    # 当前页面的内容
    page = paginator.page(int(page_index))
    for p in page:
        p.grade = calculate_grade(p.entrance_time)
        p.entrance_time = p.entrance_time.strftime("%Y-%m-%d")
        if p.register_date != None:
            p.register_date = p.register_date.strftime("%Y-%m-%d")
        # 计算学员就读的年级并更新数据库中的字段
        stu = Student.objects.get(id=p.id)
        p.temp_class = calculate_grade(stu.entrance_time)
        stu.temp_class = p.temp_class
        stu.save()

    return (paginator, page, limit, students)


@user_decorator.login
def admin_search_stu(request):
    """
    根据条件搜索学生
    :param request:
    :param is_new:
    :return:
    """
    is_new = request.GET['is_new']

    search_params = admin_get_search_stus_params(request)

    print(is_new)

    if int(is_new) == 1:
        search_params['course_id'] = 7

    print(search_params)

    students = Student.objects.filter(**search_params)
    for s in students:
        if s.register_date != None:
            s.register_date = s.register_date.strftime("%Y-%m-%d")
        s.temp_class = calculate_grade(s.entrance_time)

    if 'course_id' in search_params.keys():
        search_params['course_id'] = long(search_params['course_id'])

    context = {'students': students,
               'courses': get_courses(),
               'search_params': search_params,
               'total': students.count(),
               'is_new': int(is_new),
               'is_search': True}

    return render(request, 'admin-stu.html', context)


def admin_get_search_stus_params(request):
    """
    获取查询学生信息时，传递过来的查询参数
    :param request:
    :return: search_params 封装查询参数的字典
    """
    search_params = {}
    for key in request.GET.keys():
        value = request.GET[key]
        if value.strip():
            # 用于过滤打印时上传的参数
            if key == 'type' or key == 'is_search' or key == 'is_new' or key == 'index':
                continue
            elif key == 'course_id':
                search_params[key] = value
            elif key == 'temp_class':
                search_params[key] = value
            elif key == 'school_name':
                search_params['school__school_name__contains'] = value
            else:
                search_params[key + "__contains"] = value
    search_params['is_delete'] = 0
    search_params['school__is_delete'] = 2
    return search_params


@user_decorator.login
def admin_del_stu(request):
    """
    删除单个学生
    :param request:
    :param stu_id:
    :return:
    """

    stu_id = request.GET['stu_id']
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
def admin_del_stus(request):
    """
    批量删除学生
    :param request:
    :return:
    """
    del_list = json.loads(request.body)

    # 批量删除
    for stu_id in del_list:
        student = Student.objects.get(id=stu_id)
        student.is_delete = 1
        student.save()

    resp = Response()
    resp.status = 200
    resp.result = 'success'

    resp_json = json.dumps(resp.__dict__)
    return HttpResponse(resp_json, 'application/json')


@user_decorator.login
def admin_stu_edit(request):
    stu_id = request.GET['stu_id']
    student = Student.objects.get(id=stu_id)
    student.entrance_time = student.entrance_time.strftime("%Y-%m-%d")

    schools = School.objects.filter(is_delete=2)

    print(schools)

    context = {'student_info': student,
               'courses': get_courses(),
               'schools': schools
               }

    return render(request, 'admin-stu-edit.html', context)


@csrf_exempt
@user_decorator.login
def admin_stu_edit_handle(request):
    student_info = json.loads(request.body, 'utf-8')
    student = Student.objects.all().get(id=student_info['student_id'])
    student.name = student_info['student_name']
    student.gender = student_info['sex']
    student.phone = student_info['phone']
    student.entrance_time = student_info['entrance_time']

    print(student_info['school_name'])
    student.school_id = student_info['school_name']
    student.class_name = student_info['class_id']
    student.course_id = student_info['course_id']
    student.register_date = datetime.date.today()
    student.remark = student_info['remark']

    student.save()

    resp = Response()
    resp.status = 200
    resp.result = 'success'
    return HttpResponse(json.dumps(resp.__dict__), content_type='application/json')


@user_decorator.login
def admin_stu_detail(request):
    """
    查看学生详情
    :param request:
    :param student_id:
    :return:
    """
    stu_id = request.GET['stu_id']
    student = Student.objects.all().get(id=stu_id)
    student.entrance_time = student.entrance_time.strftime("%Y-%m-%d")
    if student.register_date != None:
        student.register_date = student.register_date.strftime("%Y-%m-%d")
    context = {'student_info': student}
    return render(request, 'admin-stu-detail.html', context)


# ********************** 学员管理 **********************


# ********************** 教师管理 **********************

@user_decorator.login
def admin_teacher_add(request):
    """
    携带数据，返回页面
    :param request:
    :return:
    """
    context = {'edu': get_edu(),
               'english_level': get_english_level()
               }
    return render(request, 'admin-teacher-add.html', context)


@csrf_exempt
def admin_teacher_add_handle(request):
    """
    处理增加教师的逻辑
    :param request:
    :return:
    """

    teacher_info = json.loads(request.body)
    teacher = Teacher()
    print(teacher_info['teacher_name'])
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


@user_decorator.login
def admin_teacher_leave(request):
    """
    设置教师离职
    :param request:
    :param teacher_id:
    :return:
    """
    teacher_id = request.GET['teacher_id']
    teacher = Teacher.objects.get(id=teacher_id)
    # print(teacher.name)

    resp = Response()
    resp.status = 200
    if teacher.leave_date == None:
        # 设置为离职状态，添加离职时间
        teacher.leave_date = datetime.date.today()
        teacher.is_delete = 1
        teacher.save()
        resp.result = "success"
        resp.remark = "设置成功"
    else:
        resp.result = "failed"
        resp.remark = "已设置为离职状态，无需继续设置"

    return HttpResponse(json.dumps(resp.__dict__), content_type='application/json')


def admin_get_teacher(page_index):
    # 每页显示的条数
    # limit = 50
    # 获取所有的教师信息
    teachers = Teacher.objects.all();

    for t in teachers:
        if t.birthday != None:
            t.birthday = t.birthday.strftime("%Y-%m-%d")
        if t.entry_date != None:
            t.entry_date = t.entry_date.strftime("%Y-%m-%d")
        if t.leave_date != None:
            t.leave_date = t.leave_date.strftime("%Y-%m-%d")
        else:
            t.leave_date = ""

    # 数据总数
    total = teachers.count()
    paginator = Paginator(teachers, limit)
    # 获取当前页显示的内容
    curr_page = paginator.page(page_index)

    return (curr_page, limit, total)


@user_decorator.login
def admin_teacher_manager(request):
    page_index = request.GET['index']
    teachers = admin_get_teacher(page_index)

    context = {'teachers': teachers[0],
               'page_index': page_index,
               'limit': teachers[1],
               'total': teachers[2],
               'edu': get_edu(),
               'is_search': False,
               'english_level': get_english_level()
               }

    return render(request, 'admin-teacher.html', context)


@user_decorator.login
def admin_teacher_edit(request):
    teacher_id = request.GET['teacher_id']
    teacher_info = Teacher.objects.get(id=teacher_id)
    if teacher_info.entry_date != None:
        teacher_info.entry_date = teacher_info.entry_date.strftime('%Y-%m-%d')

    context = {'teacher_info': teacher_info,
               'edu': get_edu(),
               'english_level': get_english_level()
               }

    return render(request, "admin-teacher-edit.html", context)


@csrf_exempt
@user_decorator.login
def admin_teacher_edit_handle(request):
    teacher_info = json.loads(request.body, 'utf-8')
    teacher = Teacher.objects.get(id=teacher_info['teacher_id'])
    # print(teacher.name)
    teacher.name = teacher_info['teacher_name']
    teacher.gender = teacher_info['gender']
    teacher.entry_date = teacher_info['entrance_time']
    identity = teacher_info['identity']
    teacher.id_number = identity
    teacher.birthday = get_birthday(identity)
    teacher.phone = teacher_info['phone']
    teacher.edu = teacher_info['edu']
    teacher.english_level = teacher_info['english_level']
    teacher.remark = teacher_info['remark']

    if 0 == int(teacher_info['status']):
        teacher.leave_date = None
        teacher.is_delete = 0
    elif 1 == int(teacher_info['status']):
        teacher.leave_date = datetime.date.today()
        teacher.is_delete = 1

    teacher.save()

    resp = Response()
    resp.status = 200
    resp.result = "success"

    return HttpResponse(json.dumps(resp.__dict__), content_type="application/json")


def get_search_teachers_params(request):
    search_params = {}
    for key in request.GET.keys():
        value = request.GET[key]
        if key == 'type' or key == 'is_search' or key == 'index':
            continue
        if value.strip():
            if key == 'id' or key == 'is_delete':
                search_params[key] = value
            elif key == 'is_delete' and value != '':
                search_params[key] = value
            else:
                search_params[key + "__contains"] = value

    return search_params


@user_decorator.login
def admin_search_teacher(request):
    '''
    教师信息检索
    :param request:
    :return:
    '''
    search_params = get_search_teachers_params(request)
    print(search_params)

    teachers = Teacher.objects.all().filter(**search_params)

    if 'is_delete' in search_params.keys():
        search_params['is_delete'] = int(search_params['is_delete'])

    # print(teachers.count())
    context = {'teachers': teachers,
               'total': teachers.count(),
               'edu': get_edu(),
               'is_search': True,
               'search_params': search_params,
               'english_level': get_english_level()
               }

    for t in teachers:
        t.birthday = t.birthday.strftime("%Y-%m-%d")
        t.entry_date = t.entry_date.strftime("%Y-%m-%d")
        if t.leave_date != None:
            t.leave_date = t.leave_date.strftime("%Y-%m-%d")
        else:
            t.leave_date = ""

    # print(search_params)

    return render(request, 'admin-teacher.html', context)


# ********************** 教师管理 **********************

# ********************** 班次管理 **********************

@user_decorator.login
def admin_add_course(request):
    classrooms = Classroom.objects.all()
    teachers = Teacher.objects.all().filter(leave_date=None)

    context = {'classrooms': classrooms,
               'teachers': teachers,
               'season': get_season()
               }

    return render(request, 'admin-course-add.html', context)


@csrf_exempt
@user_decorator.login
def admin_add_course_handle(request):
    """
    添加一个班次信息
    :param request:
    :return:
    """

    course_info = json.loads(request.body, 'utf-8')

    teacher = Teacher.objects.get(id=course_info['teacher_id'])

    course = Course()

    course_name = course_info['course_year'] + \
                  course_info['course_season'] + \
                  teacher.name + course_info['course_name']

    course.name = course_name
    course.class_field_id = course_info['class_id']
    course.time = course_info['course_time']
    course.teacher_id = course_info['teacher_id']
    course.remark = course_info['remark']
    course.is_delete = 0

    course.save()

    resp = Response()
    resp.status = 200
    resp.result = 'success'

    return HttpResponse(json.dumps(resp.__dict__), content_type='application/json')


def admin_course_edit(request, course_id):
    course = Course.objects.get(id=course_id)
    classrooms = Classroom.objects.all()
    teachers = Teacher.objects.all().filter(leave_date=None)

    context = {'classrooms': classrooms,
               'teachers': teachers,
               'course': course
               }

    return render(request, 'admin-course-edit.html', context)


@csrf_exempt
def admin_course_edit_handle(request):
    """
    编辑一个班次信息
    :param request:
    :return:
    """
    course_info = json.loads(request.body)
    course = Course.objects.get(id=course_info['course_id'])
    course.name = course_info['course_name']
    course.teacher_id = course_info['teacher_id']
    course.class_field_id = course_info['class_id']
    course.time = course_info['course_time']
    course.remark = course_info['remark']
    course.save()

    resp = Response()
    resp.status = 200
    resp.result = 'success'

    return HttpResponse(json.dumps(resp.__dict__), content_type="application/json")


@user_decorator.login
def admin_course_del(request):
    """
    删除一个班次
    :param request:
    :param course_id:
    :return:
    """

    course_id = request.GET['course_id']
    course = Course.objects.get(id=course_id)
    course.is_delete = 1
    course.save()
    resp = Response()
    resp.status = 200
    resp.result = "success"
    return HttpResponse(json.dumps(resp.__dict__), content_type='application/json')


@csrf_exempt
@user_decorator.login
def admin_courses_del(request):
    """
    批量删除
    :param request:
    :return:
    """
    del_list = json.loads(request.body)

    # 批量删除
    for course_id in del_list:
        course = Course.objects.get(id=course_id)
        course.is_delete = 1
        course.save()

    resp = Response();
    resp.status = 200
    resp.result = 'success'

    resp_json = json.dumps(resp.__dict__)
    return HttpResponse(resp_json, 'application/json')


def get_courses_page(index):
    """
    获取下标对应页的班次信息
    :param index:
    :return:
    """
    courses = Course.objects.all().filter(is_delete=0).filter(id__gt=7).order_by('-id')
    paginator = Paginator(courses, limit)
    page = paginator.page(index)
    return (page, limit, courses)


@user_decorator.login
def admin_course_manager(request):
    """
    分页显示班次信息
    :param request:
    :param index:
    :return:
    """

    index = request.GET['index']
    courses_info = get_courses_page(index)
    classrooms = Classroom.objects.all().filter(is_delete=0)
    teachers = Teacher.objects.all().filter(is_delete=0)

    context = {'courses': courses_info[0],
               'choice_courses': get_courses(),
               'limit': courses_info[1],
               'index': index,
               'total': len(courses_info[2]),
               'classrooms': classrooms,
               'teachers': teachers,
               'is_search': False

               }

    return render(request, 'admin-course.html', context)


def get_search_courses_params(request):
    '''
    对搜索传递的参数的key进行处理
    :param request:
    :return:
    '''
    # 班次号精确查询
    # 班次名精确查询
    # 上课时间模糊查询
    # 上课教室精确查询

    search_params = {}
    for key in request.GET.keys():
        value = request.GET[key]
        if value.strip():
            # 用于过滤打印时上传的参数
            if key == 'type' or key == 'is_search' or key == 'is_new' or key == 'index':
                continue
            if key == 'id':
                search_params[key] = request.GET[key]
            else:
                search_params[key + "__contains"] = request.GET[key]

    return search_params


@user_decorator.login
def admin_search_courses(request):
    """
    班次信息检索
    :param request:
    :return:
    """
    search_params = get_search_courses_params(request)
    page = Course.objects.all().filter(**search_params).filter(id__gt=1)
    classrooms = Classroom.objects.all().filter(is_delete=0)
    teachers = Teacher.objects.all().filter(is_delete=0)
    context = {'courses': page,
               'choice_courses': get_courses(),
               'total': len(page),
               'classrooms': classrooms,
               'teachers': teachers,
               'search_params': search_params,
               'is_search': True

               }

    return render(request, 'admin-course.html', context)


# ********************** 班次管理 **********************


# ********************** 校区管理 **********************

@user_decorator.login
def admin_classroom_manager(request):
    """
    分页浏览班级信息
    :param request:
    :return:
    """
    index = request.GET['index']
    classrooms = Classroom.objects.all().filter(is_delete=0)
    paginator = Paginator(classrooms, limit)
    page = paginator.page(index)
    schools = School.objects.all().filter(is_delete=0)

    context = {'courses': page,
               'limit': limit,
               'index': index,
               'total': len(classrooms),
               'classrooms': page,
               'schools': schools,
               'is_search': False
               }

    return render(request, 'admin-classroom.html', context)


@csrf_exempt
@user_decorator.login
def admin_add_classroom(request):
    """
    添加一个新的教室
    :param request:
    :return:
    """
    classroom_info = json.loads(request.body, 'utf-8')

    classroom = Classroom()
    classroom.name = classroom_info['class_name']
    classroom.places = classroom_info['places']
    classroom.school_id = classroom_info['school_id']
    classroom.remark = classroom_info['remark']
    classroom.is_delete = 0
    classroom.save()

    resp = Response()
    resp.status = 200
    resp.result = 'success'

    return HttpResponse(json.dumps(resp.__dict__), content_type='application/json')


def get_search_classroom_params(request):
    '''
    对搜索传递的参数的key进行处理
    :param request:
    :return:
    '''
    # 班次号精确查询
    # 班次名精确查询
    # 上课时间模糊查询
    # 上课教室精确查询

    search_params = {}
    for key in request.GET.keys():

        value = request.GET[key]
        if value.strip():
            if key == 'school_id':
                search_params[key] = request.GET[key]
            else:
                search_params[key + "__contains"] = request.GET[key]

        search_params['is_delete'] = 0

    return search_params


@user_decorator.login
def admin_search_classroom(request):
    """
    教室的搜索
    :param request:
    :return:
    """
    search_params = get_search_classroom_params(request)

    print(search_params)

    classrooms = Classroom.objects.all().filter(**search_params)

    schools = School.objects.all().filter(is_delete=0)

    # 转型，避免前端页面接收数据进行比较时的类型不匹配
    if 'school_id' in search_params.keys():
        search_params['school_id'] = int(search_params['school_id'])

    context = {'classrooms': classrooms,
               'total': len(classrooms),
               'schools': schools,
               'search_params': search_params,
               'is_search': True
               }

    return render(request, "admin-classroom.html", context)


@user_decorator.login
def admin_edit_classroom(request):
    """
    编辑教室信息
    :param request:
    :param classroom_id:
    :return:
    """

    classroom_id = request.GET['classroom_id']
    classroom = Classroom.objects.get(id=classroom_id)
    school = School.objects.all().filter(is_delete=0)
    context = {'classroom': classroom,
               'schools': school
               }
    return render(request, 'admin-classroom-edit.html', context)


@user_decorator.login
def admin_classroom_del(request):
    classroom_id = request.GET['classroom_id']
    classroom = Classroom.objects.get(id=classroom_id)
    classroom.is_delete = 1
    classroom.save()
    resp = Response()
    resp.status = 200
    resp.result = "success"
    return HttpResponse(json.dumps(resp.__dict__), content_type='application/json')


@csrf_exempt
@user_decorator.login
def admin_del_classrooms(request):
    """
    批量删除
    :param request:
    :return:
    """
    del_list = json.loads(request.body)

    # 批量删除
    for classroom_id in del_list:
        classroom = Classroom.objects.get(id=classroom_id)
        classroom.is_delete = 1
        classroom.save()

    resp = Response();
    resp.status = 200
    resp.result = 'success'

    resp_json = json.dumps(resp.__dict__)
    return HttpResponse(resp_json, 'application/json')


@csrf_exempt
@user_decorator.login
def admin_edit_classroom_handle(request):
    classroom_info = json.loads(request.body)
    # {u'course_id': 1, u'remark': u'None', u'name': u'\u4e00\u53f7\u6559\u5ba4', u'places': u'40', u'school_id': u'1'}

    classroom = Classroom.objects.get(id=classroom_info['id'])

    classroom.name = classroom_info['name']
    classroom.places = classroom_info['places']
    classroom.school_id = classroom_info['school_id']
    classroom.remark = classroom_info['remark']

    classroom.save()

    resp = Response()
    resp.status = 200
    resp.result = 'success'

    return HttpResponse(json.dumps(resp.__dict__), content_type='application/json')


# 分页浏览校区信息
@user_decorator.login
def admin_campus_manager(request):
    """
    分页浏览校区信息
    :param request:
    :return:
    """

    index = request.GET['index']

    schools = School.objects.all().filter(is_delete=0)
    paginator = Paginator(schools, limit)
    page = paginator.page(index)
    context = {'schools': page,
               'limit': limit,
               'index': index,
               'total': len(schools),
               'classrooms': page,
               'is_local_school': False
               }

    return render(request, 'admin-campus.html', context)


def admin_school_manager(request):
    """
    分页浏览本地所有学校信息
    :param request:
    :return:
    """
    index = request.GET['index']
    schools = School.objects.all().filter(is_delete=2)
    paginator = Paginator(schools, limit)
    page = paginator.page(index)
    context = {'schools': page,
               'limit': limit,
               'index': index,
               'total': len(schools),
               'classrooms': page,
               'is_local_school': True
               }

    return render(request, 'admin-campus.html', context)


@csrf_exempt
def admin_school_add(request):
    """
    添加一个本地学校的信息
    :param request:
    :return:
    """
    school_info = json.loads(request.body, 'utf-8')

    if school_info['is_local_school'] == 'true':
        school = School()
        school.school_name = school_info['school_name']
        school.school_address = school_info['school_address']
        school.remark = school_info['remark']
        school.is_delete = 0
        school.save()

    elif school_info['is_local_school'] == 'false':

        school = School()
        school.school_name = school_info['school_name']
        school.school_address = school_info['school_address']
        school.remark = school_info['remark']
        school.is_delete = 2
        school.save()

    resp = Response()
    resp.status = 200
    resp.result = 'success'
    return HttpResponse(json.dumps(resp.__dict__), content_type='application/json')


def admin_school_edit(request):
    school_id = request.GET['school_id']
    school = School.objects.get(id=school_id)
    context = {'school': school}
    return render(request, 'admin-school-edit.html', context)


@csrf_exempt
def admin_school_edit_handle(request):
    school_info = json.loads(request.body)

    school = School.objects.get(id=school_info['id'])

    school.school_name = school_info['school_name']
    school.school_address = school_info['school_address']
    school.remark = school_info['remark']
    school.save()

    resp = Response()
    resp.status = 200
    resp.result = 'success'

    return HttpResponse(json.dumps(resp.__dict__), content_type='application/json')


def admin_school_del(request, school_id):
    school = School.objects.get(id=school_id)
    # print(school.school_name)
    school.is_delete = 1
    school.save()
    resp = Response()
    resp.status = 200
    resp.result = "success"
    return HttpResponse(json.dumps(resp.__dict__), content_type='application/json')


@csrf_exempt
def admin_schools_del(request):
    """
    批量删除
    :param request:
    :return:
    """
    del_list = json.loads(request.body)

    # 批量删除
    for school_id in del_list:
        school = School.objects.get(id=school_id)
        school.is_delete = 1
        school.save()

    resp = Response()
    resp.status = 200
    resp.result = 'success'

    resp_json = json.dumps(resp.__dict__)
    return HttpResponse(resp_json, 'application/json')


# ********************** 校区管理 **********************


# ********************** 表格生成 **********************

def create_teacher_table(teacher_id):
    teacher = Teacher.objects.get(id=teacher_id)

    # 格式化时间
    if teacher.entry_date!=None:
        teacher.entry_date = teacher.entry_date.strftime('%Y-%m-%d')
    if teacher.birthday!=None:
        teacher.birthday = teacher.birthday.strftime('%Y-%m-%d')
    if teacher.leave_date != None:
        teacher.leave_date = teacher.leave_date.strftime('%Y-%m-%d')

    """
    创建教师信息的表格
    :param context:
    :return:
    """

    # 创建工作簿
    wbk = xlwt.Workbook('utf-8')
    # 创建工作表
    sheet1 = wbk.add_sheet('Sheet1', cell_overwrite_ok=True)

    font = xlwt.Font()

    # 设置单元格中标题文字的显示样式
    style_title = xlwt.easyxf('font:height 420;')  # 36pt,类型小初的字号
    alignment_title = xlwt.Alignment()  # Create Alignment
    alignment_title.horz = xlwt.Alignment.HORZ_CENTER  # May be: HORZ_GENERAL, HORZ_LEFT, HORZ_CENTER, HORZ_RIGHT, HORZ_FILLED, HORZ_JUSTIFIED, HORZ_CENTER_ACROSS_SEL, HORZ_DISTRIBUTED
    style_title.alignment = alignment_title
    # 设置第二列和第四列的宽度

    # 设置单元格的宽度
    for i in xrange(0, 6):
        if i % 2 == 0:
            sheet1.col(i).width = 256 * 15
        else:
            sheet1.col(i).width = 256 * 20

    # 标题
    sheet1.write_merge(0, 0, 0, 4, '名佳英语教师信息表', style_title)
    # 设置正文文本再单元格中的显示样式
    style_content = xlwt.easyxf('font:height 280;')
    alignment_content = xlwt.Alignment()
    alignment_content.horz = xlwt.Alignment.WRAP_AT_RIGHT
    style_content.alignment = alignment_content
    borders = xlwt.Borders()
    borders.top = xlwt.Borders.DOUBLE
    borders.top_colour = 0x40
    style_border = xlwt.XFStyle()
    style_border.borders = borders
    startLine = 3
    for i in xrange(0, 5):
        sheet1.write(startLine + 1, i, "", style_border)

    sheet1.write(startLine + 2, 0, '打印时间:', style_content)

    sheet1.write(startLine + 2, 1, get_current_time(), style_content)

    sheet1.write(startLine + 4, 0, '员工号:', style_content)

    sheet1.write(startLine + 4, 1, teacher.id, style_content)

    sheet1.write(startLine + 4, 2, '姓名:', style_content)

    sheet1.write(startLine + 4, 3, teacher.name, style_content)

    sheet1.write(startLine + 6, 0, '性别:', style_content)

    sheet1.write(startLine + 6, 1, teacher.gender, style_content)

    sheet1.write(startLine + 6, 2, '出生日期:', style_content)

    sheet1.write(startLine + 6, 3, teacher.birthday, style_content)

    sheet1.write(startLine + 8, 0, '身份证号码:', style_content)

    sheet1.write(startLine + 8, 1, teacher.id_number, style_content)

    sheet1.write(startLine + 10, 0, '学历:', style_content)
    sheet1.write(startLine + 10, 1, teacher.edu, style_content)

    sheet1.write(startLine + 10, 2, '英语水平:', style_content)

    sheet1.write(startLine + 10, 3, teacher.english_level, style_content)

    sheet1.write(startLine + 12, 0, '入职时间:', style_content)

    sheet1.write(startLine + 12, 1, teacher.entry_date, style_content)

    if teacher.leave_date != None:
        sheet1.write(startLine + 12, 2, '离职时间:', style_content)
        sheet1.write(startLine + 12, 3, teacher.leave_date, style_content)

    sheet1.write(startLine + 14, 0, '备注:', style_content)
    sheet1.write(startLine + 14, 1, teacher.remark, style_content)

    table_name = str(time.time()) + teacher.name + ".xls"

    wbk.save('mingjia_admin/file/' + table_name)

    return table_name


def create_course_table(id):
    """
    创建班次报表
    :param id:
    :return:
    """

    course = Course.objects.get(id=id)

    """
       创建学生信息的表格
       :param context:
       :return:
       """

    # 创建工作簿
    wbk = xlwt.Workbook('utf-8')
    # 创建工作表
    sheet1 = wbk.add_sheet('Sheet1', cell_overwrite_ok=True)

    font = xlwt.Font()

    # 设置单元格中标题文字的显示样式
    style_title = xlwt.easyxf('font:height 420;')  # 36pt,类型小初的字号
    alignment_title = xlwt.Alignment()  # Create Alignment
    alignment_title.horz = xlwt.Alignment.HORZ_CENTER  # May be: HORZ_GENERAL, HORZ_LEFT, HORZ_CENTER, HORZ_RIGHT, HORZ_FILLED, HORZ_JUSTIFIED, HORZ_CENTER_ACROSS_SEL, HORZ_DISTRIBUTED
    style_title.alignment = alignment_title
    # 设置第二列和第四列的宽度

    # 设置单元格的宽度
    for i in xrange(0, 6):
        if i % 2 == 0:
            sheet1.col(i).width = 256 * 15
        else:
            sheet1.col(i).width = 256 * 20

    # 标题
    sheet1.write_merge(0, 0, 0, 4, '名佳英语班次信息表', style_title)
    # 设置正文文本再单元格中的显示样式
    style_content = xlwt.easyxf('font:height 280;')
    alignment_content = xlwt.Alignment()
    alignment_content.horz = xlwt.Alignment.WRAP_AT_RIGHT
    style_content.alignment = alignment_content
    borders = xlwt.Borders()
    borders.top = xlwt.Borders.DOUBLE
    borders.top_colour = 0x40
    style_border = xlwt.XFStyle()
    style_border.borders = borders
    startLine = 1
    sheet1.write(startLine + 1, 0, '打印时间:', style_content)
    sheet1.write(startLine + 1, 1, get_current_time(), style_content)
    for i in xrange(0, 5):
        sheet1.write(startLine + 2, i, "", style_border)

    sheet1.write(startLine + 4, 0, '班次号:', style_content)

    sheet1.write(startLine + 4, 1, course.id, style_content)

    sheet1.write(startLine + 4, 2, '班次名:', style_content)

    sheet1.write(startLine + 4, 3, course.name, style_content)

    sheet1.write(startLine + 6, 0, '上课时间:', style_content)

    sheet1.write(startLine + 6, 1, course.time, style_content)

    sheet1.write(startLine + 8, 0, '上课地点:', style_content)

    if course.class_field != None:
        sheet1.write(startLine + 8, 1, course.class_field.name + "-" + course.class_field.school.school_name,
                     style_content)

        sheet1.write(startLine + 10, 1, course.class_field.places, style_content)

    sheet1.write(startLine + 10, 0, '班次人数:', style_content)

    sheet1.write(startLine + 12, 0, '备注:', style_content)

    sheet1.write(startLine + 12, 1, course.remark, style_content)

    for i in xrange(0, 5):
        sheet1.write(startLine + 14, i, "", style_border)

        sheet1.write(startLine + 16, 0, '任课教师:', style_content)
        sheet1.write(startLine + 16, 1, course.teacher.name, style_content)

        sheet1.write(startLine + 18, 0, '联系方式:', style_content)
        sheet1.write(startLine + 18, 1, course.teacher.phone, style_content)

    table_name = str(time.time()) + course.name + ".xls"

    wbk.save('mingjia_admin/file/' + table_name)

    return table_name


def admin_print(request, type, id):
    """
    生成报表
    :param request:
    :param type:
    :param is_single:
    :param id:
    :return:
    """
    # 生成报表前先清空之前已经存在的报表文件

    del_files('mingjia_admin/file')

    # type: # 打印的类型
    # is_single: 0->打印单个 1->打印多个
    # id: 要打印的学生/当前页面中显示的内容

    table_name = None

    if int(type) == 0:
        # 创建学员报表
        table_name = create_student_table(id)
    elif int(type) == 1:
        # 创建教师报表
        table_name = create_teacher_table(id)
    elif int(type) == 2:
        # 创建班次报表
        table_name = create_course_table(id)

    context = {'table_name': table_name}
    return render(request, 'admin-print.html', context)


def create_teachers_table(teachers):
    """
    批量创建教师信息表
    :param teachers:
    :return:
    """
    wbk = xlwt.Workbook('utf-8')
    sheet1 = wbk.add_sheet('Sheet1', cell_overwrite_ok=True)

    header = ['员工号', '姓名', '性别', '身份证', '电话', '学历', '英语水平']

    # 设置表格单元格的宽度
    sheet1.col(0).width = 256 * 8
    sheet1.col(1).width = 256 * 14
    sheet1.col(2).width = 256 * 8
    sheet1.col(3).width = 256 * 20
    sheet1.col(4).width = 256 * 15
    sheet1.col(5).width = 256 * 15
    sheet1.col(6).width = 256 * 14

    style_title = xlwt.easyxf('font:height 220;')  # 36pt,类型小初的字号
    alignment_title = xlwt.Alignment()  # Create Alignment
    alignment_title.horz = xlwt.Alignment.HORZ_CENTER  # May be: HORZ_GENERAL, HORZ_LEFT, HORZ_CENTER, HORZ_RIGHT, HORZ_FILLED, HORZ_JUSTIFIED, HORZ_CENTER_ACROSS_SEL, HORZ_DISTRIBUTED
    style_title.alignment = alignment_title

    # 设置表头文字
    for i in xrange(header.__len__()):
        sheet1.write(0, i, header[i], style_title)

    line = 2
    for t in teachers:
        sheet1.write(line, 0, t.id, style_title)
        sheet1.write(line, 1, t.name, style_title)
        sheet1.write(line, 2, t.gender, style_title)
        sheet1.write(line, 3, t.id_number, style_title)
        sheet1.write(line, 4, t.phone, style_title)
        sheet1.write(line, 5, t.edu, style_title)
        sheet1.write(line, 6, t.english_level, style_title)
        line += 1

    table_name = str(time.time()) + "- 教师信息表.xls"

    wbk.save('mingjia_admin/file/' + table_name)

    return table_name


def create_courses_table(coureses):
    """
    批量打印班次信息
    :param courese:
    :return:
    """

    """
      批量创建教师信息表
      :param teachers:
      :return:
      """
    wbk = xlwt.Workbook('utf-8')
    sheet1 = wbk.add_sheet('Sheet1', cell_overwrite_ok=True)

    header = ['班次号', '班次名', '任课教师', '上课时间', '上课教室']

    # 设置表格单元格的宽度
    sheet1.col(0).width = 256 * 8
    sheet1.col(1).width = 256 * 30
    sheet1.col(2).width = 256 * 12
    sheet1.col(3).width = 256 * 25
    sheet1.col(4).width = 256 * 18

    style_title = xlwt.easyxf('font:height 220;')  # 36pt,类型小初的字号
    alignment_title = xlwt.Alignment()  # Create Alignment
    alignment_title.horz = xlwt.Alignment.HORZ_CENTER  # May be: HORZ_GENERAL, HORZ_LEFT, HORZ_CENTER, HORZ_RIGHT, HORZ_FILLED, HORZ_JUSTIFIED, HORZ_CENTER_ACROSS_SEL, HORZ_DISTRIBUTED
    style_title.alignment = alignment_title

    # 设置表头文字
    for i in xrange(header.__len__()):
        sheet1.write(0, i, header[i], style_title)

    line = 2
    for c in coureses:
        sheet1.write(line, 0, c.id, style_title)
        sheet1.write(line, 1, c.name, style_title)
        sheet1.write(line, 2, c.teacher.name, style_title)
        sheet1.write(line, 3, c.time, style_title)
        if c.class_field != None:
            sheet1.write(line, 4, c.class_field.name + "-" + c.class_field.school.school_name, style_title)

        line += 1

    table_name = str(time.time()) + "- 班次信息表.xls"

    wbk.save('mingjia_admin/file/' + table_name)

    return table_name


def admin_print_more(request):
    # {u'index': [u''], u'remark': [u''], u'name': [u''], u'is_search': [u'True'], u'school_name': [u''],
    #  u'phone': [u'1'], u'course_id': [u'2'], u'type': [u'0']}

    # 生成报表前先清空之前已经存在的报表文件
    del_files('mingjia_admin/file')
    context = {}

    # type -> 0 -> 学员
    if int(request.GET['type']) == 0:
        if request.GET['is_search'] == 'False':
            page_index = request.GET['index']
            is_new = request.GET['is_new']

            # 根据当前显示的页来查询学生信息
            students = admin_get_student(page_index, is_new)[1]

            table_name = create_students_table(students)
            context = {'table_name': table_name}
        # 根据搜索的结果生成报表
        else:
            search_params = admin_get_search_stus_params(request)
            students = Student.objects.filter(**search_params)
            for s in students:
                s.register_date = s.register_date.strftime("%Y-%m-%d")
            table_name = create_students_table(students)
            context = {'table_name': table_name}

    # type -> 1 -> 教师
    elif int(request.GET['type']) == 1:
        if request.GET['is_search'] == 'False':
            page_index = request.GET['index']
            teachers = admin_get_teacher(page_index)[0]
            table_name = create_teachers_table(teachers)
            context = {'table_name': table_name}
        else:
            search_params = get_search_teachers_params(request)
            teachers = Teacher.objects.all().filter(**search_params)
            table_name = create_teachers_table(teachers)
            context = {'table_name': table_name}
    # type -> 2 -> 班次
    elif int(request.GET['type']) == 2:
        if request.GET['is_search'] == 'False':
            page_index = int(request.GET['index'])
            courses = get_courses_page(page_index)[0]
            table_name = create_courses_table(courses)
            context = {'table_name': table_name}

        else:
            search_params = get_search_courses_params(request)
            courses = Course.objects.all().filter(**search_params).filter(id__gt=1)
            table_name = create_courses_table(courses)

    return render(request, 'admin-print.html', context)


def create_students_table(students):
    wbk = xlwt.Workbook('utf-8')
    sheet1 = wbk.add_sheet('Sheet1', cell_overwrite_ok=True)

    header = ['学号', '姓名', '性别', '班次', '电话', '就读小学', '年级']

    # 设置表格单元格的宽度
    sheet1.col(0).width = 256 * 8
    sheet1.col(1).width = 256 * 14
    sheet1.col(2).width = 256 * 8
    sheet1.col(3).width = 256 * 30
    sheet1.col(4).width = 256 * 15
    sheet1.col(5).width = 256 * 15
    sheet1.col(6).width = 256 * 8

    style_title = xlwt.easyxf('font:height 220;')  # 36pt,类型小初的字号
    alignment_title = xlwt.Alignment()  # Create Alignment
    alignment_title.horz = xlwt.Alignment.HORZ_CENTER  # May be: HORZ_GENERAL, HORZ_LEFT, HORZ_CENTER, HORZ_RIGHT, HORZ_FILLED, HORZ_JUSTIFIED, HORZ_CENTER_ACROSS_SEL, HORZ_DISTRIBUTED
    style_title.alignment = alignment_title

    # 设置表头文字
    for i in xrange(header.__len__()):
        sheet1.write(0, i, header[i], style_title)

    line = 2
    for s in students:
        sheet1.write(line, 0, s.id, style_title)
        sheet1.write(line, 1, s.name, style_title)
        sheet1.write(line, 2, s.gender, style_title)
        sheet1.write(line, 3, s.course.name, style_title)
        sheet1.write(line, 4, s.phone, style_title)
        sheet1.write(line, 5, s.school.school_name, style_title)
        # 当前学生所在的年级需要单独计算
        sheet1.write(line, 6, '3', style_title)
        line += 1

    table_name = str(time.time()) + ".xls"

    wbk.save('mingjia_admin/file/' + table_name)

    return table_name


def create_student_table(id):
    student = Student.objects.get(id=id)
    """
    创建学生信息的表格
    :param context:
    :return:
    """

    # 创建工作簿
    wbk = xlwt.Workbook('utf-8')
    # 创建工作表
    sheet1 = wbk.add_sheet('Sheet1', cell_overwrite_ok=True)

    font = xlwt.Font()

    # 设置单元格中标题文字的显示样式
    style_title = xlwt.easyxf('font:height 420;')  # 36pt,类型小初的字号
    alignment_title = xlwt.Alignment()  # Create Alignment
    alignment_title.horz = xlwt.Alignment.HORZ_CENTER  # May be: HORZ_GENERAL, HORZ_LEFT, HORZ_CENTER, HORZ_RIGHT, HORZ_FILLED, HORZ_JUSTIFIED, HORZ_CENTER_ACROSS_SEL, HORZ_DISTRIBUTED
    style_title.alignment = alignment_title
    # 设置第二列和第四列的宽度

    # 设置单元格的宽度
    for i in xrange(0, 6):

        if i % 2 == 0:
            sheet1.col(i).width = 256 * 15
        else:
            sheet1.col(i).width = 256 * 20

    # 标题
    sheet1.write_merge(0, 0, 0, 4, '名佳英语学员信息表', style_title)
    # 设置正文文本再单元格中的显示样式
    style_content = xlwt.easyxf('font:height 280;')
    alignment_content = xlwt.Alignment()
    alignment_content.horz = xlwt.Alignment.WRAP_AT_RIGHT
    style_content.alignment = alignment_content
    borders = xlwt.Borders()
    borders.top = xlwt.Borders.DOUBLE
    borders.top_colour = 0x40
    style_border = xlwt.XFStyle()
    style_border.borders = borders
    startLine = 3
    for i in xrange(0, 5):
        sheet1.write(startLine + 1, i, "", style_border)

    sheet1.write(startLine + 2, 0, '打印时间:', style_content)

    sheet1.write(startLine + 2, 1, get_current_time(), style_content)

    sheet1.write(startLine + 4, 0, '学号:', style_content)

    sheet1.write(startLine + 4, 1, student.id, style_content)

    sheet1.write(startLine + 4, 2, '姓名:', style_content)

    sheet1.write(startLine + 4, 3, student.name, style_content)

    sheet1.write(startLine + 6, 0, '性别:', style_content)

    sheet1.write(startLine + 6, 1, student.gender, style_content)

    sheet1.write(startLine + 6, 2, '学校:', style_content)

    sheet1.write(startLine + 6, 3, student.school.school_name, style_content)

    sheet1.write(startLine + 8, 0, '入校时间:', style_content)

    sheet1.write(startLine + 8, 1, student.entrance_time.strftime('"%Y-%m-%d"'), style_content)

    sheet1.write(startLine + 8, 2, '年级:', style_content)
    sheet1.write(startLine + 8, 3, student.temp_class, style_content)

    sheet1.write(startLine + 10, 0, '班级:', style_content)

    sheet1.write(startLine + 10, 1, student.grade, style_content)

    sheet1.write(startLine + 10, 2, '联系电话:', style_content)

    sheet1.write(startLine + 10, 3, student.phone, style_content)

    sheet1.write(startLine + 12, 0, '备注:', style_content)

    sheet1.write(startLine + 12, 1, student.remark, style_content)

    for i in xrange(0, 5):
        sheet1.write(startLine + 14, i, "", style_border)

    if student.course.name == '暂无安排':
        sheet1.write(startLine + 17, 0, '所在班次:', style_content)
        sheet1.write(startLine + 17, 1, '暂无安排', style_content)
    else:
        sheet1.write(startLine + 17, 0, '所在班次:', style_content)
        sheet1.write(startLine + 17, 1, student.course.name, style_content)

        sheet1.write(startLine + 19, 0, '任课教师:', style_content)
        sheet1.write(startLine + 19, 1, student.course.teacher.name, style_content)

        sheet1.write(startLine + 21, 0, '教师电话:', style_content)

        sheet1.write(startLine + 21, 1, student.course.teacher.phone, style_content)

        sheet1.write(startLine + 23, 0, '上课地点:', style_content)

        if student.course.class_field != None:
            sheet1.write(startLine + 23, 1,
                         student.course.class_field.name + "--" + student.course.class_field.school.school_name,
                         style_content)

        sheet1.write(startLine + 25, 0, '班次时间:', style_content)
        sheet1.write(startLine + 25, 1, student.course.time, style_content)

        sheet1.write(startLine + 27, 0, '报名时间:', style_content)
        sheet1.write(startLine + 27, 1, student.register_date, style_content)

        sheet1.write(startLine + 29, 0, '班次备注:', style_content)
        sheet1.write(startLine + 29, 1, student.course.remark, style_content)

    table_name = str(time.time()) + student.name + ".xls"

    wbk.save('mingjia_admin/file/' + table_name)

    return table_name


# ********************** 表格生成 **********************


# ********************** 工具类 **********************

def get_season():
    return ['春季', '暑假', '秋季', '寒假']


def get_edu():
    return ['初中', '高中', '大专', '本科', '硕士研究生', '博士研究生']


def get_english_level():
    return ['英语四级', '英语六级', '专业四级', '专业八级']


def get_current_time():
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))


def del_files(parent):
    """
    删除指定目录下的所有文件
    :param parent: 父目录
    :return:
    """
    path_dirs = os.listdir(parent)
    if path_dirs.__len__() > 0:
        for f in path_dirs:
            os.remove(parent + "/" + f)


def backup_db(username, password, db_name):
    """
    数据库备份，将数据库转储为sql脚本
    :param uname:
    :param pwd:
    :param db_name:
    :return:
    """
    # 在当前项目下创建存储备份文件的文件夹
    curr_path = os.getcwd()
    backup_path = 'mingjia_admin/file/'
    if not os.path.exists(backup_path):
        os.mkdir(backup_path)

    str_cmd = 'mysqldump -u' + username + ' -p' + password + " " + db_name + ' > ' + backup_path + '/mingjia_backup.sql'
    # 转储sql
    os.system(str_cmd)

    # 将sql脚本的路径返回
    return 'mingjia_backup.sql'


def admin_backup(request):
    del_files('mingjia_admin/file')
    db_name = backup_db('root', 'wangke0310', 'mingjia')
    context = {'db_name': db_name}
    return render(request, 'admin-backup.html', context=context)


def admin_download(request, file_name):
    """
    文件下载
    :param request:
    :return:
    """

    def file_iterator(file_name, chunk_size=512):
        # 需要加上‘rb’,负责下载的文件将是乱码
        with open(file_name, 'rb') as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break

    the_file_name = "mingjia_admin/file/" + file_name
    response = StreamingHttpResponse(file_iterator(the_file_name))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(the_file_name)
    return response


def calculate_grade(entrance_time):
    """
    根据入学时间计算所在年级
    :param entrance_time:
    :return:
    """
    # 获取当前的日期
    todaty = datetime.date.today()
    curr_year = todaty.year
    curr_month = todaty.month
    curr_day = todaty.day

    # 获取入学日期
    year = entrance_time.year
    month = entrance_time.month
    day = entrance_time.day

    # 年级
    grade = curr_year - year

    if month > curr_month:
        pass
        # grade -= 1
    elif month < curr_month:
        grade += 1

    elif curr_month == month:
        if day <= curr_day:
            grade += 1
        elif day > curr_day:
            pass
            # grade -= 1

    return grade


def get_courses():
    '''
    从数据库中获取班次信息
    :return:
    '''
    return Course.objects.filter(is_delete=0).order_by('-id')


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


def importTeacher(request):
    curr_path = os.getcwd()

    excel_path = 'mingjia_admin/file/teachers.xlsx'
    workbook = xlrd.open_workbook(excel_path)

    #  ctype :  0 empty,1 string, 2 number, 3 date, 4 boolean, 5 error
    sheet = workbook.sheet_by_index(0)

    for x in xrange(1, sheet.nrows):
        teacher_id = int(sheet.cell_value(x, 0))
        teacher_name = sheet.cell_value(x, 1).encode('utf-8')
        teacher_remark = sheet.cell_value(x, 2).encode('utf-8')
        teacher = Teacher()
        teacher.name = teacher_name
        teacher.remark = teacher_remark
        teacher.is_delete = 0
        print(teacher_name)
        teacher.save()

    return HttpResponse('导入教师信息')


# def importCourse(request):
#     teacher_id_map = {7: 56, 35: 57, 36: 58, 37: 59, 38: 60, 39: 61, 40: 62, 41: 63, 42: 64, 43: 65, 44: 66, 45: 67,
#                       46: 68, 49: 69, 50: 70, 51: 71, 52: 72}
#
#     excel_path = 'mingjia_admin/file/courses.xlsx'
#     workbook = xlrd.open_workbook(excel_path)
#
#     #  ctype :  0 empty,1 string, 2 number, 3 date, 4 boolean, 5 error
#     sheet = workbook.sheet_by_index(0)
#     for x in xrange(1, sheet.nrows):
#         course_name = sheet.cell_value(x, 1).encode('utf-8')
#         teacher_id = teacher_id_map[int(sheet.cell_value(x, 2))]
#         course_time = sheet.cell_value(x, 3).encode('utf-8')
#         remark = sheet.cell_value(x, 5).encode('utf-8')
#
#         course = Course()
#         course.name = course_name
#         course.teacher_id = teacher_id
#         course.time = course_time
#         course.remark = remark
#         course.is_delete = 0
#         course.save()
#
#         print(course_name)
#         print (teacher_id)
#         print (course_time)
#         print (remark)
#     return HttpResponse("导入班次信息")


# def importCourse(request):
#     course_id_map = {};
#
#     excel_path = 'mingjia_admin/file/courses.xlsx'
#     workbook = xlrd.open_workbook(excel_path)
#
#     # 建立班次映射
#     sheet = workbook.sheet_by_index(0)
#     for x in xrange(1, sheet.nrows):
#         # key
#         course_id = int(sheet.cell_value(x, 0))
#         course_name = sheet.cell_value(x, 1).encode('utf-8')
#
#         course = Course.objects.get(name=course_name)
#
#         course_id_map[course_id] = int(course.id)
#
#         print(str(course_id) + "=>" + str(course.id))
#
#     excel_stu_path = 'mingjia_admin/file/students.xlsx'
#
#     workbook_stu = xlrd.open_workbook(excel_stu_path)
#     sheet_stu = workbook_stu.sheet_by_index(0)
#
#     schools = []
#
#     for x in xrange(1, sheet_stu.nrows):
#         student = Student()
#
#         stu_name = sheet_stu.cell_value(x, 1).encode('utf-8')
#         student.name = stu_name
#         print(stu_name)
#         stu_gender = sheet_stu.cell_value(x, 2).encode('utf-8')
#         student.gender = stu_gender
#         stu_school = sheet_stu.cell_value(x, 3).encode('utf-8')
#         school = School.objects.get(school_name=stu_school)
#
#         student.school_id = school.id
#
#         entranceTime = sheet_stu.cell_value(x, 4)
#
#         date_value = xlrd.xldate_as_tuple(entranceTime, workbook.datemode)
#         entranceTime_data = date(*date_value[:3])
#
#         student.entrance_time = entranceTime_data
#
#         stu_class = int(sheet_stu.cell_value(x, 5))
#
#         student.class_name = stu_class
#
#         stu_phone = int(sheet_stu.cell_value(x, 6))
#
#         student.phone = stu_phone
#         stu_remark = sheet_stu.cell_value(x, 7)
#
#         student.remark = stu_remark
#
#         course = sheet_stu.cell_value(x, 8)
#         print (type(course))
#         if course != "":
#             course_id = int(sheet_stu.cell_value(x, 8))
#
#         student.course_id = course_id_map[course_id]
#
#         student.is_delete = 0
#
#         student.save()
#
#
#
#     return HttpResponse("导入班次信息")


# ********************** 工具类 **********************


class Response:
    status = 200
    result = None
    remark = ''

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

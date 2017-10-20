# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals

import xlwt
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


# Create your views here.
@user_decorator.login
def test(request):
    cookie = request.COOKIES['username']
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
    response = HttpResponseRedirect(redirect_to='/user/')
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

    schools = School.objects.all().filter(is_delete=2)

    context = {'courses': courses,
               'schools': schools
               }
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
        # 这个班次总共可容纳的人数
        places = course.class_field.places
        print(places)
        # 当前人数
        curr_num = Student.objects.all().filter(course_id=course_id).count()
        print('当前人数-->', curr_num)
        if curr_num >= places:
            resp.remark = "注意！！！当前班次可容纳的总人数为: " + str(places) + "人, 当前的报名人数为: " + str(curr_num) + "人, 请注意是否继续报名!"

    return HttpResponse(json.dumps(resp.__dict__, encoding='utf-8'), content_type='application/json')


def admin_student_manager(request, page_index=1, is_new=1):
    """
    学员管理
    :param request:
    :param page_index:
    :param is_new: 1->新生 0-> 普通学员 用于标记是否是新生(班次为暂无安排的被标记为新生)
    :return:
    """
    print(is_new)
    limit = 20

    if is_new == '1':
        print('查询课程id为1')
        students = Student.objects.filter(is_delete=0).filter(course_id=1)
    else:
        students = Student.objects.filter(is_delete=0)
        print('查询所有的课程id')

    paginator = Paginator(students, limit)
    # 当前页面的内容
    page = paginator.page(int(page_index))
    for p in page:
        p.register_date = p.register_date.strftime("%Y-%m-%d")
    # 页面展示的范围
    page_range = paginator.page_range

    context = {'students': page,
               'courses': get_courses(),
               'limit': limit,
               'total': students.count(),
               'page_index': page_index,
               'page_range': page_range,
               'max_page': len(page_range),
               'is_new': int(is_new),
               'is_search': False}

    return render(request, 'admin-student.html', context=context)


def get_search_students_params(request):
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


def get_students(request, is_new=1):
    students = None
    # 搜索
    # if not page_index.strip() and len(request.GET.keys()) > 0:
    search_params = get_search_students_params(request)
    # search_params1 = {'course_id': 1, 'name__contains': '王', 'is_delete': 0}
    students = Student.objects.filter(**search_params)

    for s in students:
        s.register_date = s.register_date.strftime("%Y-%m-%d")

    if 'course_id' in search_params.keys():
        search_params['course_id'] = long(search_params['course_id'])

    context = {'students': students,
               'courses': get_courses(),
               'search_params': search_params,
               'total': students.count(),
               'is_new': int(is_new),
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


def admin_student_detail(request, student_id):
    """
    学生详情
    :param request:
    :param student_id:
    :return:
    """
    print(student_id)
    student = Student.objects.all().get(id=student_id)
    # 时间格式转化
    student.entrance_time = student.entrance_time.strftime("%Y-%m-%d")
    student.register_date = student.register_date.strftime("%Y-%m-%d")
    context = {'student_info': student}
    return render(request, 'admin-student-detail.html', context)


def admin_teacher_add(request):
    context = {'edu': get_edu(),
               'english_level': get_english_level()
               }
    return render(request, 'admin-teacher-add.html', context)


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


def admin_teacher_leave(request, teacher_id):
    teacher = Teacher.objects.get(id=teacher_id)
    print(teacher.name)

    resp = Response()
    resp.status = 200
    if teacher.leave_date == None:
        # 设置为离职状态，添加离职时间
        teacher.leave_date = datetime.date.today()
        teacher.save()
        resp.result = "success"
        resp.remark = "设置成功"
    else:
        resp.result = "failed"
        resp.remark = "已设置为离职状态，无需继续设置"

    return HttpResponse(json.dumps(resp.__dict__), content_type='application/json')


def admin_teacher_manager(request, page_index=1):
    # 每页显示的条数
    limit = 20
    # 获取所有的教师信息
    teachers = Teacher.objects.all()

    for t in teachers:
        t.birthday = t.birthday.strftime("%Y-%m-%d")
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

    context = {'teachers': curr_page,
               'page_index': page_index,
               'limit': limit,
               'total': total,
               'edu': get_edu(),
               'is_search': False,
               'english_level': get_english_level()
               }

    return render(request, 'admin-teacher.html', context)


def admin_teacher_edit(request, teacher_id):
    teacher_info = Teacher.objects.get(id=teacher_id)

    teacher_info.entry_date = teacher_info.entry_date.strftime('%Y-%m-%d')

    context = {'teacher_info': teacher_info,
               'edu': get_edu(),
               'english_level': get_english_level()
               }

    return render(request, "admin-teacher-edit.html", context)


@csrf_exempt
def admin_teacher_edit_handle(request):
    teacher_info = json.loads(request.body, 'utf-8')
    teacher = Teacher.objects.get(id=teacher_info['teacher_id'])
    print(teacher.name)
    teacher.name = teacher_info['teacher_name']
    teacher.gender = teacher_info['gender']
    teacher.entry_date = teacher_info['entrance_time']
    teacher.id_number = teacher_info['identity']
    teacher.phone = teacher_info['phone']
    teacher.edu = teacher_info['edu']
    teacher.english_level = teacher_info['english_level']
    teacher.remark = teacher_info['remark']

    teacher.save()

    resp = Response()
    resp.status = 200
    resp.result = "success"

    return HttpResponse(json.dumps(resp.__dict__), content_type="application/json")


def get_search_teachers_params(request):
    search_params = {}
    for key in request.GET.keys():
        value = request.GET[key]
        if value.strip():
            if key != 'id':
                search_params[key + "__contains"] = value
            else:
                search_params[key] = value
    return search_params


def get_teachers(request):
    '''
    教师信息检索
    :param request:
    :return:
    '''
    search_params = get_search_teachers_params(request)
    print(search_params)
    teachers = Teacher.objects.all().filter(**search_params)
    print(teachers.count())
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

    print(search_params)

    return render(request, 'admin-teacher.html', context)


def admin_add_course(request):
    classrooms = Classroom.objects.all()
    teachers = Teacher.objects.all()

    for t in teachers:
        print(t.name)

    context = {'classrooms': classrooms,
               'teachers': teachers,
               'season': get_season()
               }

    return render(request, 'admin-course-add.html', context)


@csrf_exempt
def admin_add_course_handle(request):
    print(request.body)

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

    course.save()

    resp = Response()
    resp.status = 200
    resp.result = 'success'

    return HttpResponse(json.dumps(resp.__dict__), content_type='application/json')


def admin_course_manager(request, index=1):
    limit = 3
    courses = Course.objects.all().filter(is_delete=0).filter(id__gt=1)
    print(courses.count())
    paginator = Paginator(courses, limit)
    page = paginator.page(index)
    classrooms = Classroom.objects.all().filter(is_delete=0)
    teachers = Teacher.objects.all().filter(is_delete=0)

    context = {'courses': page,
               'choice_courses': get_courses(),
               'limit': limit,
               'index': index,
               'total': len(courses),
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
            if key == 'id':
                search_params[key] = request.GET[key]
            else:
                search_params[key + "__contains"] = request.GET[key]

    return search_params


def admin_get_courses(request):
    """
    班次信息检索
    :param request:
    :return:
    """
    search_params = get_search_courses_params(request)
    print(search_params)
    # 不查询暂无安排的班次
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


def admin_classroom(request, index):
    """
    分页浏览班级信息
    :param request:
    :return:
    """
    print("index-->" + index)

    limit = 3
    classrooms = Classroom.objects.all().filter(is_delete=0)
    print(classrooms.count())
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
def admin_add_classroom(request):
    """
    添加一个新的教室
    :param request:
    :return:
    """
    print(request.body)
    # {"class_name": "banji", "school_id": "1", "places": "40", "remark": "de"}

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


def get_classroom(request):
    """
    教室的搜索
    :param request:
    :return:
    """
    search_params = get_search_classroom_params(request)

    classrooms = Classroom.objects.all().filter(**search_params)

    schools = School.objects.all().filter(is_delete=0)

    # 转型，避免前端页面接收数据进行比较时的类型不匹配
    search_params['school_id'] = int(search_params['school_id'])

    context = {'classrooms': classrooms,
               'total': len(classrooms),
               'schools': schools,
               'search_params': search_params,
               'is_search': True
               }

    return render(request, "admin-classroom.html", context)


def admin_campus(request, index):
    """
    分页浏览校区信息
    :param request:
    :return:
    """
    print("index-->" + index)

    limit = 20
    schools = School.objects.all().filter(is_delete=0)
    print(schools.count())
    paginator = Paginator(schools, limit)
    page = paginator.page(index)
    context = {'schools': page,
               'limit': limit,
               'index': index,
               'total': len(schools),
               'classrooms': page,
               }

    return render(request, 'admin-campus.html', context)


@csrf_exempt
def admin_add_campus(request):
    """
    添加一个校区信息
    :param request:
    :return:
    """
    print(request.body)

    school_info = json.loads(request.body, 'utf-8')

    school = School()
    school.school_name = school_info['school_name']
    school.school_address = school_info['school_address']
    school.remark = school_info['remark']
    school.is_delete = 0
    school.save()

    resp = Response()
    resp.status = 200
    resp.result = 'success'
    return HttpResponse(json.dumps(resp.__dict__), content_type='application/json')


def admin_school(request, index):
    """
    分页浏览本地所有学校信息
    :param request:
    :return:
    """
    print("index-->" + index)

    limit = 20
    schools = School.objects.all().filter(is_delete=2)
    print(schools.count())
    paginator = Paginator(schools, limit)
    page = paginator.page(index)
    context = {'schools': page,
               'limit': limit,
               'index': index,
               'total': len(schools),
               'classrooms': page,
               }

    return render(request, 'admin-campus.html', context)


@csrf_exempt
def admin_add_school(request):
    """
    添加一个本地学校的信息
    :param request:
    :return:
    """
    print(request.body)

    school_info = json.loads(request.body, 'utf-8')

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


def admin_download(request, file_name):
    """
    文件下载的方法
    :param request:
    :return:
    """

    def file_iterator(file_name, chunk_size=512):
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
            # {u'course_id': u'2', u'school_name__contains': u'\u51af', u'is_delete': 0}


def get_season():
    return ['春季', '夏季', '秋季', '冬季']


def get_edu():
    return ['初中', '高中', '大专', '本科', '硕士研究生', '博士研究生']


def get_english_level():
    return ['英语四级', '英语六级', '专业四级', '专业八级']


def get_current_time():
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))


def admin_print(request, type, is_single, id):
    """
    生成报表
    :param request:
    :param type:
    :param is_single:
    :param id:
    :return:
    """

    # type: # 打印的类型
    # is_single: 0->打印单个 1->打印多个
    # id: 要打印的学生/当前页面中显示的内容

    print(type)
    print(is_single)
    print(id)

    table_name = None

    if int(type) == 0:
        if int(is_single) == 1:
            # 创建学员报表
            table_name = create_student_table(id)

    context = {'table_name': table_name}
    return render(request, 'admin-print.html', context)


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
        print
        i
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

    sheet1.write(startLine + 6, 3, student.school_name, style_content)

    sheet1.write(startLine + 8, 0, '入校时间:', style_content)

    sheet1.write(startLine + 8, 1, student.entrance_time, style_content)

    sheet1.write(startLine + 8, 2, '年级:', style_content)
    sheet1.write(startLine + 8, 3, '3', style_content)

    sheet1.write(startLine + 10, 0, '班级:', style_content)

    sheet1.write(startLine + 10, 1, student.grade, style_content)

    sheet1.write(startLine + 10, 2, '联系电话:', style_content)

    sheet1.write(startLine + 10, 3, student.phone, style_content)

    sheet1.write(startLine + 12, 0, '备注:', style_content)

    sheet1.write(startLine + 12, 1, student.remark, style_content)


    print (student.course.name)




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
        sheet1.write(startLine + 23, 1,
                     student.course.class_field.name + "--" + student.course.class_field.school.school_name, style_content)

        sheet1.write(startLine + 25, 0, '班次时间:', style_content)
        sheet1.write(startLine + 25, 1, student.course.time, style_content)

        sheet1.write(startLine + 27, 0, '报名时间:', style_content)
        sheet1.write(startLine + 27, 1, student.register_date, style_content)

        sheet1.write(startLine + 29, 0, '班次备注:', style_content)
        sheet1.write(startLine + 29, 1, student.course.remark, style_content)

    table_name = str(time.time()) + student.name + ".xls"

    wbk.save('mingjia_admin/file/' + table_name)

    return table_name

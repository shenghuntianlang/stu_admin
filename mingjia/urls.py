"""mingjia URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from mingjia_admin import views

urlpatterns = [
    url(r'^$',views.index),
    url(r'^admin/', admin.site.urls),
    url(r'^admin_print/(\d+)/(\d+)$', views.admin_print),
    url(r'^admin_print_more/$', views.admin_print_more),
    url(r'^test/$', views.test),
    url(r'^index/$', views.index),
    url(r'^user/$', views.login),
    url(r'^login_handle/$', views.login_handle),
    url(r'^log_out/$', views.log_out),
    url(r'^index', views.index),


    url(r'^admin_add_stu/$', views.admin_add_stu),
    url(r'^admin_add_stu_handle/$', views.admin_add_stu_handle),
    url(r'^admin_stu_manager/$', views.admin_stu_manager),
    url(r'^admin_stu_edit/$', views.admin_stu_edit),
    url(r'^admin_stu_edit_handle/$', views.admin_stu_edit_handle),
    url(r'^admin_search_stu/$', views.admin_search_stu),
    url(r'^admin_del_stu/$', views.admin_del_stu),
    url(r'^admin_del_stus/$', views.admin_del_stus),
    url(r'^admin_stu_detail/', views.admin_stu_detail),



    url(r'^admin_teacher_add/$', views.admin_teacher_add),
    url(r'^admin_teacher_add_handle/$', views.admin_teacher_add_handle),
    url(r'^admin_teacher_manager/$', views.admin_teacher_manager),
    url(r'^admin_teacher_edit/$', views.admin_teacher_edit),
    url(r'^admin_teacher_edit_handle/$', views.admin_teacher_edit_handle),
    url(r'^admin_teacher_leave/$', views.admin_teacher_leave),
    url(r'^admin_search_teacher/$', views.admin_search_teacher),


    url(r'^admin_add_course/$', views.admin_add_course),
    url(r'^admin_course_add_handle/$', views.admin_add_course_handle),
    url(r'^admin_course_manager/$', views.admin_course_manager),
    url(r'^admin_course_edit/(\d+)$', views.admin_course_edit),
    url(r'^admin_course_edit_handle/$', views.admin_course_edit_handle),
    url(r'^admin_course_del/$', views.admin_course_del),
    url(r'^admin_courses_del/', views.admin_courses_del),


    url(r'^get_courses/$', views.admin_search_courses),
    url(r'^admin_classroom_manager/$', views.admin_classroom_manager),
    url(r'^admin_add_classroom/$', views.admin_add_classroom),
    url(r'^admin_search_classroom/$', views.admin_search_classroom),
    url(r'^admin_edit_classroom/$', views.admin_edit_classroom),
    url(r'^admin_edit_classroom_handle/$', views.admin_edit_classroom_handle),
    url(r'^admin_classroom_del/$', views.admin_classroom_del),
    url(r'^admin_del_classrooms/$', views.admin_del_classrooms),

    url(r'^admin_campus_manager/$', views.admin_campus_manager),
    url(r'^admin_school_manager/$', views.admin_school_manager),
    url(r'^admin_school_add/$', views.admin_school_add),
    url(r'^admin_school_edit/$', views.admin_school_edit),
    url(r'^admin_school_edit_handle/$', views.admin_school_edit_handle),
    url(r'^admin_school_del/(\d+)$', views.admin_school_del),
    url(r'^admin_schools_del/$', views.admin_schools_del),

    url(r'^admin_download/([\s\S]*)$', views.admin_download),
    url(r'^admin_backup/$', views.admin_backup),




]

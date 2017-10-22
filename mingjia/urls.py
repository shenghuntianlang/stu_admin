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
    url(r'^admin/', admin.site.urls),
    url(r'^admin_print/(\d+)/(\d+)$', views.admin_print),
    url(r'^admin_print_more/$', views.admin_print_more),
    url(r'^test/$', views.test),
    url(r'^index/$', views.index),
    url(r'^user/$', views.login),
    url(r'^login_handle/$', views.login_handle),
    url(r'^log_out/$', views.log_out),
    url(r'^index', views.index),
    url(r'^admin_add/$', views.admin_add),
    url(r'^admin_add_handle/$', views.admin_add_handle),
    url(r'^admin_student/(\d+)/(\d+)$', views.admin_student_manager),
    url(r'^admin_student_edit/(\d+)$', views.admin_student_edit),
    url(r'^admin_student_edit_handle/$', views.admin_student_edit_handle),
    url(r'^get_students/(\d+)$', views.get_students),
    url(r'^del_student/(\d+)$', views.del_student),
    url(r'^del_students/$', views.del_students),
    url(r'^admin_student_detail/(\d+)$', views.admin_student_detail),
    url(r'^admin_teacher_add/$', views.admin_teacher_add),
    url(r'^admin_teacher_add_handle/$', views.admin_teacher_add_handle),
    url(r'^admin_teacher_manager/(\d+)$', views.admin_teacher_manager),
    url(r'^admin_teacher_edit/(\d+)$', views.admin_teacher_edit),
    url(r'^admin_teacher_edit_handle/$', views.admin_teacher_edit_handle),
    url(r'^admin_teacher_leave/(\d+)$', views.admin_teacher_leave),
    url(r'^get_teachers/$', views.get_teachers),
    url(r'^admin_add_course/$', views.admin_add_course),
    url(r'^admin_course_add_handle/$', views.admin_add_course_handle),
    url(r'^admin_course_manager/(\d*)$', views.admin_course_manager),
    url(r'^admin_course_edit/(\d+)$', views.admin_course_edit),
    url(r'^admin_course_edit_handle/$', views.admin_course_edit_handle),
    url(r'^admin_course_del/(\d+)$',views.admin_course_del),
    url(r'^admin_del_courses/',views.admin_del_courses),

    url(r'^get_courses/$', views.admin_get_courses),
    url(r'^admin_classroom/(\d*)$', views.admin_classroom),
    url(r'^admin_add_classroom/$', views.admin_add_classroom),
    url(r'^get_classroom/$', views.get_classroom),
    url(r'^admin_campus/(\d*)$', views.admin_campus),
    url(r'^admin_add_campus/$', views.admin_add_campus),
    url(r'^admin_school/(\d*)$', views.admin_school),
    url(r'^admin_add_school/$', views.admin_add_school),
    url(r'^admin_download/([\s\S]*)$', views.admin_download)

]

from django.shortcuts import render
from django.shortcuts import redirect
from .models import Course, Teacher


def index(request):
    if not request.session.get('is_login', None):
        return redirect("/login/login/")
    course_list = Course.objects.order_by('cno')
    teacher_list = Teacher.objects.order_by("tno")
    ctx = {'course_list': course_list, 'teacher_list': teacher_list}
    return render(request, 'index.html', ctx)


def course_detail(request, course_cno):
    if not request.session.get('is_login', None):
        return redirect("/login/login/")
    course = Course.objects.get(pk=course_cno)
    ctx = {
        'course': course,
        'teachers': course.teacher_set.all()
    }
    return render(request, 'courses/detail.html', ctx)


def teacher_detail(request, teacher_tno):
    if not request.session.get('is_login', None):
        return redirect("/login/login/")
    teacher = Teacher.objects.get(pk=teacher_tno)
    ctx = {
        'teacher': teacher,
        'courses': teacher.course.all()
    }
    return render(request, 'teachers/detail.html', ctx)

from django.shortcuts import render
from django.shortcuts import redirect
from . import models


def index(request):
    if not request.session.get('is_login', None):
        return redirect("/login/login/")
    return render(request, 'index.html')


def courses_index(request):
    if not request.session.get('is_login', None):
        return redirect("/login/login/")
    return render(request, 'courses/index.html')


def teachers_index(request):
    if not request.session.get('is_login', None):
        return redirect("/login/login/")
    return render(request, 'teachers/index.html')

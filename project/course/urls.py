from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'course'
urlpatterns = [
    url(r'^$', views.index),
    path('course/<str:course_cno>/', views.course_detail),
    path('teacher/<str:teacher_tno>/', views.teacher_detail),
]

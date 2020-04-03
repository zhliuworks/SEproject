from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'course'
urlpatterns = [
    url(r'^$', views.index),
    path('courses/', views.courses_index),
    path('teachers/', views.teachers_index),
]

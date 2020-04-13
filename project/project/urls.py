from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from login import views

urlpatterns = [
    url(r'^$', views.login),
    path('admin/', admin.site.urls),
    path('login/', include('login.urls')),
    path('captcha/', include('captcha.urls')),
    path('about/', views.about),
    path('course/', include('course.urls')),
    path('bbs/', include('bbs.urls')),
    path('editnickname/',views.editnickname),
    path('editemail/',views.editemail),
    path('editpwd/', views.editpwd),
]

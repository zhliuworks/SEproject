from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.urls import re_path
from django.conf import settings
from django.views.static import serve
from login import views

urlpatterns = [
    url(r'^$', views.login),
    path('admin/', admin.site.urls),
    path('login/', include('login.urls')),
    path('captcha/', include('captcha.urls')),
    path('about/', views.about),
    path('course/', include('course.urls')),
    path('bbs/', include('bbs.urls')),
    path('editnickname/', views.editnickname),
    path('editemail/', views.editemail),
    path('editpwd/', views.editpwd),
    path('editphoto/', views.editphoto),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    url(r'^search/', include('haystack.urls')),
    path('info/<int:sno>', views.info, name='info'),
    path('likes/', views.likes),
    path('posts/', views.posts),
    path('comments/', views.comments),
    path('send/<int:sno>', views.send),
    path('mailbox/', views.mailbox),
    path('follow/<int:sno>', views.follow),
    path('follows/', views.follows),
    path('follow_cancel/<int:sno>', views.follow_cancel),
]

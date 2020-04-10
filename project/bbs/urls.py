from django.urls import path
from . import views

app_name = 'bbs'

urlpatterns = [
    path('', views.index),
    path('<int:post_id>', views.bbs_detail),
    path('edit/', views.post_edit_page),
    path('edit/action/', views.post_edit_page_action),
]
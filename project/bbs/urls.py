from django.urls import path
from . import views

app_name = 'bbs'

urlpatterns = [
    path('', views.index),
    path('<int:post_id>', views.bbs_detail, name='detail'),
    path('edit/<int:post_id>', views.post_edit_page),
    path('edit/action/', views.post_edit_page_action),
    path('like/<int:post_id>', views.like_post),
    path('comment/<int:post_id>', views.post_comment_page, name='comment'),
    path('comment/action/', views.post_comment_page_action),
    path('delete/<int:comment_id>', views.delete_comment),
]

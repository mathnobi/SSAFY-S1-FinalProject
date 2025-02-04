from django.urls import path
from . import views

app_name = 'articles'
urlpatterns = [
    path('', views.article_list, name='article_list'),
    path('<int:article_pk>/', views.article_detail, name='article_detail'),
    path('<int:article_pk>/comments/', views.comment_list_create, name='comment_list_create'),  # 댓글 목록 및 생성
    path('<int:article_pk>/comments/<int:comment_pk>/', views.comment_detail, name='comment_detail'),  # 댓글 수정, 삭제
]

from django.contrib import admin
from django.urls import path, include
from article import views

urlpatterns = [
    path('<article_id>/', views.ArticleView.as_view()),
    path('<article_id>/comment/', views.CommentView.as_view()),
]

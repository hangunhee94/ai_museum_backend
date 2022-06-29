from django.contrib import admin
from django.urls import path, include
from article import views

urlpatterns = [
    path('article/', views.ArticleView.as_view()),
]
from django.contrib import admin
from django.urls import path, include
from user import views

urlpatterns = [
    path('sign_up', views.UserView.as_view()),
    path('login/', views.LoginView.as_view()),
    path('logout/', views.LoginView.as_view()),
    path('test/', views.TestView.as_view()),
]

from django.urls import path
from . import views

urlpatterns = [
    path('Mission/', views.index),
    path('captcha/', views.captcha),
    path('login/', views.login),
]
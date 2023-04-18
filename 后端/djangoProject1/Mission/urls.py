from django.urls import path
from . import views

urlpatterns = [
    path('mission_create/', views.missioncreate),
    path('mission_get/', views.missionget),
]
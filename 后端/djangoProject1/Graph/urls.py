from django.urls import path
from . import views

urlpatterns = [
    path('graph_construct/', views.graphConstruction),
]
from django.urls import path
from . import views

urlpatterns = [
    path('project_create/', views.projectcreate),
    path('project_get/', views.projectget),
    path('project_edit/', views.projectedit),
    path('project_delete/', views.projectdelete),
    path('entity_create/', views.entitycreate),
    path('entity_get/', views.entityget),
    path('entity_edit/', views.entityedit),
    path('entity_delete/', views.entitydelete),
    path('file_upload/',views.datacreate),
    path('data_get/', views.dataget),
    path('rel_create/', views.relcreate),
    path('rel_edit/', views.reledit),
    path('rel_get/', views.relget),
    path('rel_delete/', views.reldelete)
]
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('team/', views.team),
    path('collection/', views.getCollection),
]

from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('geek/', views.geek, name='geek'),
    path('user/', views.user, name='user'),
    path('db_handle', views.db_handle, name='db_handle'),
]

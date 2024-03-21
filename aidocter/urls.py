from django.urls import path

from .views import views

urlpatterns = [
    
    #화면이동
    path('', views.index),
    path('view/<str:view_name>', views.view, name='view'),
    
    #action처리
    path('action/register', views.register, name='register'),
    path('action/login', views.login, name='login'),
]
from django.urls import path

from .views import view_views, action_views

urlpatterns = [
    
    #화면이동
    path('', view_views.index),
    path('view/login', view_views.login, name='view_login'),
    path('view/register', view_views.register, name='view_register'),
    path('view/chat', view_views.chat, name='view_chat'),
    
    #action처리
    path('action/login', action_views.login, name='action_login'),
    path('action/register', action_views.register, name='action_register'),
    path('action/logout', action_views.logout, name='action_logout'),
]
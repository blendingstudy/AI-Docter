from django.urls import path

from .views import actions, views

urlpatterns = [
    
    #화면이동
    path('', views.index),
    path('view/login', views.login, name='view_login'),
    path('view/register', views.register, name='view_register'),
    path('view/chat-list', views.chat_list, name='view_chat_list'),
    path('view/chat', views.chat, name='view_chat'),
    
    #action처리
    path('action/login', actions.login, name='action_login'),
    path('action/register', actions.register, name='action_register'),
    path('action/logout', actions.logout, name='action_logout'),
    path('action/chat-start', actions.chat_start, name='action_chat_start'),
]
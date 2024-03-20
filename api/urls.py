from django.urls import path

from .views import chat_views

urlpatterns = [
    path('chat/llm/', chat_views.chat_llm, name='chat_llm')
]
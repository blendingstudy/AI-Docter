from django.urls import path

from .views import chat

urlpatterns = [
    path('chat/llm/', chat.chat_llm, name='chat_llm')
]
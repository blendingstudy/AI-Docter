from django.urls import path

from .views import chat

urlpatterns = [
    path('chat/llm', chat.chat_llm, name='chat_llm'),
    path('chat/get-history', chat.get_chat_hisotry, name='chat_get_history')
]
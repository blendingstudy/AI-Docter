from django.urls import path

from .views import chat

urlpatterns = [
    path('chat/llm', chat.chat_llm, name='chat_llm'),
    path('chat/set-history', chat.set_chat_hisotry, name='chat_get_history'),
    path('chat/get-hospital', chat.get_hospital, name='chat_get_history'),
    path('chat/set-chroma', chat.set_chroma, name='set_chroma')
]
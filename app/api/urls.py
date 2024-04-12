from django.urls import path

from .views import chat

urlpatterns = [
    path('chat/llm', chat.chat_llm, name='chat_llm'),
    path('chat/set-history', chat.set_chat_history, name='chat_get_history'),
    path('chat/get-hospital', chat.get_hospital, name='get_hospital'),
    path('chat/get-disease', chat.get_disease, name='get_disease'),
    path('chat/set-chroma', chat.set_chroma, name='set_chroma'),


    path('chat/search/google', chat.search_google, name='search_google'),
    path('chat/search/naver', chat.search_naver, name='search_google')
]
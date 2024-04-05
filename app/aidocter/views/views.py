#기본경로 리다이렉트
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET

from app.aidocter.models.chat_list import ChatList

@require_GET
def index(request): 
    return redirect('view/login')

#화면 호출 메소드
@require_GET
def login(request):
    
    context: dict = {}
    message = request.GET.get('message')

    if message:
        context['message'] = message
    
    return render(request, 'login.html', context)

#화면 호출 메소드
@require_GET
def register(request):
    
    context: dict = {}
    message = request.GET.get('message')

    if message:
        context['message'] = message
    
    return render(request, 'register.html', context)

#화면 호출 메소드
@login_required
@require_GET
def chat_list(request):
    
    user = request.user
    context: dict = {}
    message = request.GET.get('message')

    if message:
        context['message'] = message
    
    context['chat_list'] = ChatList.objects.filter(username=user).order_by('-id')
    print(context)
    return render(request, 'chatList.html', context)

#화면 호출 메소드
@login_required
@require_GET
def chat(request):
    
    context: dict = {}
    message = request.GET.get('message')
    chat_list_id = request.GET.get('id')

    if message:
        context['message'] = message
        
    context['id'] = chat_list_id
    
    return render(request, 'chat.html', context)
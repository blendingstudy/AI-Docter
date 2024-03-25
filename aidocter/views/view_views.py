#기본경로 리다이렉트
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

def index(request): 
    return redirect('view/login')

#화면 호출 메소드
def login(request):
    
    context: dict = {}
    
    if request.method == 'GET':
    
        message = request.GET.get('message')

        if message:
            context['message'] = message
    
    return render(request, 'login.html', context)

#화면 호출 메소드
def register(request):
    
    context: dict = {}
    
    if request.method == 'GET':
    
        message = request.GET.get('message')

        if message:
            context['message'] = message
    
    return render(request, 'register.html', context)

#화면 호출 메소드
@login_required
def chat(request):
    
    context: dict = {}
    
    if request.method == 'GET':
    
        message = request.GET.get('message')

        if message:
            context['message'] = message
    
    return render(request, 'chat.html', context)
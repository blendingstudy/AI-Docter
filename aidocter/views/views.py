from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

from aidocter.models import User

#기본경로 리다이렉트
def index(request): 
    return redirect('view/login')

#화면 호출 메소드
def view(request, view_name):
    
    context: dict = {}
    
    if request.method == 'GET':
    
        message = request.GET.get('message')

        if message:
            context['message'] = message
    
    return render(request, f'{view_name}.html', context)

#회원가입
def register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        id = request.POST.get('id')
        pw = request.POST.get('pw')
        
        try:
            # 특정 id를 가진 멤버 조회
            member = User.objects.get(id=id)
            print("회원존재: "+str(member))
            # 이미 존재하는 아이디라면 실패 메시지를 표시하고 이전 페이지로 리다이렉트
            message = '회원존재: 아이디중복'
            return redirect(f'/view/register?message={message}') 
        except User.DoesNotExist:
            # 존재하지 않는 아이디라면 새로운 멤버 생성
            new_member = User.objects.create(id=id, pw=pw, name=name)
            print("회원생성: ", new_member)
            message = '회원가입 완료'
            # 회원가입이 성공했을 경우 로그인 페이지로 리다이렉트
            return redirect(f'/view/login?message={message}')  # login은 로그인 페이지의 URL 이름입니다.
    
    print("회원생성 실패")
    return render(request, 'login.html')

#로그인
def login(request):
    
    if request.method == 'POST':
        id = request.POST.get('id')
        pw = request.POST.get('pw')
        
        
        user = authenticate(id=id, pw=pw)
        
        if user is not None:
            print("로그인성공: "+str(user))
            
            login(request, user)
            
            # 이미 존재하는 아이디라면 실패 메시지를 표시하고 이전 페이지로 리다이렉트
            return redirect('/view/chat') 
        else:
            print("로그인실패: 회원없음")
            
            message = '로그인실패: 아이디 또는 비밀번호 확인'
            # 로그인 실패 메시지를 표시하고 이전 페이지로 리다이렉트
            return redirect(f'/view/login?message={message}') 
    
    print("로그인 실패")
    return redirect('/view/login') 


#로그아웃
def logout(request):
    
    logout(request)
        
    return render(request, '/view/login')
    
    


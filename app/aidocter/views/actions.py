from django.shortcuts import redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.views.decorators.http import require_POST, require_GET


#회원가입
@require_POST
def register(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    
    try:
        # 특정 id를 가진 멤버 조회
        member = User.objects.get(username=username)
        print("회원존재: "+str(member))
        # 이미 존재하는 아이디라면 실패 메시지를 표시하고 이전 페이지로 리다이렉트
        message = '회원존재: 아이디중복'
        return redirect(f'/view/register?message={message}') 
    except User.DoesNotExist:
        # 존재하지 않는 아이디라면 새로운 멤버 생성
        # new_member = User.objects.create(username=username, password=password)
        user = User(username=username)
        user.set_password(password)
        user.save()
        print("회원생성: ", user)
        message = '회원가입 완료'
        # 회원가입이 성공했을 경우 로그인 페이지로 리다이렉트
        return redirect(f'/view/login?message={message}')  # login은 로그인 페이지의 URL 이름입니다.

#로그인
@require_POST
def login(request):
    
    username = request.POST.get('username')
    password = request.POST.get('password')
    
    user = authenticate(username=username, password=password)
    print(user)
    
    if user is not None:
        print("로그인성공: "+str(user))
        
        auth_login(request, user)
        
        # 이미 존재하는 아이디라면 실패 메시지를 표시하고 이전 페이지로 리다이렉트
        return redirect('/view/chat-list') 
    else:
        print("로그인실패: 회원없음")
        
        message = '로그인실패: 아이디 또는 비밀번호 확인'
        # 로그인 실패 메시지를 표시하고 이전 페이지로 리다이렉트
        return redirect(f'/view/login?message={message}')  


#로그아웃
@require_GET
def logout(request):
    
    auth_logout(request)
        
    return redirect('/view/login')

#채팅 시작
@require_GET
def chat_start(request):
    user = request.user
    
    chat_list = ChatList.objects.create(username=user)
    chat_list_id = chat_list.id
    return redirect(f'/view/chat?id={chat_list_id}')
    
    


from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.urls import resolve

class LoginCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        resolver_match = resolve(request.path_info)
        
        # 로그인 페이지인 경우 미들웨어를 건너뜁니다.
        if resolver_match.url_name == 'login':
            return self.get_response(request)

        # 사용자가 인증되지 않은 경우 로그인 페이지로 리디렉션합니다.
        if not request.user.is_authenticated:
            message = '로그인 정보 없음'
            if request.path_info != '/view/login':
                return redirect(f'/view/login?message={message}')

        # 다음 미들웨어나 뷰로 요청을 전달합니다.
        return self.get_response(request)

from django.shortcuts import render

#화면 호출 메소드
def view(request, view_name):
    return render(request, f'{view_name}.html')
    


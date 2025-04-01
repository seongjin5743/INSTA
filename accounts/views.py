from django.shortcuts import render, redirect  # 템플릿 렌더링 및 리다이렉트를 위한 함수
from .forms import CustomUserCreationForm, CustomAuthenticationForm  # 커스텀 회원가입 및 로그인 폼
from django.contrib.auth import login as auth_login  # 사용자 로그인 처리 함수
from django.contrib.auth import logout as auth_logout  # 사용자 로그아웃 처리 함수
from .models import User
from django.contrib.auth.decorators import login_required

# 회원가입 뷰
def signup(request):
    if request.method == 'POST':  # POST 요청일 경우, 폼 데이터를 처리
        form = CustomUserCreationForm(request.POST, request.FILES)  # 폼에 데이터와 파일 전달
        if form.is_valid():  # 폼 유효성 검사
            form.save()  # 유효하면 사용자 저장
            return redirect('posts:index')  # 저장 후 게시물 목록 페이지로 리다이렉트
    else:  # GET 요청일 경우, 빈 폼 생성
        form = CustomUserCreationForm()

    context = {
        'form': form,  # 템플릿에 전달할 폼 객체
    }
    return render(request, 'signup.html', context)  # 회원가입 템플릿 렌더링

# 로그인 뷰
def login(request):
    if request.method == 'POST':  # POST 요청일 경우, 폼 데이터를 처리
        form = CustomAuthenticationForm(request, request.POST)  # 폼에 요청 객체와 데이터 전달
        if form.is_valid():  # 폼 유효성 검사
            user = form.get_user()  # 유효하면 사용자 객체 가져오기
            auth_login(request, user)  # 사용자 로그인 처리
            return redirect('posts:index')  # 로그인 후 게시물 목록 페이지로 리다이렉트
    else:  # GET 요청일 경우, 빈 폼 생성
        form = CustomAuthenticationForm()
    context = {
        'form': form,  # 템플릿에 전달할 폼 객체
    }
    return render(request, 'login.html', context)  # 로그인 템플릿 렌더링

# 로그아웃 뷰
@login_required
def logout(request):
    auth_logout(request)  # 사용자 로그아웃 처리
    return redirect('posts:index')  # 로그아웃 후 게시물 목록 페이지로 리다이렉트

def profile(request, username):
    user_profile = User.objects.get(username=username)
    context = {
        'user_profile': user_profile,
    }
    return render(request, 'profile.html', context)

def follow(request, username):
    me = request.user
    you = User.objects.get(username=username)

    if me == you:
        return redirect('accounts:profile', username)

    if me in you.followers.all():
        you.followers.remove(me)
    else:
        you.followings.add(me)
    return redirect('accounts:profile', username)
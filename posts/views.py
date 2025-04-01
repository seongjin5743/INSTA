from django.shortcuts import render, redirect  # 템플릿 렌더링 및 리다이렉트를 위한 함수
from .models import Post  # Post 모델 가져오기
from .forms import PostForm, CommentForm  # 게시물 및 댓글 폼 가져오기
from django.contrib.auth.decorators import login_required  # 로그인 여부를 확인하는 데코레이터

# 게시물 목록(index) 뷰
def index(request):
    posts = Post.objects.all()  # 모든 게시물 가져오기
    form = CommentForm()  # 댓글 작성 폼 생성
    context = {
        'form': form,  # 템플릿에 전달할 폼 객체
        'posts': posts,  # 템플릿에 전달할 게시물 리스트
    }
    return render(request, 'index.html', context)  # 게시물 목록 템플릿 렌더링

# 게시물 생성(create) 뷰
@login_required  # 로그인된 사용자만 접근 가능
def create(request):
    if request.method == 'POST':  # POST 요청일 경우, 폼 데이터를 처리
        form = PostForm(request.POST, request.FILES)  # 폼에 데이터와 파일 전달
        if form.is_valid():  # 폼 유효성 검사
            post = form.save(commit=False)  # 데이터 저장 전, 객체 반환
            post.user = request.user  # 현재 로그인된 사용자를 작성자로 설정
            post.save()  # 게시물 저장
            return redirect('posts:index')  # 저장 후 게시물 목록 페이지로 리다이렉트
    else:  # GET 요청일 경우, 빈 폼 생성
        form = PostForm()
    context = {
        'form': form,  # 템플릿에 전달할 폼 객체
    }
    return render(request, 'create.html', context)  # 게시물 생성 템플릿 렌더링

# 게시물 상세(detail) 뷰
def detail(request, id):
    post = Post.objects.get(id=id)  # id에 해당하는 게시물 가져오기
    context = {
        'post': post,  # 템플릿에 전달할 게시물 객체
    }
    return render(request, 'detail.html', context)  # 게시물 상세 템플릿 렌더링

# 댓글 생성(comment_create) 뷰
@login_required  # 로그인된 사용자만 접근 가능
def comment_create(request, post_id):
    form = CommentForm(request.POST)  # POST 요청 데이터로 댓글 폼 생성
    if form.is_valid():  # 폼 유효성 검사
        comment = form.save(commit=False)  # 데이터 저장 전, 객체 반환
        comment.user = request.user  # 현재 로그인된 사용자를 댓글 작성자로 설정
        comment.post_id = post_id  # 댓글이 달린 게시물 설정
        comment.save()  # 댓글 저장
        return redirect('posts:index')  # 저장 후 게시물 목록 페이지로 리다이렉트

# 좋아요/좋아요 취소(like) 뷰
@login_required  # 로그인된 사용자만 접근 가능
def like(request, post_id):
    user = request.user  # 현재 로그인된 사용자
    post = Post.objects.get(id=post_id)  # id에 해당하는 게시물 가져오기
    
    if user in post.like_users.all():  # 사용자가 이미 좋아요를 눌렀는지 확인
        post.like_users.remove(user)  # 좋아요 취소
    else:
        post.like_users.add(user)  # 좋아요 추가
    return redirect('posts:index')  # 처리 후 게시물 목록 페이지로 리다이렉트

# 피드(feed) 뷰
def feed(request):
    followings = request.user.followings.all()  # 현재 사용자가 팔로우 중인 사용자 목록 가져오기
    posts = Post.objects.filter(user__in=followings)  # 팔로우 중인 사용자의 게시물 가져오기
    form = CommentForm()  # 댓글 작성 폼 생성
    context = {
        'posts': posts,  # 템플릿에 전달할 게시물 리스트
        'form': form,  # 템플릿에 전달할 폼 객체
    }
    return render(request, 'index.html', context)  # 피드 템플릿 렌더링
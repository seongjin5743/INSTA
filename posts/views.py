from django.shortcuts import render, redirect
from .models import Post
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required

# 게시물 목록(index) 뷰
def index(request):
    posts = Post.objects.all()  # 모든 게시물 가져오기
    form = CommentForm()
    context = {
        'form': form,
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
    post = Post.objects.get(id=id)
    context = {
        'post': post,
    }
    return render(request, 'detail.html', context)

@login_required
def comment_create(request, post_id):
    form = CommentForm(request.POST)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.post_id = post_id
        comment.save()
        return redirect('posts:index')

@login_required
def like(request, post_id):
    user = request.user
    post = Post.objects.get(id=post_id)
    
    if user in post.like_users.all():
        post.like_users.remove(user)
    else:
        post.like_users.add(user)
    return redirect('posts:index')

def feed(request):
    followings = request.user.followings.all()
    posts = Post.objects.filter(user__in=followings)
    form = CommentForm()
    context = {
        'posts': posts,
        'form': form,
    }
    return render(request, 'index.html', context)
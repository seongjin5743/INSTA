from django.urls import path  # URL 패턴을 정의하기 위한 함수
from . import views  # 현재 디렉토리의 views 모듈 가져오기

app_name = 'posts'  # 앱 이름 지정 (URL 네임스페이스)

urlpatterns = [
    path('', views.index, name='index'),  # 게시물 목록 페이지 URL
    path('create/', views.create, name='create'),  # 게시물 생성 페이지 URL
    path('<int:id>/', views.detail, name='detail'),  # 게시물 상세 페이지 URL
    path('<int:post_id>/comments/create/', views.comment_create, name='comment_create'),  # 댓글 생성 URL
    path('<int:post_id>/comments/<int:comment_id>/delete/', views.comment_delete, name='comment_delete'), # 댓글 삭제 URL
    # path('<int:post_id>/like/', views.like, name='like'),  # 좋아요/좋아요 취소 URL
    path('feed/', views.feed, name='feed'),  # 피드 페이지 URL
    path('<int:id>/like-async/',views.like_async, name='like_async') # 좋아요/좋아요 취소 URL
]
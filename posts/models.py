from django.db import models  # Django의 ORM을 사용하기 위한 models 모듈
from django_resized import ResizedImageField  # 이미지를 리사이즈하기 위한 필드 제공
from django.conf import settings  # 프로젝트 설정을 가져오기 위한 모듈

# 게시물(Post) 모델 정의
class Post(models.Model):
    content = models.TextField()  # 게시물 내용 저장
    created_at = models.DateTimeField(auto_now_add=True)  # 게시물 생성 시간 자동 저장

    # 게시물 이미지 필드
    # 이미지는 500x500 크기로 리사이즈되고, 중앙을 기준으로 크롭됨
    # 업로드된 파일은 'image/년/월' 디렉토리에 저장됨
    image = ResizedImageField(
        size=[500, 500],  # 리사이즈할 이미지 크기
        crop=['middle', 'center'],  # 이미지 크롭 위치
        upload_to='image/%Y/%m',  # 파일 업로드 경로 (년/월 구조)
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # User 모델과의 외래키 관계
        on_delete=models.CASCADE  # 작성자가 삭제되면 해당 게시물도 삭제됨
    )

    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,  # 좋아요를 누른 사용자와의 관계
        related_name='like_posts',  # 역참조 시 사용할 이름
    )

# 댓글(Comment) 모델 정의
class Comment(models.Model):
    content = models.CharField(max_length=200)  # 댓글 내용 (최대 200자)
    post = models.ForeignKey(
        Post,  # 댓글이 달린 게시물과의 외래키 관계
        on_delete=models.CASCADE  # 게시물이 삭제되면 댓글도 삭제됨
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # 댓글 작성자와의 외래키 관계
        on_delete=models.CASCADE  # 작성자가 삭제되면 댓글도 삭제됨
    )
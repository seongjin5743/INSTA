from django.db import models
from django_resized import ResizedImageField
from django.conf import settings
class Post(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    # image = models.ImageField(upload_to='image')
    # 이미지는 500x500 크기로 리사이즈되고, 중앙을 기준으로 크롭됨
    # 업로드된 파일은 'image/년/월' 디렉토리에 저장됨
    image = ResizedImageField(
        size=[500, 500],  # 리사이즈할 이미지 크기
        crop=['middle', 'center'],  # 이미지 크롭 위치
        upload_to='image/%Y/%m',  # 파일 업로드 경로 (년/월 구조)
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  
    # 게시물 작성자 (User 모델과의 외래키 관계)
    # 작성자가 삭제되면 해당 게시물도 삭제됨

class Comment(models.Model):
    content = models.CharField(max_length=200)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
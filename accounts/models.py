from django.db import models
from django.contrib.auth.models import AbstractUser
from django_resized import ResizedImageField

class User(AbstractUser):
    # 이미지는 500x500 크기로 리사이즈되고, 중앙을 기준으로 크롭됨
    # 업로드된 파일은 'profile' 디렉토리에 저장됨
    profile_image = ResizedImageField(
        size=[500, 500],  # 리사이즈할 이미지 크기
        crop=['middle', 'center'],  # 이미지 크롭 위치
        upload_to='profile',  # 파일 업로드 경로
    )

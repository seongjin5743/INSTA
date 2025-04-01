from django.contrib import admin  # 관리자 페이지를 위한 admin 모듈
from django.urls import path, include  # URL 패턴 정의 및 앱 URL 포함을 위한 함수
from django.conf.urls.static import static  # 정적 및 미디어 파일 서빙을 위한 함수
from django.conf import settings  # 프로젝트 설정을 가져오기 위한 모듈
from accounts import views  # accounts 앱의 뷰 가져오기

urlpatterns = [
    path('', views.home, name='home'),  # 홈 페이지 URL (accounts 앱의 home 뷰 연결)
    path('admin/', admin.site.urls),  # 관리자 페이지 URL
    path('posts/', include('posts.urls')),  # 'posts' 앱의 URL 패턴 포함
    path('accounts/', include('accounts.urls')),  # 'accounts' 앱의 URL 패턴 포함
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # 미디어 파일 URL 및 루트 설정
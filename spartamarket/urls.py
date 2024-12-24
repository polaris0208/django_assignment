from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns += [
  path('users/', include('users.urls'))
]

urlpatterns += [
  path('home/', include('homepage.urls'))
]

urlpatterns += [
  path('accounts/', include('accounts.urls'))
]

urlpatterns += [
  path('products/', include('products.urls'))
]

# 개발 환경에서 MEDIA 파일 관리
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
        )
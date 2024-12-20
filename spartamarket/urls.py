from django.contrib import admin
from django.urls import path, include

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
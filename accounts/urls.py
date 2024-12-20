from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
  path('login/', views.login, name='login'),
  path('logout/', views.logout, name='logout'),
  path('signin/', views.signin, name='signin'),
  path('resign/', views.resign, name='resign'),
  path('update/', views.update, name='update'),
  path('change-password/', views.change_password, name='change-password'),
]

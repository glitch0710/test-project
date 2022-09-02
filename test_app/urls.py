from django.urls import path
from . import views


urlpatterns = [
    path('', views.login_user, name='login_user'),
    path('info/', views.user_info, name='user_info'),
    path('register/', views.register_user, name='register_user'),
    path('logout/', views.logout_user, name='logout_user'),
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('home/', views.user_home, name='user_home')
]
from django.urls import path
from . import views


urlpatterns = [
    path('', views.login_user, name='login_user'),
    path('info/', views.user_info, name='user_info'),
    path('register/', views.register_user, name='register_user'),
    path('logout/', views.logout_user, name='logout_user'),
    path('home/', views.user_home, name='user_home'),
    path('home/addentry/', views.add_entry, name='add_entry'),
    path('home/viewarea/<int:pk>', views.view_area, name='view_area'),

    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('dashboard/viewuser/<int:pk>', views.view_user, name='view_user'),
    path('dashboard/viewuserarea/<int:pk>/', views.view_area_admin, name='view_area_admin'),
]

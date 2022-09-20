from django.urls import path
from . import views


urlpatterns = [
    path('', views.login_user, name='login_user'),
    path('register/', views.register_user, name='register_user'),
    path('logout/', views.logout_user, name='logout_user'),
    path('verify/', views.user_home, name='user_home'),

    # Staff
    path('info/', views.user_info, name='user_info'),
    path('info/farmer', views.add_farmer, name='add_farmer'),
    path('info/addentry/', views.add_entry, name='add_entry'),
    path('info/farmer/<int:pk>', views.view_user, name='view_farmer'),
    path('info/viewarea/<int:pk>', views.view_area, name='view_area'),

    # Admin
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('dashboard/viewuser/<int:pk>', views.view_user, name='view_user'),
    path('dashboard/viewuserarea/<int:pk>/', views.view_area_admin, name='view_area_admin'),
    path('dashboard/area', views.viewarea_dashboard, name='viewarea_dashboard'),
    path('dashboard/users', views.user_list, name='user_list'),

    # Engineer
    path('home/', views.user_engineer, name='user_engineer'),
    path('home/viewarea/<int:pk>', views.engineer_view_area, name='engineer_view_area'),

    # Locations
    path('loadprovince/<int:pk>', views.province_filtered, name='province_filtered'),
    path('loadmuncity/<int:pk>', views.muncity_filtered, name='muncity_filtered'),
    path('loadbrgy/<int:pk>', views.brgy_filtered, name='brgy_filtered'),
]

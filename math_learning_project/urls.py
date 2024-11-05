from django.contrib import admin
from django.urls import path , include
from math_app.views import CustomLogoutView
from django.contrib.auth import views as auth_views
from math_app import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='math_app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('exercise/', views.exercise, name='exercise'),
    path('practice/', views.practice_mode, name='practice_mode'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('tutorials/', views.tutorial_list, name='tutorial_list'),
    path('tutorials/<int:tutorial_id>/', views.tutorial_detail, name='tutorial_detail'),
]
from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as vw

app_name='users'
urlpatterns = [
    path('login/',vw.LoginView.as_view(template_name='USERS/login-cover.html'),name='login'),
    path('logout/',vw.LogoutView.as_view(template_name='Shop/home-page.html'),name='logout'),
    path('register/',views.registerview,name='register'),
    path('profile/',views.profileview,name='profile'),
]

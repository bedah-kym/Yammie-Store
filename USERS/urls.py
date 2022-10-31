from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as vw

app_name='users'
urlpatterns = [
    path('login/',vw.LoginView.as_view(template_name='USERS/login-cover.html'),name='login'),
    path('logout/',vw.LogoutView.as_view(template_name='Shop/home-page.html'),name='logout'),
    path('register/',views.registerview,name='register'),
    path('make-agent/',views.makeagent,name='make-agent'),
    path('unmake-agent/',views.unmakeagent,name='unmake-agent'),
    path('profile/',views.profileview,name='profile'),
]

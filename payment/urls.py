from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('index', views.index2,name='mpesa_stk_push_callback'),

]

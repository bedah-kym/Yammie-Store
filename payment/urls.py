from django.urls import path, include
from . import views

urlpatterns = [
    path('pay4goods/', views.index, name='chargeclient'),
    path('payagent/', views.payagent, name='payagent'),

]

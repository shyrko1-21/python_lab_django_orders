from django.contrib import admin
from django.urls import path, re_path, include

from orders import views

urlpatterns = [
    path('', views.clients, name='clients'),
    re_path(r'^([0-9]+)/$', views.orders, name='orders'),
]
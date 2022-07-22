from django.contrib import admin
from django.urls import path, re_path, include

from orders import views

urlpatterns = [
    path('', views.clients, name='clients'),
    re_path(r'^([0-9]+)/$', views.orders, name='orders'),
    re_path(r'^register/$', views.RegisterFormView.as_view()),
    re_path(r'^login/$', views.LoginFormView.as_view()),
    re_path(r'^logout/$', views.LogoutView.as_view()),
    re_path(r'^password-change/', views.PasswordChangeView.as_view()),
    # отправка сообщения
    re_path(r'^([0-9]+)/post/$', views.post, name='post'),
    # отправка списка сообщений
    re_path(r'^([0-9]+)/msg_list/$', views.msg_list, name='msg_list'),
    # отправка оценки
    re_path(r'^([0-9]+)/post_mark/$', views.post_mark, name='post_mark'),
    # средняя оценка
    re_path(r'^([0-9]+)/get_mark/$', views.get_mark, name='get_mark'),
]

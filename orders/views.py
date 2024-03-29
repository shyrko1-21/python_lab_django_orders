from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import render, get_list_or_404

# Create your views here.
from .models import Client, Order, Mark, Message
from django.shortcuts import get_object_or_404, render, redirect
# оценки
# вычисление среднего,
# например, средней оценки
from django.db.models import Avg
from django import forms
from django.utils.translation import gettext, gettext_lazy as _


def clients(request):
    clients = Client.objects.all()
    return render(
        request,
        'clients.html',
        context={'clients': clients},
    )


def orders(request, client_id):
    orders = Order.objects.filter(client=client_id)
    return render(
        request,
        'orders.html',
        context={
            'client': get_object_or_404(Client, pk=client_id),
            'orders': orders,
            # 'latest_orders':  Message.objects.filter(chat_id=client_id).order_by('-pub_date')[:5],
            # кол-во оценок, выставленных пользователем
            "already_rated_by_user":
                Mark.objects
                    .filter(author_id=request.user.id)
                    .filter(client_id=client_id)
                    .count(),
            # оценка текущего пользователя
            "user_rating":
                Mark.objects
                    .filter(author_id=request.user.id)
                    .filter(client_id=client_id)
                    .aggregate(Avg('mark'))
                ["mark__avg"],
            # средняя по всем пользователям оценка
            "avg_mark":
                Mark.objects
                    .filter(client_id=client_id)
                    .aggregate(Avg('mark'))
                ["mark__avg"]
        }
    )


# Базовый класс для обработки страниц с формами.
from django.views.generic.edit import FormView
# Спасибо django за готовую форму регистрации.
from django.contrib.auth.forms import UserCreationForm

...
# базовый URL приложения, главной страницы -
# часто нужен при указании путей переадресации
app_url = "/orders/"


# наше представление для регистрации
class RegisterFormView(FormView):
    # будем строить на основе
    # встроенной в django формы регистрации
    form_class = UserCreationForm
    # Ссылка, на которую будет перенаправляться пользователь
    # в случае успешной регистрации.
    # В данном случае указана ссылка на
    # страницу входа для зарегистрированных пользователей.
    success_url = app_url + "login/"
    # Шаблон, который будет использоваться
    # при отображении представления.
    template_name = "reg/register.html"

    def form_valid(self, form):
        # Создаём пользователя,
        # если данные в форму были введены корректно.
        form.save()
        # Вызываем метод базового класса
        return super(RegisterFormView, self).form_valid(form)


# Спасибо django за готовую форму аутентификации.
from django.contrib.auth.forms import AuthenticationForm
# Функция для установки сессионного ключа.
# По нему django будет определять,
# выполнил ли вход пользователь.
from django.contrib.auth import login

...


# наше представление для входа
class LoginFormView(FormView):
    # будем строить на основе
    # встроенной в django формы входа
    form_class = AuthenticationForm
    # Аналогично регистрации,
    # только используем шаблон аутентификации.
    template_name = "reg/login.html"
    # В случае успеха перенаправим на главную.
    success_url = app_url

    def form_valid(self, form):
        # Получаем объект пользователя
        # на основе введённых в форму данных.
        self.user = form.get_user()
        # Выполняем аутентификацию пользователя.
        login(self.request, self.user)
        return super(LoginFormView, self).form_valid(form)


# Для Log out с перенаправлением на главную
from django.http import HttpResponseRedirect
from django.views.generic.base import View
from django.contrib.auth import logout

...


# для выхода - миниатюрное представление без шаблона -
# после выхода перенаправим на главную
class LogoutView(View):
    def get(self, request):
        # Выполняем выход для пользователя,
        # запросившего данное представление.
        logout(request)
        # После чего перенаправляем пользователя на
        # главную страницу.
        return HttpResponseRedirect(app_url)


# Для смены пароля - форма
from django.contrib.auth.forms import PasswordChangeForm

...


# наше представление для смены пароля
class PasswordChangeView(FormView):
    # будем строить на основе
    # встроенной в django формы смены пароля
    form_class = PasswordChangeForm
    template_name = 'reg/password_change_form.html'
    # после смены пароля нужно снова входить
    success_url = app_url + 'login/'

    def get_form_kwargs(self):
        kwargs = super(PasswordChangeView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        if self.request.method == 'POST':
            kwargs['data'] = self.request.POST
        return kwargs

    def form_valid(self, form):
        form.save()
        return super(PasswordChangeView, self).form_valid(form)


# сообщения
from .models import Message
from datetime import datetime

...


def post(request, client_id):
    msg = Message()
    msg.author = request.user
    msg.chat = get_object_or_404(Client, pk=client_id)
    msg.message = request.POST['message']
    msg.pub_date = datetime.now()
    msg.save()
    return HttpResponseRedirect(app_url + str(client_id))


# для ответа на асинхронный запрос в формате JSON
from django.http import JsonResponse
import json

...


def msg_list(request, client_id):
    # выбираем список сообщений
    res = list(
        Message.objects
            # фильтруем по id загадки
            .filter(chat_id=client_id)
            # отбираем 5 самых свежих
            .order_by('-pub_date')[:5]
            # выбираем необходимые поля
            .values('author__username',
                    'pub_date',
                    'message'
                    )
    )
    # конвертируем даты в строки - сами они не умеют
    for r in res:
        r['pub_date'] = \
            r['pub_date'].strftime(
                '%d.%m.%Y %H:%M:%S'
            )
    return JsonResponse(json.dumps(res), safe=False)


# оценки
from .models import Mark

...


def post_mark(request, client_id):
    msg = Mark()
    msg.author = request.user
    msg.client = get_object_or_404(Client, pk=client_id)
    msg.mark = request.POST['mark']
    msg.pub_date = datetime.now()
    msg.save()
    return HttpResponseRedirect(app_url + str(client_id))


def get_mark(request, client_id):
    res = Mark.objects.filter(client_id=client_id).aggregate(Avg('mark'))
    return JsonResponse(json.dumps(res), safe=False)


def admin(request):
    clients = Client.objects.all()
    return render(
        request,
        "admin.html",
        context={
            'clients': clients
        }
    )


def post_client(request):
    # защита от добавления клиентов неадминистраторами
    author = request.user
    if not (author.is_authenticated and author.is_staff):
        return HttpResponseRedirect(app_url + "admin")

    # добавление клиента
    client = Client()
    client.client_name = request.POST['text']
    client.save()

    # добавление заказов
    order = Order()
    order.client = client
    order.description = request.POST['description']
    order.qty = request.POST['qty']
    order.date = datetime.now()
    order.save()

    for i in User.objects.all():
        # проверка, что текущий пользователь подписан - указал e-mail
        if i.email != '':
            send_mail(
                # тема письма
                'New client',
                # текст письма
                'A new client was added:\n' +
                'http://localhost:8000/orders/' + str(client.id) + '.',
                # отправитель
                'forreg100@mail.ru',
                # список получателей из одного получателя
                [i.email],
                # отключаем замалчивание ошибок,
                # чтобы из видеть и исправлять
                False
            )
    return HttpResponseRedirect(app_url + str(client.id))


# класс, описывающий логику формы:
# список заполняемых полей и их сохранение
class SubscribeForm(forms.Form):
    # поле для ввода e-mail
    email = forms.EmailField(
        label=_("E-mail"),
        required=True,
    )

    # конструктор для запоминания пользователя,
    # которому задается e-mail
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    # сохранение e-mail
    def save(self, commit=True):
        self.user.email = self.cleaned_data["email"]
        if commit:
            self.user.save()
        return self.user


# класс, описывающий взаимодействие логики
# со страницами веб-приложения
class SubscribeView(FormView):
    # используем класс с логикой
    form_class = SubscribeForm
    # используем собственный шаблон
    template_name = 'subscribe.html'
    # после подписки возвращаем на главную станицу
    success_url = app_url

    # передача пользователя для конструктора класса с логикой
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    # вызов логики сохранения введенных данных
    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(self.success_url)


# функция для удаления подписки (форма не нужна,
# поэтому без классов, просто функция)
def unsubscribe(request):
    request.user.email = ''
    request.user.save()
    return HttpResponseRedirect(app_url)

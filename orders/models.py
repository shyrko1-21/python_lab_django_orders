from django.db import models

# Create your models here.
class Client(models.Model):
    client_name = models.CharField(max_length=255)

class Order(models.Model):
    description = models.CharField(max_length=255)
    qty = models.IntegerField()
    date = models.DateTimeField()
    client = models.ForeignKey(Client,on_delete=models.SET_NULL, null=True)

# встроенная модель пользователя
# нужна для авторов сообщений
from django.contrib.auth.models import User
# тип "временнАя зона" для получения текущего времени
from django.utils import timezone
...
class Message(models.Model):
    chat = models.ForeignKey(
        Client,
        verbose_name='Чат под загадкой',
        on_delete=models.CASCADE)
    author = models.ForeignKey(
        User,
        verbose_name='Пользователь', on_delete=models.CASCADE)
    message = models.TextField('Сообщение')
    pub_date = models.DateTimeField(
        'Дата сообщения',
        default=timezone.now)

class Mark(models.Model):
    client = models.ForeignKey(
        Client,
        verbose_name='Клиент',
        on_delete=models.CASCADE)
    author = models.ForeignKey(
        User,
        verbose_name='Пользователь', on_delete=models.CASCADE)
    mark = models.IntegerField(
        verbose_name='Оценка')
    pub_date = models.DateTimeField(
        'Дата оценки',
        default=timezone.now)

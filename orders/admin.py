from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Client, Order, Message, Mark
admin.site.register(Client)
admin.site.register(Order)
admin.site.register(Message)
admin.site.register(Mark)
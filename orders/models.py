from django.db import models

# Create your models here.
class Client(models.Model):
    client_name = models.CharField(max_length=255)

class Order(models.Model):
    description = models.CharField(max_length=255)
    qty = models.IntegerField()
    date = models.DateTimeField()
    client = models.ForeignKey(Client,on_delete=models.SET_NULL, null=True)
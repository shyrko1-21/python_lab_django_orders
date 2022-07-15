from django.shortcuts import render, get_list_or_404

# Create your views here.
from .models import Client, Order
from django.shortcuts import get_object_or_404, render, redirect

def clients(request):
    clients = Client.objects.all()
    return render(
        request,
        'clients.html',
        context={'clients':clients},
    )

def orders(request, client_id):
    orders = Order.objects.filter(client=client_id)
    return render(
        request,
        'orders.html',
        context={
            'client': get_object_or_404(Client, pk=client_id),
            'orders': orders},
    )
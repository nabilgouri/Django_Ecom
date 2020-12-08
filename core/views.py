from django.shortcuts import render
from .models import Item, Order, OrderItem


def itemList(request):
    context = {
        'items': Item.objects.all()



    }
    return render(request, "itemList.html", context)

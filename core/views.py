from django.shortcuts import render, get_object_or_404, redirect
from .models import Item, Order, OrderItem
from django.views.generic import ListView, DetailView
from django.utils import timezone


def checkout(request):
    context = {

    }
    return render(request, "checkout-page.html", context)


def products(request):
    context = {
        'items': Item.objects.all()
    }
    return render(request, "product-page.html", context)


class HomeView(ListView):
    model = Item
    template_name = 'home-page.html'


class ItemDetailView(DetailView):
    model = Item
    template_name = 'product.html'


def add_to_cart(request, slug):
    # hna we get the item lel cart
    item = get_object_or_404(Item, slug=slug)
    # hna we make it a part f our order
    order_item, created = OrderItem.objects.get_or_create(
        item=item, user=request.user, ordered=False)

    # order_qs tessma order querry set w nfiltriwha to be unique 3a assass l user ofc
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        # kan kayn deja order fel cart nroto our item jdid as the first item fel order
        order = order_qs[0]
        # bsh kan l item aw deja fel order nzidou quantity brk
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity = order_item.quantity + 1
            order_item.save()
        else:
            order.items.add(order_item)

    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, orderDate=ordered_date)
        order.items.add(order_item)
    return redirect("core:product", slug=slug)

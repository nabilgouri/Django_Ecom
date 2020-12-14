from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
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
    paginate_by = 12


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
            messages.info(request, "This item quantity is updated")
        else:
            order.items.add(order_item)

    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, orderDate=ordered_date)
        order.items.add(order_item)
    return redirect("core:product", slug=slug)


def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, "This item was removed from your cart.")
            # return redirect("core:order-summary")
            return redirect("core:product", slug=slug)
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("core:product", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("core:product", slug=slug)

    return redirect("core:product", slug=slug)

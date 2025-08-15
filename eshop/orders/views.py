from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpRequest
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart


def order_create(request: HttpRequest):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST, request=request)
        if form.is_valid():
            order = form.save()
            for item in cart:
                discount_price = item['product'].sell_price()
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=discount_price,
                                         quantity=item['quantity'])
            cart.clear()
            request.session['order_id'] = order.id
            return redirect(reverse('payment:process'))
    else:
        form = OrderCreateForm(request=request)
    return render(request,
                  'orders/create.html',
                  {'cart': cart,
                   'form': form})



from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from cart.cart import Cart

from .forms import OrderForm
from .models import Order, OrderItem

COURIER_COST = Decimal('300.00')


@login_required
def checkout(request):
    cart = Cart(request)
    if len(cart) == 0:
        return redirect('cart:detail')

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            delivery_method = form.cleaned_data['delivery_method']
            delivery_cost = COURIER_COST if delivery_method == 'courier' else Decimal('0.00')
            cart_total = cart.get_total_price()

            order = Order.objects.create(
                user=request.user,
                full_name=form.cleaned_data['full_name'],
                phone=form.cleaned_data['phone'],
                address=form.cleaned_data['address'],
                delivery_method=delivery_method,
                delivery_cost=delivery_cost,
                total=cart_total + delivery_cost,
                is_paid=True,
            )

            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity'],
                )

            cart.clear()
            return redirect('orders:order_success', order_id=order.pk)
    else:
        initial = {
            'full_name': request.user.full_name or '',
            'phone': request.user.phone or '',
        }
        form = OrderForm(initial=initial)

    return render(request, 'orders/checkout.html', {
        'form': form,
        'cart': cart,
        'courier_cost': COURIER_COST,
    })


@login_required
def order_success(request, order_id):
    order = get_object_or_404(Order, pk=order_id, user=request.user)
    return render(request, 'orders/order_success.html', {'order': order})


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, pk=order_id, user=request.user)
    goods_total = order.total - order.delivery_cost
    return render(request, 'orders/order_detail.html', {
        'order': order,
        'goods_total': goods_total,
    })

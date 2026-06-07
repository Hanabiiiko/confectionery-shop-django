from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from cart.cart import Cart

from .forms import OrderForm
from .models import Order, OrderItem, PromoCode

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

            promo_code_str = form.cleaned_data.get('promo_code', '').strip()
            discount = Decimal('0.00')
            applied_code = ''

            if promo_code_str:
                try:
                    promo = PromoCode.objects.get(code__iexact=promo_code_str, active=True)
                    today = timezone.now().date()
                    if promo.valid_until is not None and promo.valid_until < today:
                        form.add_error('promo_code', 'Промокод истёк.')
                    else:
                        discount = (cart_total * promo.discount_percent / 100).quantize(Decimal('0.01'))
                        applied_code = promo.code
                except PromoCode.DoesNotExist:
                    form.add_error('promo_code', 'Промокод не найден или неактивен.')

            if not form.errors.get('promo_code'):
                order = Order.objects.create(
                    user=request.user,
                    full_name=form.cleaned_data['full_name'],
                    phone=form.cleaned_data['phone'],
                    address=form.cleaned_data['address'],
                    delivery_method=delivery_method,
                    delivery_cost=delivery_cost,
                    promo_code=applied_code,
                    discount=discount,
                    total=cart_total - discount + delivery_cost,
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


@require_POST
def validate_promo(request):
    code = request.POST.get('code', '').strip()
    cart = Cart(request)
    cart_total = cart.get_total_price()

    if not code:
        return JsonResponse({'valid': False, 'message': 'Введите код.'})

    try:
        promo = PromoCode.objects.get(code__iexact=code, active=True)
        today = timezone.now().date()
        if promo.valid_until is not None and promo.valid_until < today:
            return JsonResponse({'valid': False, 'message': 'Промокод истёк.'})
        discount = float(
            (cart_total * promo.discount_percent / 100).quantize(Decimal('0.01'))
        )
        return JsonResponse({
            'valid': True,
            'discount': discount,
            'message': f'Промокод применён. Скидка {promo.discount_percent} %',
        })
    except PromoCode.DoesNotExist:
        return JsonResponse({'valid': False, 'message': 'Промокод не найден или неактивен.'})


@login_required
def order_success(request, order_id):
    order = get_object_or_404(Order, pk=order_id, user=request.user)
    return render(request, 'orders/order_success.html', {'order': order})


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, pk=order_id, user=request.user)
    goods_total = order.total - order.delivery_cost + order.discount
    return render(request, 'orders/order_detail.html', {
        'order': order,
        'goods_total': goods_total,
    })

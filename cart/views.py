from django.shortcuts import get_object_or_404, redirect, render

from shop.models import Product
from .cart import Cart


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/cart.html', {'cart': cart})


def cart_add(request, pk):
    if request.method != 'POST':
        return redirect('cart:detail')
    product = get_object_or_404(Product, pk=pk, available=True)
    cart = Cart(request)
    try:
        quantity = int(request.POST.get('quantity', 1))
        quantity = max(1, min(99, quantity))
    except (ValueError, TypeError):
        quantity = 1
    update = request.POST.get('update_quantity') == '1'
    cart.add(product, quantity=quantity, update_quantity=update)
    referer = request.META.get('HTTP_REFERER', '/shop/')
    return redirect(referer)


def cart_remove(request, pk):
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=pk)
        cart = Cart(request)
        cart.remove(product)
    return redirect('cart:detail')


def cart_update(request, pk):
    if request.method == 'POST':
        cart = Cart(request)
        try:
            quantity = int(request.POST.get('quantity', 1))
            quantity = max(1, min(99, quantity))
        except (ValueError, TypeError):
            quantity = 1
        cart.update(pk, quantity)
    return redirect('cart:detail')


def cart_clear(request):
    if request.method == 'POST':
        cart = Cart(request)
        cart.clear()
    return redirect('cart:detail')

from django.shortcuts import render

from shop.models import Product
from orders.models import Order

from .decorators import manager_required


@manager_required
def dashboard_home(request):
    context = {
        'products_count': Product.objects.count(),
        'orders_count': Order.objects.count(),
        'new_orders_count': Order.objects.filter(status='new').count(),
    }
    return render(request, 'dashboard/home.html', context)

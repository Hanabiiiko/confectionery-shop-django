from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from shop.models import Category, Product
from orders.models import Order

from .decorators import manager_required
from .forms import CategoryForm, ProductForm


@manager_required
def dashboard_home(request):
    context = {
        'section': 'overview',
        'products_count': Product.objects.count(),
        'orders_count': Order.objects.count(),
        'new_orders_count': Order.objects.filter(status='new').count(),
    }
    return render(request, 'dashboard/home.html', context)


@manager_required
def product_list(request):
    products = Product.objects.select_related('category')

    q = request.GET.get('q', '').strip()
    if q:
        products = products.filter(name__icontains=q)

    current_category = None
    slug = request.GET.get('category', '').strip()
    if slug:
        current_category = Category.objects.filter(slug=slug).first()
        products = products.filter(category__slug=slug)

    context = {
        'section': 'products',
        'products': products,
        'categories': Category.objects.all(),
        'q': q,
        'current_category': current_category,
    }
    return render(request, 'dashboard/product_list.html', context)


@manager_required
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, f'Товар «{product.name}» добавлен.')
            return redirect('dashboard:product_list')
    else:
        form = ProductForm()

    context = {
        'section': 'products',
        'form': form,
        'title': 'Добавить товар',
    }
    return render(request, 'dashboard/product_form.html', context)


@manager_required
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, f'Товар «{product.name}» обновлён.')
            return redirect('dashboard:product_list')
    else:
        form = ProductForm(instance=product)

    context = {
        'section': 'products',
        'form': form,
        'title': 'Изменить товар',
    }
    return render(request, 'dashboard/product_form.html', context)


@manager_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        name = product.name
        product.delete()
        messages.success(request, f'Товар «{name}» удалён.')
        return redirect('dashboard:product_list')

    context = {
        'section': 'products',
        'product': product,
    }
    return render(request, 'dashboard/product_confirm_delete.html', context)


@manager_required
def category_list(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            category = form.save()
            messages.success(request, f'Категория «{category.name}» добавлена.')
            return redirect('dashboard:category_list')
    else:
        form = CategoryForm()

    context = {
        'section': 'categories',
        'form': form,
        'categories': Category.objects.all(),
    }
    return render(request, 'dashboard/category_list.html', context)

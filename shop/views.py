from django.db.models import Q
from django.views.generic import DetailView, ListView, TemplateView

from .models import Category, Product

SORT_MAP = {
    'price_asc':  'price',
    'price_desc': '-price',
    'newest':     '-created_at',
}


class HomeView(TemplateView):
    template_name = 'shop/home.html'


class CatalogView(ListView):
    template_name = 'shop/catalog.html'
    context_object_name = 'products'
    paginate_by = 9

    def get_queryset(self):
        qs = Product.objects.filter(available=True).select_related('category')

        slug = self.kwargs.get('slug')
        if slug:
            qs = qs.filter(category__slug=slug)

        q = self.request.GET.get('q', '').strip()
        if q:
            qs = qs.filter(Q(name__icontains=q) | Q(description__icontains=q))

        min_price = self.request.GET.get('min_price', '').strip()
        max_price = self.request.GET.get('max_price', '').strip()
        if min_price:
            try:
                qs = qs.filter(price__gte=min_price)
            except Exception:
                pass
        if max_price:
            try:
                qs = qs.filter(price__lte=max_price)
            except Exception:
                pass

        sort = self.request.GET.get('sort', 'newest')
        qs = qs.order_by(SORT_MAP.get(sort, '-created_at'))
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()

        slug = self.kwargs.get('slug')
        context['current_category'] = (
            Category.objects.get(slug=slug) if slug else None
        )

        params = self.request.GET.copy()
        params.pop('page', None)
        context['get_params'] = params.urlencode()
        context['current_sort'] = self.request.GET.get('sort', 'newest')
        context['current_min'] = self.request.GET.get('min_price', '')
        context['current_max'] = self.request.GET.get('max_price', '')
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'shop/product_detail.html'
    context_object_name = 'product'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object
        context['related'] = (
            Product.objects
            .filter(category=product.category, available=True)
            .exclude(pk=product.pk)[:4]
        )
        return context

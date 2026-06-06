from django.views.generic import ListView, TemplateView

from .models import Category, Product


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
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        slug = self.kwargs.get('slug')
        context['current_category'] = (
            Category.objects.get(slug=slug) if slug else None
        )
        return context

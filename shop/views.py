from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Avg, Q
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import DetailView, ListView, TemplateView

from .forms import ReviewForm
from .models import Category, Favorite, Product, Review

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
        if self.request.user.is_authenticated:
            context['favorite_ids'] = set(
                Favorite.objects.filter(user=self.request.user)
                .values_list('product_id', flat=True)
            )
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
        reviews = product.reviews.select_related('user').order_by('-created_at')
        context['reviews'] = reviews
        agg = reviews.aggregate(avg=Avg('rating'))['avg']
        context['avg_rating'] = round(agg, 1) if agg else None

        user = self.request.user
        if user.is_authenticated:
            user_review = reviews.filter(user=user).first()
            context['user_review'] = user_review
            if not user_review:
                context['review_form'] = ReviewForm()
            context['is_favorite'] = Favorite.objects.filter(
                user=user, product=product
            ).exists()
        return context


class FavoritesView(LoginRequiredMixin, ListView):
    template_name = 'shop/favorites.html'
    context_object_name = 'products'

    def get_queryset(self):
        return (
            Product.objects
            .filter(favorited_by__user=self.request.user)
            .select_related('category')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['favorite_ids'] = set(
            Favorite.objects.filter(user=self.request.user)
            .values_list('product_id', flat=True)
        )
        return context


@login_required
def toggle_favorite(request, pk):
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=pk)
        fav, created = Favorite.objects.get_or_create(
            user=request.user, product=product
        )
        if not created:
            fav.delete()
    return redirect(request.META.get('HTTP_REFERER', '/shop/'))


@login_required
def add_review(request, slug):
    product = get_object_or_404(Product, slug=slug)
    if request.method == 'POST':
        if Review.objects.filter(product=product, user=request.user).exists():
            messages.error(request, 'Вы уже оставили отзыв на этот товар.')
        else:
            form = ReviewForm(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                review.product = product
                review.user = request.user
                review.save()
                messages.success(request, 'Отзыв добавлен. Спасибо!')
            else:
                messages.error(request, 'Проверьте введённые данные.')
    return redirect('product_detail', slug=slug)

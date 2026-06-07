from django.urls import path

from . import views

urlpatterns = [
    path('', views.CatalogView.as_view(), name='catalog'),
    path('favorites/', views.FavoritesView.as_view(), name='favorites'),
    path('favorite/toggle/<int:pk>/', views.toggle_favorite, name='toggle_favorite'),
    path('product/<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('product/<slug:slug>/review/', views.add_review, name='add_review'),
    path('<slug:slug>/', views.CatalogView.as_view(), name='catalog_category'),
]

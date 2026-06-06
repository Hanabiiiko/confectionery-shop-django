from django.urls import path

from . import views

urlpatterns = [
    path('', views.CatalogView.as_view(), name='catalog'),
    path('product/<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('<slug:slug>/', views.CatalogView.as_view(), name='catalog_category'),
]

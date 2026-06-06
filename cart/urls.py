from django.urls import path

from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_detail, name='detail'),
    path('add/<int:pk>/', views.cart_add, name='add'),
    path('remove/<int:pk>/', views.cart_remove, name='remove'),
    path('update/<int:pk>/', views.cart_update, name='update'),
    path('clear/', views.cart_clear, name='clear'),
]

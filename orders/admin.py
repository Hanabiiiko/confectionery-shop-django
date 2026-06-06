from django.contrib import admin

from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product', 'price', 'quantity']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name', 'phone', 'delivery_method', 'total', 'status', 'is_paid', 'created_at']
    list_filter = ['status', 'is_paid', 'delivery_method']
    search_fields = ['full_name', 'phone']
    readonly_fields = ['created_at']
    inlines = [OrderItemInline]

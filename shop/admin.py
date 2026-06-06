from django.contrib import admin

from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'weight_grams', 'available', 'created_at')
    list_filter = ('category', 'available')
    list_editable = ('available',)
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
    ordering = ('-created_at',)

from django import forms

from shop.models import Category, Product
from orders.models import Order, PromoCode

from .utils import unique_slug


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'name', 'description', 'price',
                  'weight_grams', 'image', 'available']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
        }

    def save(self, commit=True):
        obj = super().save(commit=False)
        if not obj.slug:
            obj.slug = unique_slug(Product, obj.name, obj.pk)
        if commit:
            obj.save()
        return obj


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'image']

    def save(self, commit=True):
        obj = super().save(commit=False)
        if not obj.slug:
            obj.slug = unique_slug(Category, obj.name, obj.pk)
        if commit:
            obj.save()
        return obj


class OrderStatusForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status']


class PromoCodeForm(forms.ModelForm):
    class Meta:
        model = PromoCode
        fields = ['code', 'discount_percent', 'active', 'valid_until']
        widgets = {
            'valid_until': forms.DateInput(attrs={'type': 'date'}),
        }

from django import forms

from .models import Order


class OrderForm(forms.ModelForm):
    promo_code = forms.CharField(label='Промокод', max_length=50, required=False)

    class Meta:
        model = Order
        fields = ['full_name', 'phone', 'address', 'delivery_method']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
            'delivery_method': forms.RadioSelect(),
        }

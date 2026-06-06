from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import User


class RegisterForm(UserCreationForm):
    full_name = forms.CharField(
        label='ФИО',
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={'autocomplete': 'name'}),
    )
    phone = forms.CharField(
        label='Телефон',
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={'autocomplete': 'tel'}),
    )

    class Meta:
        model = User
        fields = ('email', 'full_name', 'phone', 'password1', 'password2')
        widgets = {
            'email': forms.EmailInput(attrs={'autocomplete': 'email'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = ''

    def save(self, commit=True):
        user = super().save(commit=False)
        user.full_name = self.cleaned_data['full_name']
        user.phone = self.cleaned_data.get('phone', '')
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget = forms.EmailInput(
            attrs={'autocomplete': 'email'}
        )


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('full_name', 'phone')
        widgets = {
            'full_name': forms.TextInput(attrs={'autocomplete': 'name'}),
            'phone':     forms.TextInput(attrs={'autocomplete': 'tel'}),
        }
        labels = {
            'full_name': 'ФИО',
            'phone':     'Телефон',
        }

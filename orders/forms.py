from django import forms
from django.forms import TextInput
from django.shortcuts import get_object_or_404

from shop.models import Product
from .models import Order


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'phone_number','address','postal_code', 'city']
        widgets = {
            'first_name': TextInput(attrs={'class': 'input', 'placeholder': 'First Name'}),
            'last_name': TextInput(attrs={'class': 'input', 'placeholder': 'Last Name'}),
            'email': TextInput(attrs={'class': 'input', 'placeholder': 'Email Address'}),
            'phone_number': TextInput(attrs={'class': 'input', 'placeholder': 'Phone Number'}),
            'address': TextInput(attrs={'class': 'input', 'placeholder': 'Address'}),
            'postal_code': TextInput(attrs={'class': 'input', 'placeholder': 'Postal Code'}),
            'city': TextInput(attrs={'class': 'input', 'placeholder': 'City'}),

        }


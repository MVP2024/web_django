# File: D:/Project/web_django-develop/catalog/forms.py

from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'image', 'category', 'price']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}), # Используем form-select для select
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, label="Имя", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваше имя'}))
    phone = forms.CharField(max_length=20, label="Телефон", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Контактный телефон'}))
    message = forms.CharField(label="Сообщение", widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Сюда нужно что-то написать'}))
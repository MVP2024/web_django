# File: D:/Project/web_django-develop/catalog/forms.py

from django import forms
from django.core.exceptions import ValidationError

from .models import Product


class ProductForm(forms.ModelForm):
    """
    Форма для создания и редактирования продуктов.
    Использует модель Product и настраивает виджеты для полей формы.
    Добавлена валидация для полей 'name' и 'description' на наличие запрещенных слов.
    """

    FORBIDDEN_WORDS = [
        "казино",
        "криптовалюта",
        "крипта",
        "биржа",
        "дешево",
        "дёшево",
        "бесплатно",
        "обман",
        "полиция",
        "радар",
    ]

    class Meta:
        model = Product
        fields = ["name", "description", "image", "category", "price"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-select"}),  # Используем form-select для select
            "price": forms.NumberInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name not in ["image", "category"]: # если есть поля с заданными виджетами, то их исключаем.
                field.widget.attrs["class"] = "form-control"

    def clean_name(self):
        """
        Валидация поля 'name' на наличие запрещённых слов
        """
        name = self.cleaned_data["name"]
        for word in self.FORBIDDEN_WORDS:
            if word in name.lower():
                raise ValidationError(f"Слово '{word}' запрещено в описании продукта!")
        return name

    def clean_description(self):
        """
        Валидация поля 'description' на наличие запрещённых слов
        """
        description = self.cleaned_data["description"]
        if description:
            for word in self.FORBIDDEN_WORDS:
                if word in description.lower():
                    raise ValidationError(f"Слово '{word}' запрещено в описании продукта!")
            return description

    def clean_price(self):
        """
        Валидация поля 'price' на отсутствие отрицатеьных значений.
        """
        price = self.cleaned_data["price"]
        if price is not None and price < 0:
            raise ValidationError("Цена продукта не может быть отрицательной!")
        return price


class ContactForm(forms.Form):
    """
    Форма для страницы контактов.
    Собирает имя, телефон и сообщение от пользователя.
    """

    name = forms.CharField(
        max_length=100, label="Имя", widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Ваше имя"})
    )
    phone = forms.CharField(
        max_length=20,
        label="Телефон",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Контактный телефон"}),
    )
    message = forms.CharField(
        label="Сообщение",
        widget=forms.Textarea(attrs={"class": "form-control", "placeholder": "Сюда нужно что-то написать"}),
    )

from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    """
    Форма для создания и редактирования записей блога.
    Использует модель Post и настраивает виджеты для полей формы.
    """

    class Meta:
        model = Post
        fields = ["title", "content", "preview", "is_published"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "content": forms.Textarea(attrs={"class": "form-control"}),
            "preview": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "is_published": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

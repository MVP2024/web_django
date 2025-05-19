from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, TemplateView
from django.views.generic.edit import FormMixin

from .forms import ContactForm, ProductForm
from .models import Category, ContactInfo, Product


class HomeView(ListView):
    model = Product
    template_name = "home.html"
    context_object_name = "latest_products"
    queryset = Product.objects.order_by("-created_at")[:5]


class ContactView(FormMixin, TemplateView):
    template_name = "contacts.html"
    form_class = ContactForm
    success_url = reverse_lazy("catalog:contacts")  # Перенаправление на ту же страницу после отправки

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Получаем контактную информацию из базы данных
        context["contact_info"] = ContactInfo.objects.first()
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        # Обработка данных формы (например, отправка email или сохранение в БД)
        name = form.cleaned_data["name"]
        phone = form.cleaned_data["phone"]
        message = form.cleaned_data["message"]
        print(f"Получено сообщение от {name}: телефон: {phone} и сообщение: {message}")
        # Здесь можно добавить логику отправки email или сохранения в базу данных
        return super().form_valid(form)

    def form_invalid(self, form):
        # Если форма невалидна, рендерим шаблон с ошибками
        return self.render_to_response(self.get_context_data(form=form))


class ProductDetailView(DetailView):
    model = Product
    template_name = "product_detail.html"
    context_object_name = "product"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем PK категории в контекст для ссылки "Назад к категории"
        context["category_pk"] = self.object.category.pk
        return context


class CategoryListView(ListView):
    model = Category
    template_name = "category_list.html"
    context_object_name = "categories"
    queryset = Category.objects.all()


class ProductListByCategoryView(ListView):
    model = Product
    template_name = "product_list_by_category.html"
    context_object_name = "products"

    def get_queryset(self):
        # Получаем PK категории из URL и фильтруем продукты
        category_pk = self.kwargs["pk"]
        return Product.objects.filter(category__pk=category_pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Получаем объект категории для отображения в заголовке
        context["category"] = get_object_or_404(Category, pk=self.kwargs["pk"])
        return context


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = "product_create.html"
    success_url = reverse_lazy("catalog:home")  # Перенаправление после успешного создания

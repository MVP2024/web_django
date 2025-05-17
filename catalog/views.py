from django.shortcuts import render, get_object_or_404, redirect

from .forms import ProductForm
from .models import Product, ContactInfo, Category


def home(request):
    # Выбираем последние 5 продуктов, сортируя по дате создания в обратном порядке
    latest_products = Product.objects.order_by("-created_at")[:5]

    # выволим их в консоль
    print("Последние 5 добавленных продуктов")
    for product in latest_products:
        print(f"- {product.name} (Цена: {product.price})")

        # Передаем список продуктов в контекст шаблона
        return render(request, "home.html", {"latest_products": latest_products})


def contacts(request):
    # Получаем контактную информацию из базы данных
    contact_info = ContactInfo.objects.first()

    if request.method == "POST":
        # Получаем данные из формы
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message = request.POST.get("message")

        print(f"Получено сообщение от {name}: телефон: {phone} и сообщение: {message}")

        # Перел/даём контактную информацию и данные в контекст
        return render(request, "contacts.html",
                      {"contact_info": contact_info, "name": name, "phone": phone, "message": message})

    # Если метод запроса GET, то просто выводим страницу контактов
    return render(request, "contacts.html", {"contact_info": contact_info})


def product_detail(request, pk):
    # Получаем продукт по pk или возвращаем ошибку 404
    product = get_object_or_404(Product, pk=pk)
    context = {
    "product": product,
    "category_pk": product.category.pk  # Добавляем PK категории в контекст
    }
    return render(request, "product_detail.html", context)


def category_list(request):
    categories = Category.objects.all() # Получаем все категории
    context = {
        "categories": categories # Передаем их в контекст
    }
    return render(request, "category_list.html", context)


def product_list_by_category(request, pk):
    # Получаем категорию по pk или возвращаем ошибку 404
    category = get_object_or_404(Category, pk=pk)
    # Получаем все продукты, связанные с этой категорией
    products = Product.objects.filter(category=category)
    context = {
        "category": category,
        "products": products
    }
    return render(request, "product_list_by_category.html", context)


def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # Перенаправляем пользователя, например, на главную страницу или список товаров
            return redirect('catalog:home') # Укажите имя URL-шаблона, куда перенаправить
    else:
        form = ProductForm()
    context = {'form': form}
    return render(request, 'product_create.html', context)
from django.shortcuts import render

from .models import Product


def home(request):
    # Выбираем последние 5 продуктов, сортируя по дате создания в обратном порядке
    latest_products = Product.objects.order_by("-created_at")[:5]

    # выволим их в консоль
    print("Последние 5 добавленных продуктов")
    for product in latest_products:
        print(f"- {product.name} (Цена: {product.price})")

    return render(request, "home.html")


def contacts(request):
    if request.method == "POST":
        # Получаем данные из формы
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message = request.POST.get("message")

        print(f"Получено сообщение от {name}: телефон: {phone} и сообщение: {message}")

        return render(request, "contacts.html", {"name": name, "phone": phone, "message": message})

    # Если метод запроса GET, то просто выводим страницу контактов
    return render(request, "contacts.html")

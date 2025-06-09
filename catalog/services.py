from django.core.cache import caches
from .models import Product, Category
from django.shortcuts import get_object_or_404


def get_products_by_category_cached(category_pk: int):
    """
    Возвращает список продуктов для указанной категории, используя кеширование.
    """
    cache_key = f"products_in_category_service_{category_pk}"
    # Используем кеш по умолчанию для чтения, так как он может содержать данные
    products = caches['default'].get(cache_key) # Обращаемся к кешу по имени

    if products is None:
        # Если данные не в кеше, получаем их из БД
        category = get_object_or_404(Category, pk=category_pk)
        products = list(Product.objects.filter(category=category, is_published=True).select_related('category').order_by('name'))
        # Кешируем данные на 1 час, используя 'product_cache'
        product_cache = caches['product_cache']  # Получаем конкретный кеш по имени
        product_cache.set(cache_key, products, timeout=3600) # Устанавливаем данные в этот кеш
    return products
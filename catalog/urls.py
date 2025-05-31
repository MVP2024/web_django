# File: D:/Project/web_django-develop/catalog/urls.py

from django.urls import path
from .views import (
    HomeView,
    ContactView,
    ProductDetailView,
    CategoryListView,
    ProductListByCategoryView,
    ProductCreateView,
)

app_name = "catalog"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("contacts/", ContactView.as_view(), name="contacts"),
    path("products/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
    path("categories/", CategoryListView.as_view(), name="category_list"),
    path(
        "categories/<int:pk>/products/",
        ProductListByCategoryView.as_view(),
        name="product_list_by_category",
    ),
    path("products/create/", ProductCreateView.as_view(), name="create_product"),
]
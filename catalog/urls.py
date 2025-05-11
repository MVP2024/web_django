from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import contacts, home, product_detail, category_list, product_list_by_category, create_product

app_name = CatalogConfig.name

urlpatterns = [
    path("", home, name="home"),
    path("contacts/", contacts, name="contacts"),
    path("product/<int:pk>/", product_detail, name="product_detail"),
    path("categories/", category_list, name="category_list"),
    path("category/<int:pk>/products/", product_list_by_category, name="product_list_by_category"),
    path("create/", create_product, name="create_product"),
]

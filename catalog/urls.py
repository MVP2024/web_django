from django.urls import path

from .views import (CategoryListView, ContactView, HomeView, ProductCreateView,
                    ProductDetailView, ProductListByCategoryView, ProductDeleteView, unpublish_product,
                    ProductUpdateView)

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
path("products/<int:pk>/update/", ProductUpdateView.as_view(), name="update_product"),
    path("products/<int:pk>/delete/", ProductDeleteView.as_view(), name="delete_product"),
    path("products/<int:pk>/unpublish/", unpublish_product, name="unpublish_product"),
]

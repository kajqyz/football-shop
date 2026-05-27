from django.urls import path

from .views import (
    AboutView,
    BrandDetailView,
    BrandListView,
    CartView,
    CategoryDetailView,
    CategoryListView,
    ClubDetailView,
    ClubListView,
    HomeView,
    OrderDetailView,
    OrderListView,
    ProductDetailView,
    ProductListView,
    SupplierDetailView,
    SupplierListView,
)

app_name = "firstproject"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("about/", AboutView.as_view(), name="about"),
    path("cart/", CartView.as_view(), name="cart"),
    path("products/", ProductListView.as_view(), name="product_list"),
    path("products/<slug:slug>/", ProductDetailView.as_view(), name="product_detail"),
    path("categories/", CategoryListView.as_view(), name="category_list"),
    path(
        "categories/<slug:slug>/",
        CategoryDetailView.as_view(),
        name="category_detail",
    ),
    path("clubs/", ClubListView.as_view(), name="club_list"),
    path("clubs/<int:pk>/", ClubDetailView.as_view(), name="club_detail"),
    path("brands/", BrandListView.as_view(), name="brand_list"),
    path("brands/<int:pk>/", BrandDetailView.as_view(), name="brand_detail"),
    path("suppliers/", SupplierListView.as_view(), name="supplier_list"),
    path("suppliers/<int:pk>/", SupplierDetailView.as_view(), name="supplier_detail"),
    path("orders/", OrderListView.as_view(), name="order_list"),
    path("orders/<int:pk>/", OrderDetailView.as_view(), name="order_detail"),
]

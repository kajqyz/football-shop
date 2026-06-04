from rest_framework import filters, permissions, viewsets

from .api_serializers import (
    BrandSerializer,
    CategorySerializer,
    ClubSerializer,
    CustomerSerializer,
    OrderItemSerializer,
    OrderSerializer,
    ProductSerializer,
    SupplierSerializer,
)
from .models import Brand, Category, Club, Customer, Order, OrderItem, Product, Supplier


class ReadOnlyOrAuthenticated(permissions.IsAuthenticatedOrReadOnly):
    message = "Изменять данные API могут только авторизованные пользователи."


class BaseApiViewSet(viewsets.ModelViewSet):
    permission_classes = [ReadOnlyOrAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]


class CategoryViewSet(BaseApiViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    search_fields = ["name", "slug", "description"]
    ordering_fields = ["id", "name", "slug"]


class ClubViewSet(BaseApiViewSet):
    queryset = Club.objects.all()
    serializer_class = ClubSerializer
    search_fields = ["name", "country", "league", "description"]
    ordering_fields = ["id", "name", "country", "league"]


class BrandViewSet(BaseApiViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    search_fields = ["name", "country", "description"]
    ordering_fields = ["id", "name", "country"]


class SupplierViewSet(BaseApiViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    search_fields = ["name", "city", "email", "phone", "description"]
    ordering_fields = ["id", "name", "city", "email"]


class ProductViewSet(BaseApiViewSet):
    queryset = Product.objects.select_related("category", "club", "brand", "supplier")
    serializer_class = ProductSerializer
    search_fields = [
        "name",
        "slug",
        "short_description",
        "description",
        "category__name",
        "club__name",
        "brand__name",
        "supplier__name",
    ]
    ordering_fields = ["id", "name", "price", "stock", "created_at"]


class CustomerViewSet(BaseApiViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    search_fields = ["first_name", "last_name", "email", "phone"]
    ordering_fields = ["id", "last_name", "first_name", "email"]


class OrderViewSet(BaseApiViewSet):
    queryset = Order.objects.select_related("customer", "user").prefetch_related("items")
    serializer_class = OrderSerializer
    search_fields = [
        "customer__first_name",
        "customer__last_name",
        "customer__email",
        "user__username",
        "status",
        "delivery_address",
    ]
    ordering_fields = ["id", "created_at", "status"]


class OrderItemViewSet(BaseApiViewSet):
    queryset = OrderItem.objects.select_related("order", "product")
    serializer_class = OrderItemSerializer
    search_fields = ["product__name", "order__customer__email"]
    ordering_fields = ["id", "order", "product", "quantity", "price"]

from rest_framework import serializers

from football_shop.models import (
    Brand,
    Category,
    Club,
    Customer,
    Order,
    OrderItem,
    Product,
    Supplier,
)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug", "description"]


class ClubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Club
        fields = ["id", "name", "country", "league", "logo", "description"]


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ["id", "name", "country", "logo", "description"]


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ["id", "name", "city", "email", "phone", "description"]


class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)
    club_name = serializers.CharField(source="club.name", read_only=True)
    brand_name = serializers.CharField(source="brand.name", read_only=True)
    supplier_name = serializers.CharField(source="supplier.name", read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "slug",
            "category",
            "category_name",
            "club",
            "club_name",
            "brand",
            "brand_name",
            "supplier",
            "supplier_name",
            "price",
            "stock",
            "photo",
            "short_description",
            "description",
            "created_at",
        ]
        read_only_fields = ["created_at"]


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ["id", "first_name", "last_name", "email", "phone"]


class OrderSerializer(serializers.ModelSerializer):
    customer_name = serializers.SerializerMethodField()
    username = serializers.CharField(source="user.username", read_only=True)
    total_price = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True
    )

    class Meta:
        model = Order
        fields = [
            "id",
            "customer",
            "customer_name",
            "user",
            "username",
            "created_at",
            "status",
            "delivery_address",
            "total_price",
        ]
        read_only_fields = ["created_at", "total_price"]

    def get_customer_name(self, obj):
        return str(obj.customer)


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)
    total_price = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True
    )

    class Meta:
        model = OrderItem
        fields = [
            "id",
            "order",
            "product",
            "product_name",
            "quantity",
            "price",
            "total_price",
        ]
        read_only_fields = ["total_price"]

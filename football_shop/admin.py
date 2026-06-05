from django.contrib import admin

from .models import Brand, Category, Club, Customer, Order, OrderItem, Product, Supplier


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    list_display = ("name", "country", "league")
    search_fields = ("name", "country", "league")


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ("name", "country")
    search_fields = ("name", "country")


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ("name", "city", "email", "phone")
    search_fields = ("name", "city", "email")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "club", "brand", "price", "stock")
    list_filter = ("category", "club", "brand")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "short_description")


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("last_name", "first_name", "email", "phone")
    search_fields = ("last_name", "first_name", "email")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "customer", "user", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("customer__email", "customer__last_name", "user__username")
    inlines = [OrderItemInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "product", "quantity", "price", "total_price")
    list_filter = ("product",)
    search_fields = ("order__id", "product__name")

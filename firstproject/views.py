from django.views.generic import DetailView, ListView, TemplateView

from .models import Brand, Category, Club, Order, Product, Supplier


class HomeView(TemplateView):
    template_name = "firstproject/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["featured_products"] = Product.objects.select_related(
            "category", "club", "brand"
        )[:4]
        return context


class AboutView(TemplateView):
    template_name = "firstproject/about.html"


class CartView(TemplateView):
    template_name = "firstproject/cart.html"


class ProductListView(ListView):
    model = Product
    template_name = "firstproject/product_list.html"
    context_object_name = "products"

    def get_queryset(self):
        return Product.objects.select_related("category", "club", "brand", "supplier")


class ProductDetailView(DetailView):
    model = Product
    template_name = "firstproject/product_detail.html"
    context_object_name = "product"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        return Product.objects.select_related("category", "club", "brand", "supplier")


class CategoryListView(ListView):
    model = Category
    template_name = "firstproject/category_list.html"
    context_object_name = "categories"


class CategoryDetailView(DetailView):
    model = Category
    template_name = "firstproject/category_detail.html"
    context_object_name = "category"
    slug_field = "slug"
    slug_url_kwarg = "slug"


class ClubListView(ListView):
    model = Club
    template_name = "firstproject/club_list.html"
    context_object_name = "clubs"


class ClubDetailView(DetailView):
    model = Club
    template_name = "firstproject/club_detail.html"
    context_object_name = "club"


class BrandListView(ListView):
    model = Brand
    template_name = "firstproject/brand_list.html"
    context_object_name = "brands"


class BrandDetailView(DetailView):
    model = Brand
    template_name = "firstproject/brand_detail.html"
    context_object_name = "brand"


class SupplierListView(ListView):
    model = Supplier
    template_name = "firstproject/supplier_list.html"
    context_object_name = "suppliers"


class SupplierDetailView(DetailView):
    model = Supplier
    template_name = "firstproject/supplier_detail.html"
    context_object_name = "supplier"


class OrderListView(ListView):
    model = Order
    template_name = "firstproject/order_list.html"
    context_object_name = "orders"

    def get_queryset(self):
        return Order.objects.select_related("customer").prefetch_related("items")


class OrderDetailView(DetailView):
    model = Order
    template_name = "firstproject/order_detail.html"
    context_object_name = "order"

    def get_queryset(self):
        return Order.objects.select_related("customer").prefetch_related(
            "items__product"
        )
